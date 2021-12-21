import os

from services.image_service import ImageService
from importlib import import_module
import config

USER_DAO = getattr(import_module('daos.' + config.USER_DAO_PKG), str(config.USER_DAO))

print(f"in image service, userdao = {USER_DAO}")

from linebot import LineBotApi


class PictureFilesystemService(ImageService):

    line_bot_api = LineBotApi(channel_access_token=os.environ["LINE_CHANNEL_ACCESS_TOKEN"])

    @classmethod
    def save_picture(cls, event):

        print(f"messageEvent is {event}")

        image_id = event.message.id

        # 取得 linebot 的媒體內容
        # https://developers.line.biz/en/reference/messaging-api/#get-content
        message_content = cls.line_bot_api.get_message_content(message_id=image_id)

        user_id = event.source.user_id
        image_path = f'images/{user_id}/{image_id}.png'

        # 將檔案存到本地的檔案系統中
        # https://docs.python.org/3.2/library/os.html#os.makedirs
        # 遞迴建立 dir, 如果最終目錄已經存在，會有 OSError ，使用 exist_ok=True 忽略
        os.makedirs(os.path.dirname(image_path), exist_ok=True)
        with open(image_path, 'wb') as fwb:
            for chunk in message_content.iter_content():
                fwb.write(chunk)

        # 將其路徑存到該使用者的資料庫檔案中
        user = USER_DAO.get_user(user_id)
        if user.image_files is None:
            user.image_files = []
            user.image_files.append(image_path)
        else:
            user.image_files.append(image_path)
        USER_DAO.update_user(user)

        return "OK"
