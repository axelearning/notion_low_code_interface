from typing import Dict
import pandas as pd
from .property import Property
from .block import extract_block, insert_block
from .request import RequestPage, RequestBlock


class PageProperties:
    def __init__(self, properties: Dict, headers: Dict):
        self.headers = headers

        self.raw = properties
        self._properties = properties["properties"]
        self.parent_id = properties["id"]

    def __getitem__(self, key):
        return Property(self._properties[key]).extract()

    def __setitem__(self, key, value):
        Property(self._properties[key]).insert(value)

    def __repr__(self) -> str:
        return f"{self.get()}"

    def get(self) -> pd.Series:
        data = {key: self[key] for key in self._properties.keys()}
        return pd.Series(data)

    def update(self) -> None:
        RequestPage(self.headers, self.parent_id).update(self.raw)


class PageContent:
    def __init__(self, blocks, page_id, headers) -> None:
        self.raw = blocks
        self.page_id = page_id
        self.headers = headers

    def __getitem__(self, index):
        return extract_block(self.raw[index])

    def __setitem__(self, index, value):
        insert_block(self.raw[index], value)

    def __repr__(self) -> str:
        return f"{self.get()}"

    def _repr_html_(self):
        return self.get().to_html()

    def get(self) -> pd.DataFrame:
        result = []
        for block in self.raw:
            result.append(
                {
                    "type": block.get("type"),
                    "content": extract_block(block),
                    "id": block.get("id"),
                }
            )
        return pd.DataFrame(result)

    def append(self, block: Dict) -> None:
        if block["type"] == "child_page":
            block.pop("type")
            block["parent"] = {"page_id": self.page_id}
            RequestPage(self.headers).create(block)
        else:
            RequestBlock(self.headers, self.page_id).append_children(block)
