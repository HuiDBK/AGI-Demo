#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @File: browser_engine.py
# @Desc: { 模块描述 }
# @Date: 2024/08/20 14:51
import asyncio

from playwright.async_api import async_playwright
from py_tools.logging import logger

from src.tools.schemas import LinkInfo, WebPage


class BrowserEngine:
    def __init__(self, headless=True, timeout=10, **launch_kwargs):
        self.headless = headless
        self.playwright_engine = None
        self.browser = None
        self.launch_kwargs = launch_kwargs
        self.timeout = timeout  # unit seconds

    async def launch_browser(self):
        if self.browser is None:
            self.playwright_engine = await async_playwright().start()
            self.browser = await self.playwright_engine.chromium.launch(
                headless=self.headless,
                timeout=self.timeout * 1000,  # unit ms
                **self.launch_kwargs,
            )

    async def close_browser(self):
        if self.browser:
            await self.browser.close()
            await self.playwright_engine.stop()
            self.browser = None

    def get_selector(self, content: str) -> str:
        selector = "body"
        if "juejin" in content and "article-area" in content:
            # 掘金文章
            selector = "div#juejin > div.view-container > main > div > div.main-area.article-area"
        # todo 知乎、csdn、博客园
        return selector

    async def _parse_page_content(self, page, url, selector: str = "body", timeout=None) -> WebPage:
        timeout = timeout or self.timeout
        timeout = timeout * 1000  # unit ms
        async with page:
            await page.goto(url)
            await page.wait_for_load_state("networkidle")
            content = await page.content()

            if selector == "body":
                # 根据content内容制定不同的selector，只获取网页相关的数据就没有那么多干扰项
                selector = self.get_selector(content)

            try:
                inner_text = await page.inner_text(selector, timeout=timeout)
            except Exception as e:
                print(e)
                inner_text = await page.inner_text("body")

            return WebPage(url=url, content=content, inner_text=inner_text)

    async def _fetch_page_content(self, url, selector="body", timeout=None) -> WebPage:
        try:
            await self.launch_browser()
            page = await self.browser.new_page()
            return await self._parse_page_content(page, url, selector, timeout)
        except Exception as e:
            logger.error(f"_fetch_page_content error: {e}")
            return WebPage(url="", content="", inner_text="")

    async def fetch_page_content(self, urls: list, selector="body", timeout=None) -> tuple[WebPage]:
        return await asyncio.gather(*[self._fetch_page_content(url, selector, timeout) for url in urls])

    async def google_search(self, query, max_results=8) -> list[LinkInfo]:
        await self.launch_browser()
        page = await self.browser.new_page()

        async with page:
            # 打开Google主页
            await page.goto(f"https://www.google.com/search?q={query}")

            # 输入搜索词并执行搜索
            # await page.fill("textarea[name='q']", query)
            # await page.press("textarea[name='q']", "Enter")

            # 等待搜索结果页面加载
            el_selector = "div.MjjYud"
            await page.wait_for_selector(el_selector)

            # 获取搜索结果的标题和链接
            results = await page.query_selector_all(el_selector)
            search_results = await self.get_search_results(results, max_results, engine_type="google")
            return search_results

    async def baidu_search(self, query, max_results=8) -> list[LinkInfo]:
        await self.launch_browser()
        page = await self.browser.new_page()

        async with page:
            # 打开百度主页
            await page.goto(f"https://www.baidu.com/s?wd={query}")

            # 等待搜索结果页面加载
            el_selector = "div.c-container"
            await page.wait_for_selector(el_selector)

            # 获取搜索结果的标题和链接
            results = await page.query_selector_all(el_selector)
            search_results = await self.get_search_results(results, max_results, engine_type="baidu")

            return search_results

    async def bing_search(self, query, max_results=8) -> list[LinkInfo]:
        await self.launch_browser()
        page = await self.browser.new_page()

        async with page:
            # 打开bing主页
            await page.goto(f"https://www.bing.com/search?q={query}")

            # 等待搜索结果页面加载完毕
            el_selector = "li.b_algo"
            await page.wait_for_selector(el_selector)  # 确保搜索结果的链接已经加载

            # 获取搜索结果的标题和链接
            results = await page.query_selector_all(el_selector)
            search_results = await self.get_search_results(results, max_results, engine_type="bing")

            return search_results

    async def _parse_google_results(self, results, max_results=8) -> list[LinkInfo]:
        search_results = []
        for result in results:
            try:
                # 获取标题和链接
                title_element = await result.query_selector("h3")
                if not title_element:
                    continue  # 如果找不到标题，跳过这个结果

                title = await title_element.text_content()
                url = await title_element.evaluate("el => el.parentElement.href")

                # 获取快照内容
                snapshot_element = await result.query_selector("div.VwiC3b")
                snapshot = await snapshot_element.text_content() if snapshot_element else ""
                if len(search_results) >= max_results:
                    break

                search_results.append(LinkInfo(title=title, url=url, snapshot=snapshot))
            except Exception as e:
                print(e)
        return search_results

    async def _parse_bing_results(self, results, max_results=8) -> list[LinkInfo]:
        search_results = []
        for result in results:
            try:
                # 获取标题和链接
                title_element = await result.query_selector("h2 a")
                if not title_element:
                    continue  # 如果找不到标题，跳过这个结果

                title = await title_element.text_content()
                url = await title_element.get_attribute("href")

                # 获取快照内容
                snapshot_element = await result.query_selector("div.b_caption")
                snapshot = await snapshot_element.text_content() if snapshot_element else ""

                if len(search_results) >= max_results:
                    break
                search_results.append(LinkInfo(title=title, url=url, snapshot=snapshot))
            except Exception as e:
                print(e)
        return search_results

    async def _parse_baidu_results(self, results, max_results=8) -> list[LinkInfo]:
        search_results = []
        for result in results:
            try:
                # 获取标题和链接
                title_element = await result.query_selector("h3 a")
                if not title_element:
                    continue  # 如果找不到标题，跳过这个结果

                title = await title_element.text_content()
                url = await title_element.get_attribute("href")

                # 尝试获取带封面图的快照内容
                snapshot_element = await result.query_selector("div.c-span9 span.content-right_2s-H4")
                snapshot = await snapshot_element.text_content() if snapshot_element else ""

                # 如果没有封面图，尝试获取没有封面图的快照内容
                if not snapshot:
                    snapshot_element = await result.query_selector("span.content-right_1THTn")
                    snapshot = await snapshot_element.text_content() if snapshot_element else ""

                if len(search_results) >= max_results:
                    break
                search_results.append(LinkInfo(title=title, url=url, snapshot=snapshot))
            except Exception as e:
                print(e)
        return search_results

    async def get_search_results(self, results, max_results=8, engine_type="google"):
        parse_method_mapping = {
            "google": self._parse_google_results,
            "bing": self._parse_bing_results,
            "baidu": self._parse_baidu_results,
        }
        if engine_type not in parse_method_mapping:
            raise ValueError(f"Engine type {engine_type} is not supported")
        parse_method = parse_method_mapping[engine_type]
        return await parse_method(results, max_results)


async def main():
    engine = BrowserEngine(headless=False)
    # await engine.baidu_search("python异步框架大战", max_results=5)
    # await engine.bing_search("重试装饰器", max_results=5)
    # await engine.close_browser()

    # await engine.google_search("metagpt", max_results=3)
    await asyncio.gather(
        engine.google_search("metagpt", max_results=3),
        engine.baidu_search("python异步框架大战", max_results=5),
        engine.fetch_page_content(["https://juejin.cn/post/7283532551473725497"], timeout=3),
    )
    # urls = [result.url for result in results]
    # urls = ["https://juejin.cn/post/7283532551473725497"]
    # web_pages = await engine.fetch_page_content(urls, timeout=1)
    # for web_page in web_pages:
    #     print(web_page.inner_text)

    await asyncio.sleep(10)


if __name__ == "__main__":
    asyncio.run(main())
