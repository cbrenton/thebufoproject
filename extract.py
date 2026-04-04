#!/usr/bin/env python

import time
import hashlib
import json
import os
import requests
import yaml
from urllib.parse import quote

type BufoData = dict[str, tuple[str, int]]
type BufoMap = dict[str, BufoData]


class BufoAnalyzer:
    def __init__(self, slack_workspace: str, token: str, session_token: str):
        self._slack_workspace = slack_workspace
        self._user_token = token
        self._session_token = session_token
        self._filename = "bufoset.json"

    def run(self):
        self._write_metadata_file(self._get_emoji_list())

    def _get_emoji_list(self) -> BufoMap:
        # undocumented cookie-based endpoint - the api endpoint wants a bot token
        url = f"https://{self._slack_workspace}.slack.com/api/emoji.adminList"
        cookies = {"d": quote(self._session_token, safe="")}

        results = {}
        cur_page = 0

        while True:
            print(f"querying page {cur_page + 1}")
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
                results |= {
                    self._hash(x["name"]): {
                        "user_id_hash": self._hash(x["user_id"]),
                        "created_at": x["created"],
                    }
                    for x in result_json["emoji"]
                }

                cur_page = result_json["paging"]["page"]
                total_pages = result_json["paging"]["pages"]

                if cur_page == total_pages:
                    break
            else:
                raise Exception(f"Unable to poll Slack API: {result_json.get('error')}")

        return results

    def _hash(self, emoji_name: str) -> str:
        return hashlib.sha256(emoji_name.encode("utf-8")).hexdigest()[:12]

    def _write_metadata_file(self, bufo_map: BufoMap):
        with open(self._filename, "w") as f:
            f.write(json.dumps(bufo_map))
        print(f"wow. {len(bufo_map)} bufos? that's...kind of a lot")
        time.sleep(1.5)
        print("but ok, I guess.")
        time.sleep(1.5)
        print(f"bufo data successfully written to {self._filename}.")
        time.sleep(1.5)
        print("thanks for your help though! don't forget to upload your bufoset")


def main():
    user_token = None
    session_token = None

    if os.path.isfile("creds.yaml"):
        with open("creds.yaml") as f:
            creds = yaml.safe_load(f)
            slack_workspace = creds.get("slack_workspace")
            user_token = creds.get("user_token")
            session_token = creds.get("session_token")
    else:
        slack_workspace = input(
            "Enter your slack workspace (the part before '.slack.com'): "
        )
        user_token = input("Enter your Slack user token (xoxc-...): ")
        session_token = input("Enter your Slack session token (xoxd-...): ")

    analyzer = BufoAnalyzer(slack_workspace, user_token, session_token)
    analyzer.run()


if __name__ == "__main__":
    main()
