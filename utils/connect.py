VERSION = "2021-08-16"


class Notion:
    headers = {}

    @classmethod
    def connect(cls, token: str) -> None:
        cls.headers = {
            "Authorization": f"Bearer {token}",
            "Notion-Version": f"{VERSION}",
            "Content-Type": "application/json",
        }
