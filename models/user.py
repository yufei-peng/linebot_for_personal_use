from __future__ import annotations

"""
User 的實體
提供 from_dict 和 to_dict 方便快速轉換
提供 __repr__ 打印參數
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

    @staticmethod
    def from_dict(user: dict) -> User:
        user = User(
            line_user_id=user.get(u'line_user_id'),
            line_user_pic_url=user.get(u'line_user_pic_url'),
            line_user_nickname=user.get(u'line_user_nickname'),
            line_user_status=user.get(u'line_user_status'),
            line_user_system_language=user.get(u'line_user_system_language'),
            blocked=user.get(u'blocked')
        )
        return user

    def to_dict(self):
        user_dict = {
            "line_user_id": self.line_user_id,
            "line_user_pic_url": self.line_user_pic_url,
            "line_user_nickname": self.line_user_nickname,
            "line_user_status": self.line_user_status,
            "line_user_system_language": self.line_user_system_language,
            "blocked": self.blocked
        }
        return user_dict

    def __repr__(self):
        return (f'''User(
            line_user_id={self.line_user_id},
            line_user_pic_url={self.line_user_pic_url},
            line_user_nickname={self.line_user_nickname},
            line_user_status={self.line_user_status},
            line_user_system_language={self.line_user_system_language},
            blocked={self.blocked}
        )''')
