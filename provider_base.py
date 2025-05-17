from abc import ABC, abstractmethod


class LLMProvider(ABC):
    def get_response(self, filename: str) -> str:
        messages = self._build_messages(filename)
        raw = self._send_request(messages)
        return self._extract_content(raw)

    @abstractmethod
    def _build_messages(self, filename: str) -> list:
        pass

    @abstractmethod
    def _send_request(self, messages: list):
        pass

    @abstractmethod
    def _extract_content(self, raw) -> str:
        pass
