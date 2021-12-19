import os
from abc import ABC

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
使用 abstract factory 實作 image service
ImageService class 為 abstrct class
PictureCloudstorageService 為 concrete class, 將照片存到 GCP 的 cloud storage 上
PictureFilesystemService 為 concrete class, 將照片存到 本地的資料夾 上

處理 MessageEvent 中的 ImageMessage
提供的功能：
 - 將使用者傳來的 image 存在本地 image 資料夾，並將其檔案連結存入該使用者資料庫中
'''
class ImageService:

    @classmethod
    def save_picture(cls, event):
        raise NotImplementedError


class PictureCloudstorageService(ImageService):

    ''' cloud storage setting for fsouza/fake-gcs-server image
        https://github.com/googleapis/python-storage/issues/102
    '''
    # my_http = requests.Session()
    # my_http.verify = False  # disable SSL validation
    # urllib3.disable_warnings(
    #     urllib3.exceptions.InsecureRequestWarning
    # )  # disable https warnings for https insecure certs
    #
    # client = storage.Client(
    #     credentials=AnonymousCredentials(),
    #     project="certificate-system-20211203",
    #     _http=my_http,
    #     client_options=ClientOptions(api_endpoint="https://fake-gcs-service:4443"),
    # )
    # EXTERNAL_URL = os.getenv("EXTERNAL_URL", "https://fake-gcs-service:4443")
    # PUBLIC_HOST = os.getenv("PUBLIC_HOST", "storage.gcs.fake-gcs-service.nip.io:4443")
    # storage.blob._BASE_UPLOAD_TEMPLATE = f"{EXTERNAL_URL}/upload/storage/v1{{bucket_path}}/o?uploadType="


    line_bot_api = LineBotApi(channel_access_token=os.environ["LINE_CHANNEL_ACCESS_TOKEN"])

    @classmethod
    def save_picture(cls, event):

        print(f"In service: event={event}")

        image_id = event.message.id
        user_id = event.source.user_id

        image_content = cls.line_bot_api.get_message_content(image_id)
        temp_path = f"{image_id}.png"

        with open(temp_path, 'wb') as fwb:
            for chunk in image_content.iter_content():
                fwb.write(chunk)

        # link to oittaa/gcp-storage-emulator
        client = storage.Client(
            credentials=AnonymousCredentials(),
            project="test",
        )

        bucket_name = "test-bucket"
        destination_blob_name = f"images/{user_id}/{image_id}.png"
        bucket = client.bucket(bucket_name)
        print(f"bucket={bucket}")
        blob = bucket.blob(destination_blob_name)
        print(f"blob={blob}")
        blob.upload_from_string("upload-user-image")

        # 移除本地暫存檔
        os.remove(temp_path)

        user = USERDAO.get_user(user_id)
        print(f"in service, user = {user}")
        if user.image_files is None:
            user.image_files = []
            user.image_files.append(destination_blob_name)
        else:
            user.image_files.append(destination_blob_name)
        USERDAO.update_user(user)

        return "OK"


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
        user = USERDAO.get_user(user_id)
        if user.image_files is None:
            user.image_files = []
            user.image_files.append(image_path)
        else:
            user.image_files.append(image_path)
        USERDAO.update_user(user)

        return "OK"
