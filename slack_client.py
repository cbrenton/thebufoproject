import json
from urllib.parse import quote

import requests

from bufo_types import Bufo


class SlackClient:
    def __init__(self, workspace: str, user_token: str, session_token: str):
        self._workspace = workspace
        self._user_token = user_token
        self._session_token = session_token
        self._instance_url = f"https://{workspace}.slack.com/api/"

    def paged_iterator(self, endpoint: str, key: str):
        cookies = {"d": quote(self._session_token, safe="")}
        cur_page = 0
        total_pages = 1

        url = f"{self._instance_url}{endpoint}"

        while cur_page < total_pages:
            resp = requests.post(
                url,
                data={
                    "token": self._user_token,
                    "page": cur_page + 1,
                    "queries": json.dumps(["bufo", "frog", "buttfo", "boofo"]),
                },
                cookies=cookies,
                timeout=30,
            )

            result_json = resp.json()

            if result_json.get("ok"):
                for result in result_json.get(key):
                    yield result

                cur_page = result_json["paging"]["page"]
                total_pages = result_json["paging"]["pages"]

                if cur_page == total_pages:
                    break
            else:
                raise Exception(
                    f"Unable to poll Slack API {url}: {result_json.get('error')}"
                )

    def download_bufo(self, bufo: Bufo) -> str:
        response = requests.get(bufo.url)
        return response.content
