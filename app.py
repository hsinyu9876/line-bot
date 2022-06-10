from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, StickerSendMessage
)

app = Flask(__name__)

line_bot_api = LineBotApi('M3RXyKpnMOcFNp+2zahA07vR2o2nMPqgy266ng2Bk15FgLd9hrxKgEuIYE9YUq/0QClkaW7XjuPqnPq41z9CQs5A6RsJouO9QZLNblKmrdEzYFO1TVwJ6XfeL6OUFLOvRm3kTmjiaCUw72bC6qlsKgdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('e2a1be9cabd46acf89d926fe50e7f502')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text
    r = '我看不懂你說什麼'

    if '貼圖' in msg:
        sticker_message = StickerSendMessage(
            package_id='6362',
            sticker_id='11087923'
        )

        line_bot_api.reply_message(
            event.reply_token,
            sticker_message)
        return#不回傳東西的回傳，為了結束function不執行以下if。

    if msg in ['hi', 'Hi']:
        r = '嗨'
    elif msg == '你吃飯了嗎':
        r = '還沒'
    elif msg == '你是誰':
        r = '我是機器人'
    elif '訂位' in msg:
        r = '您想訂位，是嘛?'

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=r))


if __name__ == "__main__":
    app.run()