import json
import re
import os
from dotenv import load_dotenv

# Line SDK ---------------------
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

# OpenAi ------------------------
from openai import OpenAI
from openai.types import ErrorObject, FunctionDefinition, FunctionParameters
from openai.types.beta import (
    Assistant,
    AssistantDeleted,
    AssistantStreamEvent,
    AssistantTool,
    
    Thread,
    ThreadCreateParams,
    ThreadUpdateParams,
    ThreadDeleted,
    ThreadCreateAndRunParams,
    AssistantResponseFormat,
    AssistantResponseFormatOption,
    AssistantToolChoice,
    AssistantToolChoiceFunction,
    AssistantToolChoiceOption,
)
from openai.types.beta.threads import (
    RequiredActionFunctionToolCall,
    Message,
    MessageContent,
)
