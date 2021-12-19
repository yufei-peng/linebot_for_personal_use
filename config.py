''' 選擇要使用的 user model，必須搭配 dao 使用
    FirebaseUser -> FirebaseDao 使用
    MysqlUser -> MysqlDao 使用
'''
MODEL: str = 'FirebaseUser'


''' 選擇要使用的 資料庫
    UserFirestoreDao
    UserMysqlDao
'''
USERDAO: str = 'UserFirestoreDao'


''' 選擇 文字訊息 要使用的 存檔地點
    MessageCloudstorageService
    MessageFilesystemService
'''
MESSAGESERVICE: str = 'MessageCloudstorageService'


''' 選擇 照片 要使用的 存檔地點
    PictureCloudstorageService
    PictureFilesystemService
'''
IMAGESERVICE: str = 'PictureCloudstorageService'


''' 選擇 語音檔案 要使用的 存檔地點
    AudioCloudstorageService
    AudioFilesystemService
'''
AUDIOSERVICE: str = 'AudioCloudstorageService'


''' 選擇 影片檔案 要使用的 存檔地點
    VideoCloudstorageService
    VideoFilesystemService
'''
VIDEOSERVICE: str = 'VideoCloudstorageService'
