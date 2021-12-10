from models.user import User

from google.cloud import firestore

'''
User 對 Firestore 的操作
提供 新增、更新、查詢 功能
'''
class UserFirestoreDao:

    db = firestore.Client()
    users_ref = db.collection(u'users')

    # linebot 使用者 都是來自 follow
    # 使用者可能會重複 follow 、 unfollow ，兩者之間重複操作
    # 所以就算是 follow ，也有可能是舊的使用者
    @classmethod
    def add_user(cls, user: User):

        user_ref = cls.users_ref.document(user.line_user_id)
        # user_doc = user_ref.get()

        # if user_doc.exists:
        #     user_ref.update(user.to_dict())
        # else:
        #     user_ref.set(user.to_dict())

        # To “upsert” a document (create if it doesn’t exist, replace completely if it does),
        # leave the merge argument at its default
        # https://googleapis.dev/python/firestore/latest/document.html
        user_ref.set(user.to_dict())

        return "OK"

    @classmethod
    def update_user(cls, user: User):

        line_user = cls.users_ref.document(user.line_user_id)
        line_user.update(user.to_dict())

        return "OK"

    @classmethod
    def get_user(cls, user_id: str) -> User:

        user_doc = cls.users_ref.document(user_id).get()
        if user_doc.exists:
            return User.from_dict(user_doc.to_dict())
        else:
            pass
