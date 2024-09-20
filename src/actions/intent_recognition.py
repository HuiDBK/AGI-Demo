#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @File: intent_recognition.py
# @Desc: { 意图识别模块 }
# @Date: 2024/08/24 22:55
from py_tools.logging import logger

from src.actions.schemas import IntentType
from src.llm.base import BaseLLMClient
from src.prompts import action_prompts


class IntentRecognitionAction:
    """意图识别"""

    sys_prompt = action_prompts.INTENT_RECOGNITION_SYS_PROMPT
    prompt_template = """请根据用户的问题返回最匹配的意图类型名称。问题: {query}"""

    def __init__(self, llm_client: BaseLLMClient):
        self.client = llm_client
        self.client.setup_system_content(self.sys_prompt)

    async def run(self, query: str, stream: bool = False) -> IntentType:
        try:
            query = self.prompt_template.format(query=query)
            intent_type = await self.client.aask(query=query, stream=stream)
            intent_type = str(intent_type).strip()
            intent_type = IntentType(intent_type)
        except Exception as e:
            logger.warning(str(e))
            intent_type = IntentType.NORMAL
        return intent_type
