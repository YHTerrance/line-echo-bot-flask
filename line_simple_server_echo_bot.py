import os
import logging

from flask import Flask, request, abort

from linebot.v3 import WebhookHandler

from linebot.v3.exceptions import InvalidSignatureError

from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    TextMessage,
    ReplyMessageRequest
)

from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent
)

from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

configuration = Configuration(os.getenv('LINE_CHANNEL_ACCESS_TOKEN'))
handler = WebhookHandler(os.getenv('LINE_CHANNEL_SECRET'))

@app.route("/")
def home():
    app.logger.info(request)
    return "Home!"

# Listen to post requests on callback
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
        abort(400)
    return 'OK'


# Handle the request
@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    app.logger.info("Event:", event)

    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        line_bot_api.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[TextMessage(text=event.message.text)]
            )
        )

import os
if __name__ == "__main__":
    app.logger.setLevel(logging.DEBUG)
    app.run(host='0.0.0.0', port=os.getenv('FLASK_PORT', 8080))