#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @File: factory.py
# @Desc: { 模块描述 }
# @Date: 2024/08/24 12:27
from typing import Type, TypeVar

from src.llm.base import BaseLLMClient
from src.llm.client import OpenAIClient
from src.llm.config import BaseLLMConfig
from src.llm.schemas import LLMType

T_BaseLLMClient = TypeVar("T_BaseLLMClient", bound=BaseLLMClient)


class LLMFactory:
    LLM_CLIENT_MAPPING: dict[LLMType, Type[BaseLLMClient]] = {
        LLMType.OPENAI: OpenAIClient,
        LLMType.DEEPSEEK: OpenAIClient,
    }

    @classmethod
    def build(cls, llm_type: LLMType, llm_config: BaseLLMConfig, **kwargs) -> T_BaseLLMClient:
        if llm_type not in cls.LLM_CLIENT_MAPPING:
            raise ValueError(f"unsupported LLM type {llm_type}")

        llm_client_cls = cls.LLM_CLIENT_MAPPING.get(llm_type)
        return llm_client_cls(llm_config=llm_config, **kwargs)
