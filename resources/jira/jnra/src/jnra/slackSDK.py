from slack_sdk import WebClient


class SlackSDK:

    def __init__(self, bot_token: str, channel_id: str) -> None:
        self._client = WebClient(bot_token)
        self._channel_id = channel_id

    def send_file(self, file_name: str, message: str) -> None:
        print(f"Sending to slack '{file_name}'")

        self._client.files_upload(
            channels=self._channel_id,
            initial_comment=message,
            file=file_name,
        )
