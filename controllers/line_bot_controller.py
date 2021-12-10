from linebot import (
    LineBotApi
)
from linebot.models import (
    TextSendMessage
)

import os


class LineBotController:
    line_bot_api = LineBotApi(channel_access_token=os.environ["LINE_CHANNEL_ACCESS_TOKEN"])

    @classmethod
    def follow_event(cls, event):
        print("---")
        print(event)
        print("***")

        line_user_profile = cls.line_bot_api.get_profile(event.source.user_id)
        cls.line_bot_api.reply_message(event.reply_token, TextSendMessage("test"))
        # user_dict = {
        #     "line_user_id": line_user_profile.user_id,
        #     "line_user_pic_url": line_user_profile.picture_url,
        #     "line_user_nickname": line_user_profile.display_name,
        #     "line_user_status": line_user_profile.status_message,
        #     "line_user_system_language": line_user_profile.language,
        #     "blocked": False
        # }
        # return user_dict
        return 'OK'
