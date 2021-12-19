import os

import requests
import urllib3

from importlib import import_module
import config

USERDAO = getattr(import_module('daos.user_dao'), str(config.USERDAO))

print(f"in image service, userdao = {USERDAO}")

from linebot import LineBotApi
from google.cloud import storage
from google.auth.credentials import AnonymousCredentials

'''
使用 abstract factory 實作 video service
VideoService class 為 abstract class
VideoCloudstorageService 為 concrete class, 將照片存到 GCP 的 cloud storage 上
VideoFilesystemService 為 concrete class, 將照片存到 本地的資料夾 上

處理 MessageEvent 中的 ImageMessage
提供的功能：
 - 將使用者傳來的 image 存在本地 image 資料夾，並將其檔案連結存入該使用者資料庫中
'''
class VideoService:

    @classmethod
    def save_video(cls, event):
        raise NotImplementedError


class VideoFilesystemService(VideoService):

    line_bot_api = LineBotApi(channel_access_token=os.environ["LINE_CHANNEL_ACCESS_TOKEN"])

    @classmethod
    def save_video(cls, event):

        video_id = event.message.id
        user_id = event.source.user_id

        print(f"In Service: video_id={video_id}, user_id={user_id}")

        video_content = cls.line_bot_api.get_message_content(message_id=video_id)

        video_path = f"videos/{user_id}/{video_id}.mp4"

        os.makedirs(os.path.dirname(video_path), exist_ok=True)
        with open(video_path, 'wb') as fwb:
            for chunk in video_content.iter_content():
                fwb.write(chunk)

        user = USERDAO.get_user(user_id)
        print(f"In Service: old video files={user.video_files}")
        if user.video_files is None:
            user.video_files = []
            user.video_files.append(video_path)
        else:
            user.video_files.append(video_path)
        print(f"In Service: *new* video files={user.video_files}")
        USERDAO.update_user(user)

        return "OK"
