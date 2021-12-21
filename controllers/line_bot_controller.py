import os

from services.user_service import UserService
from importlib import import_module
import config

IMAGE_SERVICE = getattr(import_module('services.' + config.IMAGE_SERVICE_PKG), str(config.IMAGE_SERVICE))
VIDEO_SERVICE = getattr(import_module('services.' + config.VIDEO_SERVICE_PKG), str(config.VIDEO_SERVICE))
print(f"in line bot controller, image service = {IMAGE_SERVICE}, and video service = {VIDEO_SERVICE}")

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

        result = IMAGE_SERVICE.save_picture(event)

        return "Your Image has benn saved to database. Thank you!"

    @classmethod
    def handle_video_message(cls, event: MessageEvent):

        result = VIDEO_SERVICE.save_video(event)

        return "Your Video has benn saved to database. Thank you!"
