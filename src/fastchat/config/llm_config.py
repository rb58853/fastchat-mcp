import os


class ConfigLLM:
    DEFAULT_HISTORY_LEN: int = 20


class ConfigModel:
    MODEL_PRICE = {
        "gpt-3.5-turbo": {
            "input": 0.5 / 1000000,
            "output": 1.5 / 1000000,
        },
        "gpt-4o-mini": {
            "input": 0.15 / 1000000,
            "output": 0.60 / 1000000,
        },
        "gpt-5-mini": {
            "input": 0.25 / 1000000,
            "output": 2.00 / 1000000,
        },
        "gpt-5-nano": {
            "input": 0.05 / 1000000,
            "output": 0.40 / 1000000,
        },
        "groq/openai/gpt-oss-120b": {
            "input": 0.30 / 1000000,
            "output": 0.30 / 1000000,
        },
    }
    """Price by one tokens from each model"""

    DEFAULT_MODEL_NAME = "groq/openai/gpt-oss-120b"
    """Default model identifier that will be used"""

    LITELLM_API_KEY = os.environ.get("LITELLM_API_KEY")
    """Optional default API key for LiteLLM provider routing"""

    LITELLM_BASE_URL = os.environ.get("LITELLM_BASE_URL")
    """Optional default base URL for OpenAI-compatible providers"""

    OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
    """Backward-compatible API key (also consumed by LiteLLM for OpenAI models)"""
