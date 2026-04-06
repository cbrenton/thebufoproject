# How
## Running
Run this with `uv run ./extract.py`.

## Authenticating
In order to use this script, you need to get your Slack user token and session token.

To get your tokens:
  1. Go to your organization's "add emoji" page and open the developer console, and click on the "network" tab. In the "filter URLs" box, put "emoji.adminList", then reload the page
  2. There should be one request visible. Click it, then under cookies -> request cookies, you will see a line that says `d: xoxd-...` - right click and do "copy value". That's your session token.
  3. With the same request selected, click "request" (right next to previously selected "cookies"). In "request payload", there will be a line starting with `xoxc-`. That entire line is your user token.

The prompt will ask for your slack workspace name. On the same emoji upload page, the url will take the form `https://<something>.slack.com/customize/emoji` - that `something` is your workspace name.

You can either paste these into the prompt, or bypass the prompt by creating `creds.yaml` that looks like this:
```
slack_workspace: something
user_token: xoxc-some-gibberish
session_token: xoxd-some-gibberish
```

# What
## What data does this script output?
This outputs a json file, which maps bufo names to uploader ids and creation time.

With the --super-secure-flag, bufo names are pseudoanonymized - they're hashed and truncated - to do our best to obfuscate emoji names. You might not want to risk someone leaking the existence of, for example, a project called xkeyscore by uploading :bufo-is-angry-at-xkeyscore: to our database. Be aware that a malicious attacker could in theory brute-force every possible emoji name, though it would take a few billion years.

We also pseudoanonymize Slack user ids, just to be safe.

When you specify -i/--download-images, we will also download your full bufoset locally. This can be useful for helping us compile the world's fullest bufoset, though it's not our primary goal with this project.

Every bufo/emoji scraper script I've seen in the wild has not been this cautious - they all just scrape everything. I just wanted to be a bit more careful.

## What are you doing with the data?
We're attempting to model the spread of bufos via epidemiological methods, and hopefully get a better idea of where Bufo exists, and where he came from.

We want hashed user ids so that we can determine things like: "Some user uploaded 1150 bufos at Square between June 10th and 11th 2021, this was probably the initial bufo dump."

We want hashed bufo names and created_ats so that we can determine things like: "The initial bufo dump at Square on June 11th 2021 contained bufos [x, y, z]. The Stripe bufoset contained bufos [x, y, z] as of January 1st 2021. Therefore, it's reasonable to assume that the Square lineage originated from the Stripe lineage, deviating on June 11th 2021."

## Was this vibe coded?
I wrote this by hand, the old fashioned way, the same way that I create bufos. There is no joy and no love in letting a robot do your silly work.

## Can I trust this?
I wouldn't trust any script I didn't understand myself - please read through it before running it. Feel free to open issues if you have questions or concerns.

# Why?
We just love Bufo.
