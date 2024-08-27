#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @File: schemas.py
# @Desc: { 模块描述 }
# @Date: 2024/08/20 14:39
from enum import Enum


class LLMType(Enum):
    OPENAI = "openai"
    CLAUDE = "claude"
    DEEPSEEK = "deepseek"
    SPARKAI = "sparkai"


class OpenAIModel(Enum):
    GPT_4O = "gpt-4o"
    DEEPSEEK_CODER = "deepseek-coder"
    DEEPSEEK_CHAT = "deepseek-chat"
