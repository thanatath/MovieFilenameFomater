from config import USE_OLLAMA
from provider_base import LLMProvider
from providers.ollama_provider import OllamaProvider
from providers.opentyphoon_provider import OpenTyphoonProvider


def get_llm_provider() -> LLMProvider:
    return OllamaProvider() if USE_OLLAMA else OpenTyphoonProvider()
