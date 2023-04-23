from chat_bot.chat_message import ChatMessage, Role
from chat_bot.memory import Memory
from llm.chat_llm import call_llm
from loguru import logger
from prompt import system_prompt


class APIChatBot:
    def __init__(self, model_name: str = "gpt-4", system_prompt: str = system_prompt.NORMAL_PROMPT):
        self.model_name: str = model_name
        self.memory = Memory(system_prompt, model_name)

    def chat(self, message: str):
        self.memory.add_message(ChatMessage(message, Role.USER))
        try:
            response = call_llm(self.memory.get_prompt_messages(), self.model_name)
        except Exception as e:
            logger.error(e)
            return "发生异常，请尝试重新发送消息或重置会话。如果问题仍未解决，请联系管理员。"
        logger.info(f"chatbot response: {response}")
        self.memory.add_message(ChatMessage(message, Role.ASSISTANT))
        return response

    def _set_system_prompt(self, system_prompt: str):
        self.memory.set_system_prompt(system_prompt)

    def set_character(self, character: str):
        self._set_system_prompt(system_prompt.system_prompt_map[character])
