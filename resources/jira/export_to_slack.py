import os

from slackSDK import SlackSDK

channel_id = os.environ.get("SLACK_CHANNEL_ID", "")
app_token = os.environ.get("SLACK_BOT_TOKEN", "")

slack_sdk = SlackSDK(app_token, channel_id)
slack_sdk.send_file(("days_in_sprint.png", "Daily `Tickets in Sprint` update")
