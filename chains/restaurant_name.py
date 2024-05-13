from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough


class RestaurantNameChain:

    SYSTEM_PROMPT = (
        "system",
        "Your name is DineMate. You are a chatbot that helps users fetch information regarding restaurants near them, recommend dishes based on their previous orders and resolve customer complaints",
    )

    USER_PROMPT = (
        "user",
        """
        List all the restaurants provided in the context below
        Format them in markdown and highlights
        {context}
        """.strip(),
    )

    def __init__(self) -> None:
        self.names = ["Bistro Fusion", "Spice Symphony", "The Culinary Haven"]
        self.prompt = ChatPromptTemplate.from_messages(
            [self.SYSTEM_PROMPT, self.USER_PROMPT]
        )
        self.output_parser = StrOutputParser()

    def process_prompt(self, llm, prompt: str) -> str:
        chain = {"context": RunnablePassthrough()} | prompt | llm | self.output_parser
        return chain.invoke({"context": ", ".join(self.names)})
