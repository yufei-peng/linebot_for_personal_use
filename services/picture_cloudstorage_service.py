import os
import requests
import urllib3

from linebot import LineBotApi
from google.cloud import storage
from google.auth.credentials import AnonymousCredentials

from daos.user_firestore_dao import UserFirestoreDao

'''
處理 MessageEvent 中的 ImageMessage
提供兩個功能：
1. 將使用者傳來的 image 存在本地 image 資料夾，並將其檔案連結存入該使用者資料庫中
2. 透過 user_id 拿到該使用者傳送過的所有 image
'''
class PictureCloudstorageService:

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
    def save_picture_to_cloudstorage(cls, event):

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

        user = UserFirestoreDao.get_user(user_id)
        if user.image_files is None:
            user.image_files = []
            user.image_files.append(destination_blob_name)
        else:
            user.image_files.append(destination_blob_name)
        UserFirestoreDao.update_user(user)

        return "OK"
