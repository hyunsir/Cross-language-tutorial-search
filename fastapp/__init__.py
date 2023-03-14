# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
-----------------------------------------
@Author: gaoya
@Email: 21212010053@m.fudan.edu.cn
@Created: 2023/03/14
------------------------------------------
@Modify: 2023/03/14
------------------------------------------
@Description:
"""
from fastapi import FastAPI
from fastapp.tutorial_recommend.views import tutorial_recommend


def create_fastapp():
    # 加载
    fast_app = FastAPI()
    fast_app.include_router(tutorial_recommend, prefix="/tutorial_recommend")
    return fast_app
