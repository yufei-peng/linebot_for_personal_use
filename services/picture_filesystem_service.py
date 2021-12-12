import os

from daos.user_firestore_dao import UserFirestoreDao

from linebot import (
    LineBotApi
)
from linebot.models import (
    MessageEvent
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

        print(f"messageEvent is {message_event}")

        image_id = message_event.message.id

        # 取得 linebot 的媒體內容
        # https://developers.line.biz/en/reference/messaging-api/#get-content
        message_content = cls.line_bot_api.get_message_content(message_id=image_id)

        user_id = message_event.source.user_id
        image_path = f'images/{user_id}/{image_id}.png'

        # 將檔案存到本地的檔案系統中
        # https://docs.python.org/3.2/library/os.html#os.makedirs
        # 遞迴建立 dir, 如果最終目錄已經存在，會有 OSError ，使用 exist_ok=True 忽略
        os.makedirs(os.path.dirname(image_path), exist_ok=True)
        with open(image_path, 'wb') as fwb:
            for chunk in message_content.iter_content():
                fwb.write(chunk)

        # 將其路徑存到該使用者的資料庫檔案中
        user = UserFirestoreDao.get_user(user_id)
        if user.image_files is None:
            user.image_files = []
            user.image_files.append(image_path)
        else:
            user.image_files.append(image_path)
        UserFirestoreDao.update_user(user)

        return "OK"
