from lib import (
    OpenAI,
    Thread,
    Message,
    os,
)
# open ai instance
OPEN_AI_KEY = os.getenv('OPEN_AI_KEY')
OPEN_AI_PROJECT_ID = os.getenv('OPEN_AI_PROJECT_ID')
OPEN_AI_ORG_ID = os.getenv('OPEN_AI_ORG_ID')

client = OpenAI(
    api_key=OPEN_AI_KEY,
    organization=OPEN_AI_ORG_ID,
    project=OPEN_AI_PROJECT_ID
)

def get_thread_run(thread_id=None, run_id=None, message_list:list[Message]=None):
    if thread_id is None and message_list is not None:
        thread_run = client.beta.threads.create_and_run(
            messages=message_list
        )
    else:
        thread_run = client.beta.threads.runs.create(
            thread_id=thread_id
        )

        

