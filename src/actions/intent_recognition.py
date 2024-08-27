#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @File: intent_recognition.py
# @Desc: { 模块描述 }
# @Date: 2024/08/24 22:55
from src.llm.base import BaseLLMClient


class IntentRecognitionAction:
    def __init__(self, llm_client: BaseLLMClient):
        self.client = llm_client

    async def run(self, query: str):
        pass
