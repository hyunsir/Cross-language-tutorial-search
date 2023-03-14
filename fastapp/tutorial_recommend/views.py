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
from fastapi import APIRouter, Body
from fastapi.responses import JSONResponse
tutorial_recommend = APIRouter(tags=["tutorial_recommend"])


@tutorial_recommend.api_route('/', methods=['GET', 'POST'])
def index():
    return 'Hello tutorial recommend!'


def response(code, msg, data=None):
    return JSONResponse(content={'code': code, 'msg': msg, 'data': data})