

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
import open_ai as ai

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

    ass_id = 'asst_EkNhmrUyW9ZrEUIBOK3sn48U'
    th_id = 'thread_B2Sa8hANeQrsJnaZCHtyLeOu'

    ai.create_thread_message(
        th_id,
        'user',
        event.message.text
    )
    result = ai.create_thread_run(
        th_id,
        ass_id
    )
    msg = result.data[0].content[0].text.value

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=msg))
    

# open ai funcs
def requestOpenAi():
    pass

 
if __name__ == "__main__":
#    app.run()
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)