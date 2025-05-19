from langchain_openai import ChatOpenAI

def get_llm(api_key: str) -> ChatOpenAI:
    return ChatOpenAI(
        model="gpt-4",
        temperature=0,
        max_tokens=None,
        timeout=None,
        max_retries=2,
        api_key=api_key,
    )
