from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough, RunnableParallel
from prompts.common import SYSTEM_PROMPT
from chains.sql import MySQLChain
import json


def get_user_past_orders():
    with open("data/past_orders.json") as fp:
        past_orders = json.load(fp)
    return json.dumps(past_orders)


class RecommendationChain:

    def __init__(self) -> None:
        self.mysql_chain = MySQLChain()

    def process_prompt(self, llm, prompt: str) -> str:
        sql_chain = self.mysql_chain.return_sql_chain(prompt)
        template = ChatPromptTemplate.from_messages(
            [
                SYSTEM_PROMPT,
                (
                    "human",
                    """ 
                    Based on the users past orders suggest him dishes from the context.
                    Explain to the user as to why the dishes are being recommended.
                    Do not recommend the past orders.
                    If you don't know the answer, just say that you don't know.
                    If the context is empty then tell the user that no such data exists
                    Please format your response in Markdown. Include any necessary bullet points, tables, highlights, bold and italic text to enhance clarity and emphasis where needed.
                    Render tables without code
                    PastOrders: {past_orders}
                    Question: {question}
                    Context: {context}
                    Answer:""".strip(),
                ),
            ]
        )
        main_chain = template | llm | StrOutputParser()
        chain = RunnableParallel(
            {
                "context": sql_chain,
                "question": RunnablePassthrough(),
                "past_orders": lambda x: get_user_past_orders(),
            }
        ).assign(answer=main_chain)

        return chain.invoke(prompt)
