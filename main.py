from util import json
from flask import Flask
 
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)
import os

from scraping import wagatomo_scrape

app = Flask(__name__)
 
#環境変数取得
# LINE Developersで設定されているアクセストークンとChannel Secretをを取得し、設定します。
with open('line_setting.json','r') as f:
    line_setting = json.load(f)

print(line_setting)
CHANNEL_ACCESS_TOKEN = line_setting.get('channel_access_token')
DEVELOPER_USER_ID = line_setting.get('developer_user_id')

line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)

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
 
if __name__ == "__main__":
#    app.run()
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)