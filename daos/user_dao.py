from models.user import User


'''
使用 abstract factory 實作 UserDao
UserDao class 為 abstrct class
UserFirestoreDao 為 concrete class, 提供對 Firestore 資料庫的操作
UserMysqlDao 為 concrete class, 提供對 Mysql 資料庫的操作

User 對 資料庫 的操作
提供 新增、更新、查詢 功能
'''
class UserDao:

    @classmethod
    def add_user(cls, user: User):
        raise NotImplementedError

    @classmethod
    def update_user(cls, user: User):
        raise NotImplementedError

    @classmethod
    def get_user(cls, user_id: str) -> User:
        raise NotImplementedError
