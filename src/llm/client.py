#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @File: client.py
# @Desc: { 模块描述 }
# @Date: 2024/07/24 20:45
from openai import OpenAI

from src.llm.base import BaseLLMClient
from src.llm.config import OpenAIConfig


class OpenAIClient(BaseLLMClient):
    def __init__(self, llm_config: OpenAIConfig, **kwargs):
        super().__init__(llm_config=llm_config, kwargs=kwargs)
        self.llm_config = llm_config
        self.llm_client = OpenAI(
            api_key=llm_config.api_key,
            base_url=llm_config.base_url,
            **kwargs,
        )

    def setup_system_content(self, system_content: str):
        self.system_role_content["content"] = system_content
        return self.system_role_content

    def setup_local_memory_store(self):
        self.memory_store = "local-memory"
        return self.memory_store

    def get_messages(self, query):
        user_message = {"role": "user", "content": query}
        if not self.memory_store:
            return [
                self.system_role_content,
                user_message,
            ]

        # use memory
        if self.messages:
            self.messages[0] = self.system_role_content
        else:
            self.messages.append(self.system_role_content)

        self.messages.append(user_message)
        return self.messages

    def clear_context(self):
        self.messages.clear()

    def _handle_response(self, response):
        resp_message = response.choices[0].message
        if self.memory_store:
            # store ask context
            self.messages.append(resp_message)

        return resp_message.content

    def ask(self, query: str, stream: bool = False, response_format=None, **kwargs):
        messages = self.get_messages(query)
        response = self.llm_client.chat.completions.create(
            model=self.llm_config.llm_model.value,
            messages=messages,
            stream=stream,
            response_format=response_format,
            **kwargs,
        )
        if stream:
            for resp in response:
                yield resp.choices[0].delta.content
        else:
            resp_content = self._handle_response(response)
            return resp_content
