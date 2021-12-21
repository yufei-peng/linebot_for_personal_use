''' 選擇要使用的 資料庫
    package:
        user_firestore_dao
        user_mysql_dao
    class:
        UserFirestoreDao
        UserMysqlDao
'''
# USER_DAO_PKG: str = 'user_firestore_dao'
# USER_DAO: str = 'UserFirestoreDao'
USER_DAO: str = 'UserMySQLDao'
USER_DAO_PKG: str = 'user_mysql_dao'

''' 選擇 文字訊息 要使用的 存檔地點
    package:
        message_cloudstorage_service
        message_filesystem_service
    class:
        MessageCloudstorageService
        MessageFilesystemService
'''
MESSAGE_SERVICE_PKG: str = 'message_cloudstorage_service'
MESSAGE_SERVICE: str = 'MessageCloudstorageService'


''' 選擇 照片 要使用的 存檔地點
    package:
        image_cloudstorage_service
        image_filesystem_service
    class:
        PictureCloudstorageService
        PictureFilesystemService
'''
IMAGE_SERVICE_PKG: str = 'image_cloudstorage_service'
IMAGE_SERVICE: str = 'PictureCloudstorageService'


''' 選擇 語音檔案 要使用的 存檔地點
    package:
        audio_cloudstorage_service
        audio__filesystem_service
    class:
        AudioCloudstorageService
        AudioFilesystemService
'''
AUDIO_SERVICE_PKG: str = 'audio_cloudstorage_service'
AUDIO_SERVICE: str = 'AudioCloudstorageService'


''' 選擇 影片檔案 要使用的 存檔地點
    package:
        video_cloudstorage_service
        video_filesystem_service
    class:
        VideoCloudstorageService
        VideoFilesystemService
'''
VIDEO_SERVICE_PKG: str = 'video_filesystem_service'
VIDEO_SERVICE: str = 'VideoFilesystemService'
