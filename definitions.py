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
import os
from pathlib import Path

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))  # This is your Project Root
SAVED_MODELS_DIR= str(Path(ROOT_DIR) / "data/model")
DATA_DIR = str(Path(ROOT_DIR) / "data")  # This is the data of this project
OUTPUT_DIR = str(Path(ROOT_DIR) / "output")  # This is the output of this project
# LOG_DIR = str(Path(ROOT_DIR) / "log")  # This is the log of this project
class Config:
    es_config_DIR = str(Path(ROOT_DIR) / "config/es_config.json")
    CONNECTION_CONFIG = str(Path(ROOT_DIR) / "config/connection_config.json")


TABLE_LIST = str(Path(ROOT_DIR) / "tutorial_recommend/load_docs/table_list.json")