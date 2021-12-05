"""
User 的實體
"""


class User(object):

    def __init__(self, line_user_id, line_user_pic_url,  line_user_nickname, line_user_status,
                 line_user_system_language, blocked=False):

        self.line_user_id = line_user_id
        self.line_user_pic_url = line_user_pic_url
        self.line_user_nickname = line_user_nickname
        self.line_user_status = line_user_status
        self.line_user_system_language = line_user_system_language
        self.blocked = blocked
