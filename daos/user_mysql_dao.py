import pymysql

from models.user import User
from daos.user_dao import UserDao


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
