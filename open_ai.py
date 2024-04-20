from lib import (
    OpenAI,
    os,

)
# open ai instance
OPEN_AI_KEY = os.getenv('OPEN_AI_KEY')
OPEN_AI_PROJECT_ID = os.getenv('OPEN_AI_PROJECT_ID')
OPEN_AI_ORG_ID = os.getenv('OPEN_AI_ORG_ID')

client = OpenAI(
    organization=OPEN_AI_KEY,
    project=OPEN_AI_PROJECT_ID
)