"""
LINEBOT 的入口
LINE 會將所有的 Event 送進 `/callback`
收到 POST request 之後，利用 channel_access_token 和 channel_secret 檢查 signature
確認 request 來自 LINE
之後依照各個 Event 轉發
"""
import os
from flask import Flask, request, abort
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from controllers.line_bot_controller import LineBotController
from controllers.user_controller import UserController

line_bot_api = LineBotApi(channel_access_token=os.environ["LINE_CHANNEL_ACCESS_TOKEN"])
handler = WebhookHandler(channel_secret=os.environ["LINE_CHANNEL_SECRET"])

# 載入Follow事件
from linebot.models.events import (
    FollowEvent,UnfollowEvent,MessageEvent,TextMessage,PostbackEvent,ImageMessage,AudioMessage,VideoMessage
)

@app.route('/test')
def hello_world():
    return 'Hello World!'


'''
轉發功能列表
'''
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    print(body)
    app.logger.debug('request body is: %s', body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(FollowEvent)
def handle_line_follow(event):
    return LineBotController.follow_event(event)


@handler.add(MessageEvent, ImageMessage)
def handle_image(event):
    return LineBotController.handle_image_message(event)


@handler.add(MessageEvent, VideoMessage)
def handle_video(event):
    return LineBotController.handle_video_message(event)


@app.route('/v1/pics/<user_id>', methods=['GET'])
def get_user_images(user_id):
    return UserController.get_user_images(user_id)


@app.route('/v1/videos/<user_id>', methods=['GET'])
def get_user_videos(user_id):
    return UserController.get_user_videos(user_id)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
