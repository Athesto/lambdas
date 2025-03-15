import requests
from dataclasses import dataclass

@dataclass
class TelegramAPIParams():
    TOKEN: str
    CHAT_ID: str

@dataclass
class TelegramClient:
    token: str

    def sendMessage(self, **kwargs):
        return requests.post(
            f"https://api.telegram.org/bot{self.token}/sendMessage",
            data={
                "chat_id": kwargs.get("chat_id"),
                "parse_mode": "html",
                "text": kwargs.get("text"),
                "link_preview_options":kwargs.get("link_preview_options")
            },
        )
