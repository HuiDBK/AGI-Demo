#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @File: config.py
# @Desc: { 模块描述 }
# @Date: 2024/08/24 12:45
from typing import Optional

from pydantic import BaseModel, Field

from src.llm.schemas import OpenAIModel


class BaseLLMConfig(BaseModel):
    api_key: str
    base_url: Optional[str]


class OpenAIConfig(BaseLLMConfig):
    llm_model: OpenAIModel = Field(description="OpenAI model type")
