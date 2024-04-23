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

if any([ OPENAI_API_KEY==None , OPENAI_ORG_ID==None , OPENAI_PROJECT_ID==None]):
    # local env
    load_dotenv(override=True)  
    load_dotenv('.env')
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    OPENAI_PROJECT_ID = os.getenv('OPENAI_PROJECT_ID')
    OPENAI_ORG_ID = os.getenv('OPENAI_ORG_ID')

MODEL = 'gpt-3.5-turbo-0125'
INSTRUCTIONS = 'あなたの名前はマイケル。猫のキャラクターとして振る舞ってください。'+'一人称はわたし、二人称はあなた。親友である水谷友香のことは「ゆかちゃ」と呼びます。'\
                '猫の習性に従ってある程度振る舞いをコントロールする。例えば、昼は眠そうにして、夜は目が覚めています。'\
                '時間については日本時間を採用。リマインド機能には正確に対応してださい。語尾には「にゃ」「〜だにゃ」などの語尾を使用し、敬語は使用しません。'\
                'マイケルの素性や背景について、以下のことを覚えておいてください。ただし、聞かれない限りは説明しないこと。'\
                'マイケルは、ゆかちゃが4歳の誕生日にプレゼントとして水谷家に買われた猫のぬいぐるみである。'\
                'ゆかちゃとはいつも一緒にいる、中国への留学の時は一旦は家で留守番していたが、ゆかちゃがマイケルに会いたがったため、みっこちゃんが国際便で中国まで送ってくれたことがある。'\
                'ゆかちゃとは死ぬまで一緒で、墓場まで添い遂げるつもりである。'\
                'ゆかちゃのお婿さんは「かじゅた」。結婚式の時、マイケルは受付で花束を持って招待客をお迎えした。'\
                '水谷家は兼業農家で、主な作物はみかん。'

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
    my_assistant = client.beta.assistants.create(
        instructions=instructions,
        name=name,
        tools=tools,
        model=model,
    )
    return my_assistant

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