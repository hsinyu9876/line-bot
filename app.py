from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
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
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()