import requests
from config import OPENTYPHOON_API_URL, OPENTYPHOON_API_KEY, OPENTYPHOON_MODEL, SYSTEM_PROMPT
from provider_base import LLMProvider


class OpenTyphoonProvider(LLMProvider):
    def _build_messages(self, filename: str) -> list:
        return [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": filename}
        ]

    def _send_request(self, messages: list):
        headers = {
            "Authorization": f"Bearer {OPENTYPHOON_API_KEY}",
            "Content-Type": "application/json",
        }
        data = {
            "model": OPENTYPHOON_MODEL,
            "messages": messages,
            "temperature": 0.2
        }
        try:
            response = requests.post(OPENTYPHOON_API_URL, json=data, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"[OpenTyphoon] Error: {e}")
            return None

    def _extract_content(self, raw) -> str:
        if raw:
            try:
                return raw["choices"][0]["message"]["content"].strip()
            except (KeyError, IndexError):
                return None
        return None
