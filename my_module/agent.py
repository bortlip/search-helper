import logging
import threading

from nltk.tokenize import word_tokenize
from datetime import datetime
from my_module.logger_factory import create_logger
from my_module.gpt_wrapper import gpt35_text, gpt35_text_stream
from my_module.chat_logger import ChatLogger
from my_module.message import Message
from my_module.role import Role
from my_module.agent_settings import AgentSettings

class GPT35Agent:
    def __init__(self, agent_settings):
        self.agent_settings = agent_settings
        self.messages = []
        self.system_message = Message(Role.SYSTEM.value, agent_settings.system_prompt)
        self.system_message_world_length = len(word_tokenize(self.system_message.content))
        
        logger_name = f"GPT35Agent.{agent_settings.filename_prefix}"
        self.logger = create_logger(logger_name, level=logging.INFO, filename_prefix=agent_settings.filename_prefix)
        self.chat_logger = ChatLogger(agent_settings.filename_prefix)

        self.log_message(self.system_message)

    def log_message(self, message):
        self.chat_logger.log_message(message)
        self.logger.info("\n---\n{}: {}\n".format(message.role.capitalize(), message.content))

    def step_session(self):
        self.messages.insert(0, self.system_message)
        max_reply_tokens = self.calc_max_reply_token_count()
        self.logger.info("max_reply_tokens: {}".format(max_reply_tokens))
        to_send = [message.to_api_dict() for message in self.messages]
        response = gpt35_text(to_send, self.agent_settings.gpt_temperature, max_reply_tokens)
        self.messages.pop(0)
        self.add_message(Role.ASSISTANT.value, response)
        return response

    def calc_max_reply_token_count(self):
        request_tokens = self.get_word_count() + self.system_message_world_length
        if request_tokens + self.agent_settings.gpt_max_reply_tokens > self.agent_settings.gpt_max_total_tokens:
            return self.agent_settings.gpt_max_total_tokens - request_tokens
        else:
            return self.agent_settings.gpt_max_reply_tokens

    def step_session_stream(self):
        self.messages.insert(0, self.system_message)
        max_reply_tokens = self.calc_max_reply_token_count()
        self.logger.info("max_reply_tokens: {}".format(max_reply_tokens))
        to_send = [message.to_api_dict() for message in self.messages]
        response_stream = gpt35_text_stream(to_send, self.agent_settings.gpt_temperature, max_reply_tokens)
        self.messages.pop(0)

        current_result = ""
        for chunk in response_stream:
            chunk_message = chunk['choices'][0]['delta']
            content = chunk_message.get('content', '')
            current_result += content
            yield content

        self.add_message(Role.ASSISTANT.value, current_result)

    def add_user_message(self, text):
        self.add_message(Role.USER.value, text)

    def add_assistant_message(self, text):
        self.add_message(Role.ASSISTANT.value, text)

    def checkMessagesLength(self):
        word_count = self.get_word_count()
        self.logger.info(f"\nWord count: {word_count} Msg Count: {len(self.messages)}")

        while word_count > self.agent_settings.max_session_memory:
            self.messages.pop(0)
            word_count = self.get_word_count()
            self.logger.info(f"Reduced word count: {word_count} Msg Count: {len(self.messages)}")

    def get_word_count(self):
        return sum(len(word_tokenize(message.content)) for message in self.messages) + self.system_message_world_length

    def add_message(self, role, content):
        message = Message(role, content)
        self.messages.append(message)
        self.log_message(message)
        self.checkMessagesLength()

    def clear_messages(self):
        self.messages = []

    def set_system_message(self, prompt, role = Role.SYSTEM.value):
        self.system_message = Message(role, prompt)

