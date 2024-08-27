#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @File: schemas.py
# @Desc: { 模块描述 }
# @Date: 2024/08/24 22:55
from enum import Enum


class IntentType(Enum):
    NORMAL = "NORMAL"
    SEARCH = "SEARCH"
    WEBPAGE_SUMMARIZE = "WEBPAGE_SUMMARIZE"
    DOC_SUMMARIZE = "DOC_SUMMARIZE"
