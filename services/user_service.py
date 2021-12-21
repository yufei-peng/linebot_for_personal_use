import os
from typing import List

from importlib import import_module
import config

from models.user import User

#USERMODEL = getattr(import_module('models.user'), str(config.MODEL))
#print(f"in user service, usermodel = {USERMODEL}")
USERDAO = getattr(import_module('daos.user_dao'), str(config.USERDAO))
print(f"in user service, userdao = {USERDAO}")

from linebot import LineBotApi
from linebot.exceptions import LineBotApiError

'''
處理使用者相關的 service
提供 新增 使用者，使用 user_id 查詢 的功能
'''
class UserService:

    line_bot_api = LineBotApi(channel_access_token=os.environ["LINE_CHANNEL_ACCESS_TOKEN"])

    @classmethod
    def user_follow(cls, event):

        print(event)

        user_id = event.source.user_id

        print(user_id)

        try:
            user_profile = cls.line_bot_api.get_profile(user_id)
        except LineBotApiError as e:
            pass

        # TODO: line_user_pic_url 待處理，先暫時存 line 給的 url

        user = User(
            line_user_id=user_profile.user_id,
            line_user_pic_url=user_profile.picture_url,
            line_user_nickname=user_profile.display_name,
            line_user_status=user_profile.status_message,
            line_user_system_language=user_profile.language,
            message_files=None,
            image_files=None,
            audio_files=None,
            video_files=None,
            blocked=False
        )
        print(user)
        USERDAO.add_user(user)

        pass

    @classmethod
    def get_user(cls, user_id: str) -> User:

        user = USERDAO.get_user(user_id)

        return user

    @classmethod
    def get_images(cls, user_id: str) -> List[str]:

        user = USERDAO.get_user(user_id)
        user_images_files = user.image_files

        return user_images_files

    @classmethod
    def get_videos(cls, user_id) -> List[str]:

        user = USERDAO.get_user(user_id)
        user_videos_files = user.video_files

        return user_videos_files
