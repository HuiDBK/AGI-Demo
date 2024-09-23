#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @File: main.py
# @Desc: { 模块描述 }
# @Date: 2024/08/20 14:24
import asyncio

from src.actions import (
    IntentRecognitionAction,
    InternetSearchAction,
    WebPageSummaryAction,
)
from src.actions.schemas import IntentType
from src.llm.client import OpenAIClient
from src.llm.config import OpenAIConfig
from src.llm.factory import LLMFactory
from src.llm.schemas import LLMType, OpenAIModel
from src.settings import llm_setting


def get_llm_client() -> OpenAIClient:
    llm_config = OpenAIConfig(
        api_key=llm_setting.deepseek_api_key,
        base_url=llm_setting.deepseek_base_url,
        llm_model=OpenAIModel.DEEPSEEK_CODER,
    )
    llm_client: OpenAIClient = LLMFactory.build(llm_type=LLMType.OPENAI, llm_config=llm_config)
    return llm_client


async def internet_recognition_action(query: str):
    print("query:", query)
    llm_client = get_llm_client()

    # 意图识别
    intent_type = await IntentRecognitionAction(llm_client=llm_client).run(query)
    print("intent type:", intent_type)

    if intent_type == IntentType.WEBPAGE_SUMMARIZE:
        # 网页总结
        resp = await WebPageSummaryAction(llm_client=llm_client).run(query, stream=True)
        for token in resp:
            print(token, end="")

    elif intent_type == IntentType.DOC_SUMMARIZE:
        # 文档总结
        print("resp: 暂无")

    elif intent_type == IntentType.SEARCH:
        # 联网搜索
        ie_search_action = InternetSearchAction(llm_client=llm_client)
        ret = await ie_search_action.run(query)
        print("resp:", ret)

    else:
        # 裸llm
        llm_client.setup_system_content()  # 共享同一个llm 需要清空之前配置的系统提示词
        ret = await llm_client.aask(query=query)
        print("resp:", ret)

    print()


async def main():
    queries = [
        "深圳天气情况",
        "总结这pdf",
        "你是谁",
        "总结这篇文章 https://juejin.cn/post/7283532551473725497",
    ]
    for query in queries:
        await internet_recognition_action(query)


if __name__ == "__main__":
    asyncio.run(main())
