## Running
Run this with `uv run ./extract.py`.

## How to authenticate
In order to use this script, you need to get your Slack user token and session token.

To get your tokens:
  1. Go to your organization's "add emoji" page and open the developer console, and click on the "network" tab. In the "filter URLs" box, put "emoji.adminList", then reload the page
  2. There should be one request visible. Click it, then under cookies -> request cookies, you will see a line that says `d: xoxd-...` - right click and do "copy value". That's your session token.
  3. With the same request selected, click "request" (right next to previously selected "cookies"). In "request payload", there will be a line starting with `xoxc-`. That entire line is your user token.

The prompt will ask for your slack workspace name. On the same emoji upload page, the url will take the form `https://<something>.slack.com/customize/emoji` - that `something` is your workspace name.

You can either paste these into the prompt, or bypass the prompt by creating `creds.yaml` that looks like this:
```
workspace: something
user_token: xoxc-some-gibberish
session_token: xoxd-some-gibberish
```
