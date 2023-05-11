from chat_bot.chat_message import ChatMessage, Role
from chat_bot.memory import Memory
from llm.chat_llm import call_llm, num_tokens_from_messages
from loguru import logger
from prompt import system_prompt


class APIChatBot:
    def __init__(self, model_name: str = "gpt-4", system_prompt: str = system_prompt.NORMAL_PROMPT):
        self.model_name: str = model_name
        self.memory = Memory(system_prompt, model_name)

    def chat(self, message: str):
        self.memory.add_message(ChatMessage(message, Role.USER))
        prompt_messages = self.memory.get_prompt_messages()
        try:
            response = call_llm(prompt_messages, self.model_name)
        except Exception as e:
            logger.error(e)
            return "发生异常，请尝试重新发送消息或重置会话。如果问题仍未解决，请联系管理员。", None, None, self.model_name
        logger.info(f"chatbot response: {response}")
        response_message = ChatMessage(message, Role.ASSISTANT)
        self.memory.add_message(response_message)
        prompt_cost = num_tokens_from_messages(prompt_messages, self.model_name)
        complete_cost = num_tokens_from_messages([response_message.to_dict()], self.model_name)
        logger.info(f"prompt_cost: {prompt_cost}, complete_cost: {complete_cost}")
        return response, prompt_cost, complete_cost, self.model_name

    def chat_without_memory(self, message: str):
        prompt_messages =[{"role":"system", "content": system_prompt.NORMAL_PROMPT}] + [ChatMessage(message, Role.USER).to_dict()]
        try:
            response = call_llm(prompt_messages, self.model_name)
        except Exception as e:
            logger.error(e)
            return "发生异常，请尝试重新发送消息或重置会话。如果问题仍未解决，请联系管理员。", None, None, self.model_name
        logger.info(f"chatbot response: {response}")
        prompt_cost = num_tokens_from_messages(prompt_messages, self.model_name)
        complete_cost = num_tokens_from_messages([{"role":"assistant", "content": response}], self.model_name)
        return response, prompt_cost, complete_cost, self.model_name

    def set_model(self, model_name: str):
        self.model_name = model_name
        self.memory.model_name = model_name

    def reset(self):
        self.memory.reset()

    def _set_system_prompt(self, system_prompt: str):
        self.memory.set_system_prompt(system_prompt)

    def _insert_cost_log(self, prompt_messages, response_message):
        prompt_tokens = num_tokens_from_messages(prompt_messages)
        complete_tokens = num_tokens_from_messages(response_message)
        logger.info(f"prompt_tokens: {prompt_tokens}, complete_tokens: {complete_tokens}")


    def set_character(self, character: str):
        self._set_system_prompt(system_prompt.system_prompt_map[character])
