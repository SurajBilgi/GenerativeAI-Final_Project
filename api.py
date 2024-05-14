import json
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse

from router import PromptRouter
from models import initialize_llm
from chains.restaurant_data import RestaurantInfoChain
from chains.recommendation import RecommendationChain
from chains.complaint import ComplaintChain
from utils.sql import SQLite

llm = initialize_llm(name="gpt4o")

chain_info = json.load(open("chains/chains.json"))

chat_chains = {
    "restaurant_data": RestaurantInfoChain(),
    "recommendation": RecommendationChain(),
}

complaint_chain = ComplaintChain()

prompt_router = PromptRouter(chain_info=chain_info)

sqlite = SQLite()
app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/restaurant-list")
async def restaurant_list():
    result = sqlite(
        """
        SELECT distinct restaurantname FROM details
        """
    )
    return {"restaurant_list": [r["restaurantname"] for r in result]}


@app.post("/restaurant-info")
async def restaurant_info(text: str = Form(...)):
    result = sqlite(
        f"""
        SELECT item_type, item_name, cost, preparation_time 
        FROM details 
        WHERE  restaurantname like "%{text}%"
        """
    )
    return {"restaurant_info": result}


@app.post("/search")
async def search(text: dict):
    prompt = text["text"]
    chain_name = prompt_router.get_chain_name(prompt)
    print(chain_name)
    chain = chat_chains[chain_name]
    return chain.process_prompt(llm, prompt)


@app.post("/complaint")
async def complaint(
    cust_file: UploadFile = File(...),
    ref_file: UploadFile = File(...),
    text: str = Form(...),
):
    if cust_file.filename == "" or ref_file.filename == "":
        return JSONResponse(status_code=400, content={"error": "No selected file"})

    cus_contents = await cust_file.read()
    ref_contents = await ref_file.read()

    return complaint_chain.process_prompt(llm, text, cus_contents, ref_contents)
