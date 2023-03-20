# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
-----------------------------------------
@Author: gaoya
@Email: 21212010053@m.fudan.edu.cn
@Created: 2022/07/26
------------------------------------------
@Modify: 2022/07/26
------------------------------------------
@Description:
"""
import json
from pathlib import Path
from pprint import pprint

from tqdm import tqdm

from util import FileUtil
from util.data_utils import DataUtils, AndroidDU
from definitions import OrgAndroidData, AndroidDataGood0, AndroidDataGood, ANDROID_DIR
from bs4 import BeautifulSoup

def multi_lang_gener():
    save_path = str(Path(ANDROID_DIR) / "en_cn/en_cn_lines.json")
    cn_datas = FileUtil.load_data_list(AndroidDataGood0.cn_tutorial_DIR)
    en_datas = FileUtil.load_data_list(AndroidDataGood0.en_tutorial_DIR)
    cn_url_list = []
    en_url_list = []
    for data in cn_datas:
        cn_url_list.append(data['url'])
    for data in en_datas:
        en_url_list.append(data['url'])
    both_url_list = []
    for url in en_url_list:
        if url+'?hl=zh_cn' in cn_url_list:
            both_url_list.append(url)
    # print(len(cn_url_list))  # 6148
    # print(len(en_url_list))  # 4407
    # print(len(both_url_list))  # 3641
    # a = 0  # 2777
    re_en_cn = []
    for url in both_url_list:
        en_url = url
        cn_url = url+'?hl=zh_cn'
        for _cn_data in cn_datas:
            if _cn_data['url'] == cn_url:
                cn_data = _cn_data
                break
        for _en_data in en_datas:
            if _en_data['url'] == en_url:
                en_data = _en_data
                break
        if len(cn_data['body']) == len(en_data['body']):
            for line_en,line_cn in zip(en_data['body'],cn_data['body']):
                subtitle_en = line_en[0]
                subtitle_cn = line_cn[0]
                subbody_en = line_en[1]
                subbody_cn = line_cn[1]
                if subtitle_cn != 'idstart' and subtitle_en!=subtitle_cn :
                    re_en_cn.append([subtitle_en,subtitle_cn,'subtitle'])
                if subbody_cn != subbody_en and subbody_cn:
                    re_en_cn.append([subbody_en,subbody_cn,'subbody'])
        else:
            print('not same')
            # print(en_url)
            # print(cn_url)
            # print(len(cn_data['body']))
            # print(len(en_data['body']))
            # pprint([line[2] for line in cn_data['body']])
            # pprint([line[2] for line in en_data['body']])
    with open(save_path, "w+", encoding='utf-8') as f:
        f.write(json.dumps(re_en_cn, ensure_ascii=False, indent=4))

if __name__ == '__main__':
    multi_lang_gener()