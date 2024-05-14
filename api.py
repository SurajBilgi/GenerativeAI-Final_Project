import json
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse

from router import PromptRouter
from models import initialize_llm
from chains.restaurant_data import RestaurantInfoChain
from chains.recommendation import RecommendationChain
from chains.complaint import ComplaintChain
from utils.sql import MySQL

llm = initialize_llm(name="gpt4")

chain_info = json.load(open("chains/chains.json"))

chat_chains = {
    "restaurant_data": RestaurantInfoChain(),
    "recommendation": RecommendationChain(),
}

complaint_chain = ComplaintChain()

prompt_router = PromptRouter(llm=llm, chain_info=chain_info)

mysql = MySQL()
app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/restaurant-list")
async def restaurant_list():
    result = mysql(
        """
        SELECT name FROM restaurants.name
        """
    )
    return {"restaurant_list": [r["name"] for r in result]}


@app.post("/restaurant-info")
async def restaurant_info(text: str = Form(...)):
    result = mysql(
        f"""
        SELECT item_type, item_name, cost, preparation_time 
        FROM restaurants.details 
        WHERE restaurant_id in (SELECT id from restaurants.name WHERE name like "%{text}%") 
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
async def complaint(file: UploadFile = File(...), text: str = Form(...)):
    if file.filename == "":
        return JSONResponse(status_code=400, content={"error": "No selected file"})

    contents = await file.read()

    return complaint_chain.process_prompt(llm, text, contents)
