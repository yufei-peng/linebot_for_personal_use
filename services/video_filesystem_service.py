import os
from typing import List

from daos.user_firestore_dao import UserFirestoreDao

from linebot import LineBotApi


'''
處理 MessageEvent 中的 VideoMessage
提供兩個功能：
1. 將使用者傳來的 video 存在本地 Video 資料夾，並將其檔案連結存入該使用者資料庫中
2. 透過 user_id 拿到該使用者傳送過的所有 video
'''
class VideoFilesystemService:

    line_bot_api = LineBotApi(channel_access_token=os.environ["LINE_CHANNEL_ACCESS_TOKEN"])

    @classmethod
    def save_video_to_filesystem(cls, event):

        video_id = event.message.id
        user_id = event.source.user_id

        print(f"In Service: video_id={video_id}, user_id={user_id}")

        video_content = cls.line_bot_api.get_message_content(message_id=video_id)

        video_path = f"videos/{user_id}/{video_id}.mp4"

        os.makedirs(os.path.dirname(video_path), exist_ok=True)
        with open(video_path, 'wb') as fwb:
            for chunk in video_content.iter_content():
                fwb.write(chunk)

        user = UserFirestoreDao.get_user(user_id)
        print(f"In Service: old video files={user.video_files}")
        if user.video_files is None:
            user.video_files = []
            user.video_files.append(video_path)
        else:
            user.video_files.append(video_path)
        print(f"In Service: *new* video files={user.video_files}")
        UserFirestoreDao.update_user(user)

        return "OK"

