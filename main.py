

from lib import json , os
from flask import Flask , request ,abort
 
# Line SDK ---------------------
from lib import (
    LineBotApi, WebhookHandler
)
from lib import (
    InvalidSignatureError
)
from lib import (
    MessageEvent, TextMessage, TextSendMessage,
)

# OpenAi ------------------------
from lib import OpenAI

# original ----------------------
from scraping import wagatomo_scrape




# main code ---------------------
app = Flask(__name__)
 
#Line instance
CHANNEL_ACCESS_TOKEN = os.getenv("CHANNEL_ACCESS_TOKEN")
DEVELOPER_USER_ID = os.getenv("DEVELOPER_USER_ID")
CHANNEL_SECRET = os.getenv('CHANNEL_SECRET')

line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)

# open ai instance
OPEN_AI_KEY = os.getenv('OPEN_AI_KEY')
OPEN_AI_PROJECT_ID = os.getenv('OPEN_AI_PROJECT_ID')

OpenAI(
    organization=OPEN_AI_KEY,
    project=OPEN_AI_PROJECT_ID
)


@app.get(rule='/')
def tester():
    return 'OK'

@app.route(rule='/push_wagatomo',methods=['GET'])
def push_wagatomo():
    wagatomo = wagatomo_scrape()
    line_bot_api.push_message(
        to=DEVELOPER_USER_ID,
        messages=TextSendMessage(
            text=wagatomo,
        )
    )
    return 'OK'

@app.post(rule='/say_michael')
def say_michael():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    print("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'

@handler.add(MessageEvent,message=TextMessage)
def text_message_handler(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))
    

# open ai funcs
def requestOpenAi():
    pass

 
if __name__ == "__main__":
#    app.run()
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)