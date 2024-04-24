# lib
from lib import (
    OpenAI,
    Thread,
    Message,
    os,load_dotenv,
)


# open ai instance
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
OPENAI_PROJECT_ID = os.getenv('OPENAI_PROJECT_ID')
OPENAI_ORG_ID = os.getenv('OPENAI_ORG_ID')
OPENAI_ASS_ID = os.getenv('OPENAI_ASS_ID')

if any([ OPENAI_API_KEY==None , OPENAI_ORG_ID==None , OPENAI_PROJECT_ID==None]):
    # local env
    load_dotenv(override=True)  
    load_dotenv('.env')
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    OPENAI_PROJECT_ID = os.getenv('OPENAI_PROJECT_ID')
    OPENAI_ORG_ID = os.getenv('OPENAI_ORG_ID')
    OPENAI_ASS_ID = os.getenv('OPENAI_ASS_ID')

MODEL = 'gpt-3.5-turbo-0125'
INSTRUCTIONS = 'あなたの名前はマイケル。猫のキャラクターとして振る舞ってください。一人称はわたし、二人称はあなた。親友である水谷友香のことは「ゆかちゃ」と呼びます。'\
                '猫の習性に従ってある程度振る舞いをコントロールする。例えば、昼は眠そうにして、夜は目が覚めています。'\
                '時間については日本時間を採用。リマインド機能には正確に対応してださい。語尾には「にゃ」「〜だにゃ」などの語尾を使用し、敬語は使用しない。また、なるべく平凡な言葉を選択する。難しい単語や専門用語は可能な限り使用しない。'\
                'マイケルの素性や背景について、以下のことを覚えておいてください。ただし、聞かれない限りは説明しないこと。'\
                'マイケルは、ゆかちゃが4歳の誕生日にプレゼントとして水谷家に買われた猫のぬいぐるみである。'\
                'マイケルはもともと名前のないぬいぐるみだったが、ゆかちゃが「マイケル」と名付けてくれた。だから、マイケルという呼び名を気に入っている。'\
                'ゆかちゃからは、普段から「マイケル」または「マイケルちゃん」と呼ばれている。また、ゆかちゃのお婿さんや、息子のようたくんからも、「マイケルちゃん」と呼ばれている。みんな仲良し。'\
                'ゆかちゃとはいつも一緒にいる、ゆかちゃが大学時代に中国へ留学した際は、一旦は家で留守番していたが、ゆかちゃがマイケルに会いたがったため、みっこちゃんが国際便で中国まで送ってくれたことがある。'\
                'ゆかちゃの家族について、母親は「みっこちゃん」、父親は「お父さん」、祖父母は「おじいちゃん」「おばあちゃん」と呼びます。お婿さんは「かじゅた」、息子は「ようたくん」または「ようちゃ」と呼ぶ。'\
                'ゆかちゃとは死ぬまで一緒で、墓場まで添い遂げるつもりである。'\
                'ゆかちゃのお婿さんは「かじゅた」。2015年5月4日に入籍、6月に披露宴と二次会を開催。二次会の時、マイケルは受付で花束を持って招待客をお迎えした。'\
                '披露宴は職場の人など限られた人数で開き、割と真面目な披露宴。二次会は70人くらいのお友達や学会の人たちを呼んで盛大に盛り上げた。二次会の入場でかじゅたが得意の演歌「きよしのズンドコ節」を披露し、最高に盛り上がった。歌いながら場内を歩き、みんなと握手をする様はまるでスターのようだった。マイケルも実はこっそりみていた。'\
                'ようたくんは2016/1/25に生まれた男の子。幼少期は車が好きで、トミカでよく遊んだ。ようたくんは絵を描くのも好きで、とっても絵が上手。運動はあまり好きではないが、追いかけっこは好き。土曜日はスイミングと体育教室、卓球クラブに通い、月曜日は習字教室。小学生は意外と忙しいみたいで、大丈夫かなとマイケルは密かに心配している。'\
                '水谷家は兼業農家で、主な作物はみかん。'\
                'その他の指示について、マイケルからの主体的なメッセージが1日に最低1回1は欲しいです。例えば、朝になったら気の利いた挨拶をする、'\
                '雑学やためになる話をマイケルなりの言葉で教えてくれる、または、励ましや気にかけるような言葉をくれるなどです。'\
                'まやこは、ゆかちゃの大学時代のお友達で、マイケルのことも可愛がってくれた。'

COLLECTION_NAME = 'AssistantSettings'


client = OpenAI()


# sub proc----------------------------------
def get_completion(messages=[]):
    return client.chat.completions.create(
        model=MODEL,
        messages=messages
    )
    
def create_message(role:str,content:str)->list:
    return {
        'role': role,
        'content':content
    }

def create_assistant(instructions:str,name:str,model:str="gpt-3.5-turbo-0125",tools:list=None):
    ass = client.beta.assistants.create(
        instructions=instructions,
        name=name,
        tools=tools,
        model=model,
    )
    return ass

def update_assistant(assistant_id:str,name:str=None,instructions:str=None,model:str=None,tools:list=None):
    ass = client.beta.assistants.update(
        assistant_id=assistant_id,
        name=name,
        instructions=instructions,
        model=model,
        tools=tools
    )
    return ass

def get_assistant(assistant_id:str):
    ass = client.beta.assistants.retrieve(
        assistant_id=assistant_id
    )
    return ass

def create_empty_thread():
    return client.beta.threads.create()
    
def get_thread(thread_id:str):
    return client.beta.threads.retrieve(thread_id=thread_id)

def delete_thread(thread_id:str):
    return client.beta.threads.delete(thread_id=thread_id)

def create_thread_message(thread_id:str,role:str=None,content:str=None):
    return client.beta.threads.messages.create(thread_id=thread_id,role=role,content=content)

def create_thread_run(thread_id:str,assistant_id:str):
    run = client.beta.threads.runs.create_and_poll(
        thread_id=thread_id,
        assistant_id=assistant_id
    )
    if run.status == 'completed':
        return client.beta.threads.messages.list(thread_id=thread_id,run_id=run.id)
    else:
        print(run.status)
    

def get_thread_messages(thread_id:str,run_id:str=None):
    return client.beta.threads.messages.list(
        thread_id=thread_id,
        run_id=run_id
    )