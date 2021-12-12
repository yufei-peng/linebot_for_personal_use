import os

from services.picture_filesystem_service import PictureFilesystemService
from services.video_filesystem_service import VideoFilesystemService
from services.user_service import UserService

from linebot import (
    LineBotApi
)
from linebot.models import (
    MessageEvent
)

'''
處理所有從 LINEBOT 送過來的 Event
'''
class LineBotController:
    line_bot_api = LineBotApi(channel_access_token=os.environ["LINE_CHANNEL_ACCESS_TOKEN"])

    @classmethod
    def follow_event(cls, event):
        UserService.user_follow(event)
        return 'OK'

    @classmethod
    def handle_image_message(cls, event: MessageEvent):

        result = PictureFilesystemService.save_pic_to_filesystem(event)

        return "Your Image has benn saved to database. Thank you!"

    @classmethod
    def handle_video_message(cls, event: MessageEvent):

        result = VideoFilesystemService.save_video_to_filesystem(event)

        return "Your Video has benn saved to database. Thank you!"
