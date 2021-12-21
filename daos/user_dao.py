from importlib import import_module
import config
import pymysql

#USERMODEL = getattr(import_module('models.user'), str(config.MODEL))
from models.user import User
#print(f"in dao, usermodel = {USERMODEL}")

from google.cloud import firestore

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


class UserMySQLDao(UserDao):
    """
    實作 User 對於 MySQL 資料庫的 DAO 類
    """
    db = pymysql.connect(host='mysql', user='root', password='rootdevpassword', db='demo', charset='utf8mb4',
                         cursorclass=pymysql.cursors.DictCursor)

    schema = """
    CREATE TABLE User (
    line_user_id VARCHAR(255) NOT NULL UNIQUE,
    line_user_pic_url VARCHAR(255),
    line_user_nickname VARCHAR(255),
    line_user_status VARCHAR(255),
    line_user_system_language VARCHAR(255),
    message_files VARCHAR(255),
    image_files VARCHAR(255),
    audio_files VARCHAR(255),
    video_files VARCHAR(255),
    blocked VARCHAR(30) NOT NULL
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8
    """

    # Table 初始化
    try:
        with db.cursor() as cursor:
            cursor.execute(schema)
        print("Create User table")
    except pymysql.Error as e:
        print("Table has been created , error_message -> " + str(e))

    # Check db connection
    db.ping(reconnect=True)
    cursor = db.cursor()

    @classmethod
    def add_user(cls, user: User):
        sql = f"""
        INSERT INTO User (line_user_id, line_user_pic_url, line_user_nickname, line_user_status, line_user_system_language, message_files, image_files, audio_files, video_files, blocked)
        VALUE ('{user.line_user_id}','{user.line_user_pic_url}','{user.line_user_nickname}','{user.line_user_status}','{user.line_user_system_language}','{user.message_files}','{user.image_files}',
        '{user.audio_files}','{user.video_files}','{user.blocked}')
        """
        try:
            cls.cursor.execute(sql)
            cls.db.commit()
            return 'OK'
        except pymysql.Error as err:
            print("SQL executed error: " + str(err))

    @classmethod
    def update_user(cls, user: User):
        sql = f"""
        UPDATE User SET 
        line_user_pic_url = '{user.line_user_pic_url}' , line_user_nickname = '{user.line_user_pic_url}' , line_user_status = '{user.line_user_status}',
        line_user_system_language = '{user.line_user_system_language}', message_files = '{user.message_files}' , image_files = '{user.image_files}',
        audio_files = '{user.audio_files}', video_files = '{user.video_files}' WHERE line_user_id = '{user.line_user_id}'
        """
        try:
            cls.cursor.execute(sql)
            cls.db.commit()
            return 'OK'
        except pymysql.Error as err:
            print("SQL executed error: " + str(err))

    @classmethod
    def get_user(cls, user_id: str) -> User:
        sql = f"""
        SELECT * FROM User WHERE line_user_id = '{user_id}'
        """
        try:
            user_dict = cls.cursor.execute(sql)
            user = User.from_dict(user_dict)
            return user
        except pymysql.Error as err:
            print("SQL executed error: " + str(err))