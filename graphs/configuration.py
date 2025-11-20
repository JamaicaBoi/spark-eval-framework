from typing import TypedDict, Literal

class GraphConfig(TypedDict):
    # Prompts configuration
    prompt_provider: Literal["local", "langsmith", "langfuse"] = "langsmith"

    # LLMs configuration
    llm_provider: Literal["openai", "anthropic"] = "openai"
    model_name: str = "gpt-5-mini"
    temperature: float = 0