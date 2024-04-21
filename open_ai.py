from lib import (
    OpenAI,
    Thread,
    Message,
    os,load_dotenv
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

MODEL = 'gpt-3.5-turbo'

client = OpenAI()

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

