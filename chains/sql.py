from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI
import json

from prompts.sql import SQL_GENERATION_PROMPT
from utils.sql import SQLite


class SQLiteChain:

    def __init__(self) -> None:
        self.output_parser = StrOutputParser()
        self.prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You are skilled SQL Engineer who can extract relevant entities from a question and convert that into a SQL query",
                ),
                ("user", SQL_GENERATION_PROMPT),
            ]
        )

        self.SQLite = SQLite()
        self.llm = ChatOpenAI(model="gpt-3.5-turbo-0613")

    def process_query(self, query):
        data = self.SQLite(query)
        return json.dumps(data)

    def return_sql_chain(self, prompt: str) -> str:
        return (
            {"input": RunnablePassthrough()}
            | self.prompt
            | self.llm
            | StrOutputParser()
            | self.process_query
        )
