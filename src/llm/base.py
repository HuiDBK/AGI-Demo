#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @File: base.py
# @Desc: { 模块描述 }
# @Date: 2024/08/24 12:14
import copy

from src.llm.config import BaseLLMConfig


class BaseLLMClient:
    def __init__(self, llm_config: BaseLLMConfig, **kwargs):
        self.llm_config = llm_config
        self.memory_store = None
        self.messages = list()
        self.default_system_role_content = {"role": "system", "content": "You are a helpful assistant"}
        self.system_role_content = copy.deepcopy(self.default_system_role_content)
        self.kwargs = kwargs

    def ask(self, query, **kwargs):
        raise NotImplementedError

    async def aask(self, query, **kwargs):
        raise NotImplementedError
