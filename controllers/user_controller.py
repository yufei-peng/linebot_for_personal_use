from services.picture_filesystem_service import PictureFilesystemService
from services.video_filesystem_service import VideoFilesystemService

'''
處理所有 User 相關的 request
'''
class UserController:

    @classmethod
    def get_user_images(cls, user_id: str):
        result = PictureFilesystemService.get_pic_from_filesystem(user_id)

        return str(result)

    @classmethod
    def get_user_videos(cls, user_id: str):
        result = VideoFilesystemService.get_video_link(user_id)

        return str(result)
