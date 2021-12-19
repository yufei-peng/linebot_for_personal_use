from services.user_service import UserService

'''
處理所有 User 相關的 request
'''
class UserController:

    @classmethod
    def get_user_images(cls, user_id: str):
        result = UserService.get_images(user_id)

        return str(result)

    @classmethod
    def get_user_videos(cls, user_id: str):
        result = UserService.get_videos(user_id)

        return str(result)
