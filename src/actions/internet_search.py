#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @File: internet_search.py
# @Desc: { 模块描述 }
# @Date: 2024/08/24 12:07
from src.llm.base import BaseLLMClient
from src.tools.browser_engine import BrowserEngine


class InternetSearchAction:
    def __init__(self, llm_client: BaseLLMClient, browser_engine: BrowserEngine):
        self.llm_client = llm_client
        self.browser_engine = browser_engine

    async def run(self, query: str):
        pass
