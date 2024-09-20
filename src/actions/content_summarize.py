#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @File: content_summarize.py
# @Desc: { 内容总结：网页、文档总结等 }
# @Date: 2024/09/20 15:26
from py_tools.utils import RegexUtil

from src.llm.base import BaseLLMClient
from src.prompts import action_prompts
from src.tools.browser_engine import BrowserEngine


class WebPageSummaryAction:
    """网页总结"""

    sys_prompt = action_prompts.WEBPAGE_SUMMARIZE_SYS_PROMPT
    prompt_template = """用户问题：{query}
    已获取到以下网页内容：
    
    网页内容：
    {page_context}
    
    请根据用户的问题和网页内容，为我总结其主要信息
    """
    browser_engine = BrowserEngine(headless=True)

    def __init__(self, llm_client: BaseLLMClient):
        self.client = llm_client
        self.client.setup_system_content(self.sys_prompt)

    async def _get_page_context(self, query):
        """获取网页内容作为用户的上下文信息"""
        page_context = ""
        urls = RegexUtil.find_http_links(query)
        if not urls:
            return page_context

        web_pages = await self.browser_engine.fetch_page_content(urls, timeout=3)
        for web_page in web_pages:
            page_context = f"{page_context}{web_page.inner_text}\n"
        return page_context

    async def run(self, query: str, stream: bool = False):
        page_context = await self._get_page_context(query)
        query = self.prompt_template.format(query=query, page_context=page_context)
        return await self.client.aask(query=query, stream=stream)
