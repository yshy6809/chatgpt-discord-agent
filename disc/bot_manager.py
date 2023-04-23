from collections import defaultdict

from chat_bot.api_chat_bot import APIChatBot
from chat_bot.web_chat_bot import WebChatBot


class BotManager:
    def __init__(self):
        self.api_bot_map = defaultdict(APIChatBot)
        self.web_bot_map = defaultdict(WebChatBot)
        self.mode_map = defaultdict(lambda: "api")

    def ask_web(self, message: str, session_id: str):
        return self.web_bot_map[session_id].chat(message)

    def ask_api(self, message: str, session_id: str):
        return self.api_bot_map[session_id].chat(message)

    def set_mode(self, mode: str, session_id: str):
        self.mode_map[session_id] = mode

    def set_character(self, character: str, session_id: str):
        self.api_bot_map[session_id].set_character(character)

    def ask(self, message: str, session_id: str):
        mode = self.mode_map[session_id]
        if mode == "api":
            return self.ask_api(message, session_id)
        elif mode == "web":
            return self.ask_web(message, session_id)
        else:
            raise NotImplementedError(f"mode {mode} not implemented")


bot_manager: BotManager = BotManager()
