import os
from loguru import logger

from revChatGPT.V1 import Chatbot


class WebChatBot:
    def __init__(self):
        self.web_chat_bot = Chatbot(
            config={"access_token": os.getenv("SESSION_TOKEN"), "model": "gpt-3.5-turbo", "paid": True})

    def chat(self, message):
        try:
            res = ""
            for d in self.web_chat_bot.ask(message):
                if "message" in d:
                    res = d["message"]
            return res
        except Exception as e:
            logger.error(e)
            return "发生异常，请尝试重新发送消息或重置会话。如果问题仍未解决，请联系管理员。"
