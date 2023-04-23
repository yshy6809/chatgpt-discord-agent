import os
from datetime import date

import openai

from disc.client import *
from loguru import logger
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv('OPEN_AI_API_KEY')
openai.api_base = os.getenv('OPEN_AI_BASE_URL')

logger.add(f'{date.today()}.log', rotation='1 day', level='INFO')

client.run(os.getenv('DISCORD_BOT_TOKEN'))

