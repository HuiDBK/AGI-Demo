#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @File: demo.py
# @Desc: { llm client demo }
# @Date: 2024/09/11 10:57
import asyncio

from src.llm.client import OpenAIClient
from src.llm.config import OpenAIConfig
from src.llm.factory import LLMFactory
from src.llm.schemas import LLMType, OpenAIModel
from src.settings import llm_setting


async def main():
    llm_config = OpenAIConfig(
        api_key=llm_setting.deepseek_api_key,
        base_url=llm_setting.deepseek_base_url,
        llm_model=OpenAIModel.DEEPSEEK_CODER,
    )
    llm_client: OpenAIClient = LLMFactory.build(llm_type=LLMType.OPENAI, llm_config=llm_config)

    query = "总结这篇文章 https://juejin.cn/post/7283532551473725497"
    print("query:", query)
    resp = llm_client.ask(query)
    print("resp", resp)

    query = "如何与女生相处"
    print("\nquery:", query)
    resp = await llm_client.aask(query, stream=True)
    for chunk in resp:
        print(chunk, end="")


if __name__ == "__main__":
    asyncio.run(main())
