import os

from importlib import import_module
import config

from services.video_service import VideoService
USER_DAO = getattr(import_module('daos.' + config.USER_DAO_PKG), str(config.USER_DAO))

print(f"in image service, userdao = {USER_DAO}")

from linebot import LineBotApi


class VideoFilesystemService(VideoService):

    line_bot_api = LineBotApi(channel_access_token=os.environ["LINE_CHANNEL_ACCESS_TOKEN"])

    @classmethod
    def save_video(cls, event):

        video_id = event.message.id
        user_id = event.source.user_id

        print(f"In Service: video_id={video_id}, user_id={user_id}")

        video_content = cls.line_bot_api.get_message_content(message_id=video_id)

        video_path = f"videos/{user_id}/{video_id}.mp4"

        os.makedirs(os.path.dirname(video_path), exist_ok=True)
        with open(video_path, 'wb') as fwb:
            for chunk in video_content.iter_content():
                fwb.write(chunk)

        user = USER_DAO.get_user(user_id)
        print(f"In Service: old video files={user.video_files}")
        if user.video_files is None:
            user.video_files = []
            user.video_files.append(video_path)
        else:
            user.video_files.append(video_path)
        print(f"In Service: *new* video files={user.video_files}")
        USER_DAO.update_user(user)

        return "OK"
