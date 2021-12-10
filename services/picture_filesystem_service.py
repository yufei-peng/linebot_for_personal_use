import os

from linebot import (
    LineBotApi
)
from linebot.models import (
    MessageEvent, ImageMessage
)

'''
提供兩個服務
1. 將照片存到本地的檔案夾內
2. 從本地檔案夾拿照片
'''
class PictureFilesystemService:

    line_bot_api = LineBotApi(channel_access_token=os.environ["LINE_CHANNEL_ACCESS_TOKEN"])

    @classmethod
    def save_pic_to_filesystem(cls, message_event: MessageEvent):

        image_id = message_event.message['id']

        # 取得 linebot 的媒體內容
        # https://developers.line.biz/en/reference/messaging-api/#get-content
        message_content = cls.line_bot_api.get_message_content(message_id=image_id)

        user_id = message_event.source['userId']
        image_path = f'./{user_id}/{image_id}.png'

        with open(image_path, 'wb') as fwb:
            fwb.write(message_content.content)



    @classmethod
    def get_pic_from_filesystem(cls):
        pass
