#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @File: schemas.py
# @Desc: { 模块描述 }
# @Date: 2024/08/23 18:21
from pydantic import BaseModel


class LinkInfo(BaseModel):
    title: str
    url: str
    snapshot: str


class WebPage(BaseModel):
    url: str
    content: str
    inner_text: str
