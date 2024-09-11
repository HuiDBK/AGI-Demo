#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @File: base.py
# @Desc: { 模块描述 }
# @Date: 2024/08/24 12:14
import copy

from py_tools.utils import AsyncUtil

from src.llm.config import BaseLLMConfig


class BaseLLMClient:
    def __init__(self, llm_config: BaseLLMConfig, **kwargs):
        self.llm_config = llm_config
        self.memory_store = None
        self.messages = list()
        self.default_system_role_content = {"role": "system", "content": "You are a helpful assistant"}
        self.system_role_content = copy.deepcopy(self.default_system_role_content)
        self.kwargs = kwargs

    def setup_system_content(self, system_content: str):
        self.system_role_content["content"] = system_content
        return self.system_role_content

    def ask(self, query: str, stream: bool = False, temperature: float = None, **kwargs):
        raise NotImplementedError

    async def aask(self, query: str, stream: bool = False, temperature: float = None, **kwargs):
        # await AsyncUtil.async_run(self.ask, query, stream, temperature, **kwargs)
        return await AsyncUtil.SyncToAsync(self.ask)(query, stream, temperature, **kwargs)
