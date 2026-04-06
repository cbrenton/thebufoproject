#!/usr/bin/env python

import argparse
import os

import yaml

from bufo_analyzer import BufoAnalyzer
from slack_client import SlackClient


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

    parser = argparse.ArgumentParser(
        prog="Bufo extractor",
        description="Query Slack for information about your org's bufos",
    )
    parser.add_argument(
        "-s",
        "--super-secure-mode",
        action="store_true",
        help="only store hashes of bufo names",
    )
    parser.add_argument(
        "-i", "--download-images", action="store_true", help="download the bufos too"
    )
    args = parser.parse_args()

    sc = SlackClient(slack_workspace, user_token, session_token)

    analyzer = BufoAnalyzer(sc, args.super_secure_mode, args.download_images)
    analyzer.run()


if __name__ == "__main__":
    main()
