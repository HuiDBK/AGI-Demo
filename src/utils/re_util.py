#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @File: re_util.py
# @Desc: { 正则工具模块 }
# @Date: 2024/08/24 11:31
import re


class RegexUtil:
    # HTTP_LINK_PATTERN = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
    HTTP_LINK_PATTERN = re.compile(r"^((https|http)?:\/\/)\S+")

    @classmethod
    def find_http_links(cls, text):
        # 查找所有匹配的HTTP链接
        http_links = cls.HTTP_LINK_PATTERN.findall(text)

        return http_links
