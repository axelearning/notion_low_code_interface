from utils.request import RequestPage, RequestBlock
from utils.page import PageProperties, PageContent
from utils.connect import Notion


class Database:
    def __init__(self, database_url: str) -> None:
        self.url = database_url

    @property
    def id(self):
        path = self.url.split("/")[-1]
        return path.split("?")[0]

    def create_new_page(self):
        data = {
            "parent": {"database_id": self.id},
            "properties": {"title": [{"text": {"content": "New page"}}]},
        }
        raw_page = RequestPage(Notion.headers).create(data)
        return Page(raw_page["url"])


class Page:
    def __init__(self, page_url: str) -> None:
        self.url = page_url
        self.id = page_url.split("-")[-1]

        self._properties = RequestPage(Notion.headers, self.id).retreive()
        self.created_time = self._properties["created_time"]
        self.last_edited_time = self._properties["last_edited_time"]
        self.archived = self._properties["archived"]
        self.icon = self._properties["icon"]
        self.cover = self._properties["cover"]
        self.properties = PageProperties(self._properties, Notion.headers)
        self.parent = self._properties["parent"]

        self._content = RequestBlock(Notion.headers, self.id).retreive_children()
        self.content = PageContent(self._content, self.id, Notion.headers)

    def refresh(self):
        """Retreive Page properties & content."""
        return self.__init__(self.url)

    def delete(self):
        """Archiving workspace level pages via API not supported."""
        RequestBlock(Notion.headers, self.id).delete()


if __name__ == "__main__":

    import os
    from dotenv import load_dotenv

    load_dotenv()
    TOKEN_API = os.getenv("TOKEN_API")
    PAGE_URL = os.getenv("PAGE_URL")
    DATABASE_URL = os.getenv("DATABASE_URL")

    Notion.connect(TOKEN_API)
    database = Database(DATABASE_URL)
    page = Page(PAGE_URL)

    from utils.block import *
