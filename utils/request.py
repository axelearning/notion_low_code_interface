import requests
from typing import Dict
import json

VERSION = "2021-08-16"


def catch_error(response):
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        if response.status_code == 401:
            raise Exception(
                "❌ Connect to Notion with your Token: Notion.connect(YOUR_TOKEN_API)"
            )
        else:
            raise Exception("❌", err, response.text)


class RequestNotionAPI:
    def __init__(self, headers: Dict, id: str = None) -> None:
        self.headers = headers
        self.id = id


class RequestDatabase(RequestNotionAPI):
    URL = "https://api.notion.com/v1/databases"

    def create(self, data):
        pass


class RequestPage(RequestNotionAPI):
    URL = "https://api.notion.com/v1/pages/"

    def retreive(self) -> Dict:
        url = self.URL + self.id
        response = requests.get(url, headers=self.headers)
        catch_error(response)
        return response.json()

    def create(self, data) -> Dict:
        data = json.dumps(data)
        response = requests.post(self.URL, headers=self.headers, data=data)
        catch_error(response)
        print("✅ Page has been created")
        return response.json()

    def update(self, data):
        url = self.URL + self.id
        data = json.dumps(data)
        response = requests.patch(url, headers=self.headers, data=data)
        catch_error(response)
        print("✨ Properties have been updated")


class RequestBlock(RequestNotionAPI):
    URL = "https://api.notion.com/v1/blocks/"

    def update(self, data):
        url = self.URL + self.id
        data = json.dumps(data)
        response = requests.patch(url, headers=self.headers, data=data)
        catch_error(response)
        print("✅ Block has been updated")

    def retreive_children(self) -> Dict:
        url = self.URL + self.id + "/children"
        response = requests.get(url, headers=self.headers)
        catch_error(response)
        return response.json()["results"]

    def append_children(self, data):
        url = self.URL + self.id + "/children"

        data = {"children": [data]}
        data = json.dumps(data)

        response = requests.patch(url, headers=self.headers, data=data)
        catch_error(response)
        print("✅ Block has been add to your page")

    def delete(self):
        url = self.URL + self.id
        response = requests.delete(url, headers=self.headers)
        catch_error(response)
        print("🌪 Block has been deleted")
