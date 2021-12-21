from models.user import User
from daos.user_dao import UserDao

from google.cloud import firestore


class UserFirestoreDao(UserDao):

    db = firestore.Client()
    users_ref = db.collection(u'users')

    # linebot 使用者 都是來自 follow
    # 使用者可能會重複 follow 、 unfollow ，兩者之間重複操作
    # 所以就算是 follow ，也有可能是舊的使用者
    @classmethod
    def add_user(cls, user: User):

        print(f"In dao add -> {user}")

        user_ref = cls.users_ref.document(user.line_user_id)
        print(f"add_user_dao user_ref *** {user_ref}")

        user_doc = user_ref.get()
        if user_doc.exists:
            old_user_data = user_doc.to_dict()
            user.message_files = old_user_data['message_files']
            user.image_files = old_user_data['image_files']
            user.audio_files = old_user_data['audio_files']
            user.video_files = old_user_data['video_files']
            print(f"In DAO, old user unfollow -> user={user}")
            result = user_ref.update(user.to_dict())
        else:
            result = user_ref.set(user.to_dict())

        # To “upsert” a document (create if it doesn’t exist, replace completely if it does),
        # leave the merge argument at its default
        # https://googleapis.dev/python/firestore/latest/document.html
        # result = user_ref.set(user.to_dict())
        # print(f"add_user_dao result *** {result}")

        return "OK"

    @classmethod
    def update_user(cls, user: User):

        print(f"In dao update -> {user}")

        line_user = cls.users_ref.document(user.line_user_id)
        line_user.update(user.to_dict())

        return "OK"

    @classmethod
    def get_user(cls, user_id: str) -> User:

        user_doc = cls.users_ref.document(user_id).get()
        # print(f"in dao, user_doc = {user_doc.to_dict()}")
        if user_doc.exists:
            return User.from_dict(user_doc.to_dict())
        else:
            # print("??????????")
            pass
