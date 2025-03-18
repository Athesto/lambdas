import requests
from dataclasses import dataclass

@dataclass
class TelegramAPIParams():
    TOKEN: str
    CHAT_ID: str

@dataclass
class TelegramClient:
    token: str

    def sendMessage(self, chat_id, text, link_preview_options):
        return requests.post(
            f"https://api.telegram.org/bot{self.token}/sendMessage",
            data={
                "chat_id": chat_id,
                "parse_mode": "html",
                "text": text,
                "link_preview_options": link_preview_options
            },
        )
