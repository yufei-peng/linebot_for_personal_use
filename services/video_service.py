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
