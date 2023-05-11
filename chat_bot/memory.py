from typing import List
from chat_bot.chat_message import ChatMessage, Role
from llm.chat_llm import num_tokens_from_messages


class Memory:
    def __init__(self, system_message: str, model_name: str, memory_buffer_size: int = 2048):
        self.chat_history: List[ChatMessage] = []
        self.memory_buffer: List[ChatMessage] = []
        self.model_name: str = model_name
        self.memory_buffer_size: int = memory_buffer_size
        self.system_message: ChatMessage = ChatMessage(system_message, Role.SYSTEM)

    def add_message(self, message: ChatMessage):
        self.chat_history.append(message)
        self.memory_buffer.append(message)
        while self.count_mem_buffer_tokens() > self.memory_buffer_size:
            self.memory_buffer.pop(0)

    def count_mem_buffer_tokens(self):
        return num_tokens_from_messages(self.get_prompt_messages(), model=self.model_name)

    def get_prompt_messages(self)->List[dict]:
        return [self.system_message.to_dict()] + [msg.to_dict() for msg in self.memory_buffer]

    def set_system_prompt(self, system_prompt: str):
        self.system_message = ChatMessage(system_prompt, Role.SYSTEM)

    def reset(self):
        self.memory_buffer = []
