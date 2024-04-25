

from lib import json , os , re
from flask import Flask , request ,abort
 
# Line SDK ---------------------
from lib import (
    LineBotApi, WebhookHandler
)
from lib import (
    InvalidSignatureError
)
from lib import (
    MessageEvent, TextMessage, TextSendMessage,FollowEvent,UnfollowEvent
    
)

# OpenAi ------------------------
import open_ai as ai

# original ----------------------
from scraping import wagatomo_scrape
from user import User

# main code ---------------------
app = Flask(__name__)
 
#Line instance
CHANNEL_ACCESS_TOKEN = os.getenv("CHANNEL_ACCESS_TOKEN")
DEVELOPER_USER_ID = os.getenv("DEVELOPER_USER_ID")
CHANNEL_SECRET = os.getenv('CHANNEL_SECRET')

DEVELOPER_KEYWORD = os.getenv('DEVELOPER_KEYWORD')

line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)

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


@handler.add(FollowEvent)
def follow_event_hundler(event:FollowEvent):
    # thread_id
    U = User(user_id=event.source.user_id)
    th = ai.create_empty_thread()
    U.openai_data.thread_id = th.id
    U.update_firestore_doc()
    
    # 自己紹介
    ai.create_thread_message(
        thread_id=th.id,
        role='user',
        content='自己紹介してください'
    )

    # run
    result = ai.create_thread_run(
        thread_id=th.id,
        assistant_id=ai.OPENAI_ASS_ID
    )
    msg = result.data[0].content[0].text.value

    line_bot_api.push_message(
        to=U.id,
        messages=TextSendMessage(text=msg)
    )

@handler.add(UnfollowEvent)
def unfollow_event_hundler(event:UnfollowEvent):
    U = User(user_id=event.source.user_id)
    del_res = ai.delete_thread(thread_id=U.openai_data.thread_id)
    U.openai_data.thread_id = None
    U.update_firestore_doc()
    print(del_res)


@handler.add(MessageEvent,message=TextMessage)
def text_message_handler(event:MessageEvent):

    rgex = re.compile(DEVELOPER_KEYWORD+'*')
    mt = rgex.match(event.message.text)
    if mt is not None:
        spl = event.message.text.split(':')
        ass = ai.get_assistant(assistant_id=ai.OPENAI_ASS_ID)
        instructions = ass.instructions + spl[1]
        ass_upd = ai.update_assistant(assistant_id=ass.id,name=ass.name,model=ai.MODEL,instructions=instructions,tools=[])
        print(ass_upd)
        line_bot_api.reply_message(
            reply_token=event.reply_token,
            messages=TextSendMessage(text='assistant_instructions:\n' + instructions)
        )
        return 'OK'

    U = User(user_id=event.source.user_id)
    # スレッドの有無を確認
    if U.openai_data.thread_id is None:
        # create thread
        th = ai.create_empty_thread()
        U.openai_data.thread_id = th.id
        # 保存
        U.update_firestore_doc()

    else:
        # 
        th = ai.get_thread(thread_id=U.openai_data.thread_id)

    # メッセージを追加
    ai.create_thread_message(
        U.openai_data.thread_id,
        'user',
        event.message.text
    )

    # run
    result = ai.create_thread_run(
        thread_id=U.openai_data.thread_id,
        assistant_id=ai.OPENAI_ASS_ID
    )
    msg = result.data[0].content[0].text.value

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=msg))
    return 'OK'

 
if __name__ == "__main__":
#    app.run()
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)