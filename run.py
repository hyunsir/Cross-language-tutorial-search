#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
-----------------------------------------
@Author: duyi
@Email: yangty21@m.fudan.edu.cn
@Created: 2021/12/09
------------------------------------------
@Modify: 2021/12/09
------------------------------------------
@Description:
"""
import uvicorn
from fastapp import create_fastapp

fast_app = create_fastapp()
if __name__ == '__main__':
    uvicorn.run(fast_app, host="0.0.0.0", port=4321)
