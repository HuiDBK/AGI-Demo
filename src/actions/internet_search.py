#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @File: internet_search.py
# @Desc: { 模块描述 }
# @Date: 2024/08/24 12:07
from src.llm.base import BaseLLMClient
from src.tools.browser_engine import BrowserEngine


class InternetSearchAction:
    browser_engine = BrowserEngine(headless=True)

    def __init__(self, llm_client: BaseLLMClient):
        self.llm_client = llm_client

    async def run(self, query: str):
        return "暂未实现"
