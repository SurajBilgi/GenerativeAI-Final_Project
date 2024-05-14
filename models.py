from langchain_openai import ChatOpenAI


def initialize_llm(name) -> ChatOpenAI:
    try:
        model = {"gpt3.5": "gpt-3.5-turbo", "gpt4": "gpt-4-turbo"}
        return ChatOpenAI(
            model=model[name],
            temperature=0,
        )
    except Exception:
        raise NotImplemented
