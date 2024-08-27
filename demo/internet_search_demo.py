#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @File: main.py
# @Desc: { 模块描述 }
# @Date: 2024/08/20 14:24
import asyncio

from src.actions import IntentRecognitionAction, InternetSearchAction
from src.actions.schemas import IntentType
from src.llm.client import OpenAIClient
from src.llm.config import OpenAIConfig
from src.llm.factory import LLMFactory
from src.llm.schemas import LLMType, OpenAIModel
from src.settings import llm_setting
from src.tools.browser_engine import BrowserEngine
from src.utils.re_util import RegexUtil


async def main():
    llm_config = OpenAIConfig(
        api_key=llm_setting.deepseek_api_key,
        base_url=llm_setting.deepseek_base_url,
        llm_model=OpenAIModel.DEEPSEEK_CODER,
    )
    llm_client: OpenAIClient = LLMFactory.build(llm_type=LLMType.OPENAI, llm_config=llm_config)

    query = "总结这篇文章 https://juejin.cn/post/7283532551473725497"
    print("query:", query)

    intent_type = await IntentRecognitionAction(llm_client=llm_client).run(query)
    if intent_type == IntentType.WEBPAGE_SUMMARIZE:
        urls = RegexUtil.find_http_links(query)
        print(urls)

        browser_engine = BrowserEngine(headless=True)
        web_pages = await browser_engine.fetch_page_content(urls, timeout=1)
        context = ""
        for web_page in web_pages:
            # print(web_page.inner_text)
            context += web_page.inner_text

        query = query + f"文章内容如下 {context}"
        print("answer:")
        for token in llm_client.ask(query, stream=True):
            print(token, end="")

    elif intent_type == IntentType.SEARCH:
        browser_engine = BrowserEngine(headless=True)
        ie_search_action = InternetSearchAction(llm_client=llm_client, browser_engine=browser_engine)
        ret = await ie_search_action.run(query)
        print(ret)
    else:
        # 裸llm
        ret = llm_client.ask(query=query)
        print(ret)


if __name__ == "__main__":
    asyncio.run(main())
