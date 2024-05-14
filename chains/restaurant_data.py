from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough, RunnableParallel
from prompts.common import SYSTEM_PROMPT
from chains.sql import MySQLChain


class RestaurantInfoChain:

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
        Use the following pieces of retrieved context to answer the question.
        If you don't know the answer, just say that you don't know.
        If the context is empty then tell the user that no such data exists
        Please format your response in Markdown. Include any necessary bullet points, tables, highlights, bold and italic text to enhance clarity and emphasis where needed.
        Render tables without code
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
            }
        ).assign(answer=main_chain)

        return chain.invoke(prompt)

        # rag_chain_with_source = RunnableParallel(
        #     {"context": retriever, "question": RunnablePassthrough()}
        # ).assign(answer=rag_chain_from_docs)
