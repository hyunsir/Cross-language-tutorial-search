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

import spacy
from tqdm import tqdm

from android_recommend.util import FileUtil
from android_recommend.util.data_utils import DataUtils, AndroidDU
from definitions import OrgAndroidData, AndroidDataGood0, AndroidDataGood, ANDROID_DIR
from bs4 import BeautifulSoup


def is_chinese(string):
    """
    检查整个字符串是否包含中文
    :param string: 需要检查的字符串
    :return: bool
    """
    for ch in string:
        if u'\u4e00' <= ch <= u'\u9fff':
            return True
    return False

def lines2sentences():
    line_path = str(Path(ANDROID_DIR) / "en_cn/en_cn_lines.json")
    save_path = str(Path(ANDROID_DIR) / "en_cn/en_cn.json")
    line_datas = FileUtil.load_data_list(line_path)
    print(len(line_datas))
    en2cn = {}
    a = 0
    for line in line_datas:
        if line[2] == 'subtitle':
            en2cn[line[0]] = line[1]
            # print('----1录入标题----')
            # print(line[0])
            # print(line[1])
            # print('--------------')
        else:
            en_sents_list = line[0].split('\n')
            cn_sents_list = line[1].split('\n')
            if len(en_sents_list) != len(cn_sents_list):
                continue
            # print('---1 进入回车分割----')
            # print(line[0])
            # print(line[1])
            # print('-----------------')
            for en_sent,cn_sent in zip(en_sents_list,cn_sents_list):
                en_sent += ' '
                en_sent_list = en_sent.split('. ')
                cn_sent_list = cn_sent.split('。')
                if len(en_sent_list) != len(cn_sent_list):
                    a += 1
                    continue
                # print('---2 进入句号分割----')
                # print(en_sent_list)
                # print(cn_sent_list)
                # print('-----------------')
                for e_se,c_se in zip(en_sent_list,cn_sent_list):
                    if e_se == '':
                        continue
                    if not is_chinese(c_se):
                        continue
                    # print('--3 body录入--')
                    # print(e_se+'. ')
                    # print(c_se+'。')
                    # print('----')
                    tmp_en_sent = e_se.strip() + '.'
                    tmp_cn_sent = c_se.strip() + '。'
                    en2cn[tmp_en_sent] = tmp_cn_sent
    print(len(en2cn))
    print(f'a={a}')
    ret = []
    for key,value in en2cn.items():
        if len(key) > 350:
            continue
        ret.append([key,value])

    with open(save_path, "w+", encoding='utf-8') as f:
        f.write(json.dumps(ret, ensure_ascii=False, indent=4))

if __name__ == '__main__':
    lines2sentences()
    # sent = "wo sjd sjid j"
    # ls = sent.split('. ')
    # print(ls)