import requests
from ollama import ChatResponse, Client
from config import OLLAMA_API_URL, OLLAMA_MODEL, SYSTEM_PROMPT
from provider_base import LLMProvider


class OllamaProvider(LLMProvider):
    def __init__(self):
        self.client = Client(host=OLLAMA_API_URL)

    def _build_messages(self, filename: str) -> list:
        return [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": filename}
        ]

    def _send_request(self, messages: list):
        try:
            return self.client.chat(model=OLLAMA_MODEL, messages=messages)
        except requests.exceptions.RequestException as e:
            print(f"[Ollama] Error: {e}")
            return None

    def _extract_content(self, raw) -> str:
        if raw:
            return raw.message.content
        return None
