# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
-----------------------------------------
@Author: gaoya
@Email: 21212010053@m.fudan.edu.cn
@Created: 2022/08/16
------------------------------------------
@Modify: 2022/08/16
------------------------------------------
@Description:
"""
import json
from pathlib import Path
from pprint import pprint

from bs4 import BeautifulSoup
from tqdm import tqdm
# make android similarity data
from android_recommend.util import FileUtil
from android_recommend.util.data_utils import AndroidDU
from definitions import DATA_DIR, OrgAndroidData, MODEL_DIR
from sentence_transformers import evaluation, SentenceTransformer, util
import re


def make_en_android_similarity_data():
    # data_all = FileUtil.load_data_list(OrgAndroidData.developer_crawl_DIR)
    # trg2src_path = str(Path(DATA_DIR) / "android/en_cn/dev_trg2src.json")
    # pair_path = str(Path(DATA_DIR) / "android/en_cn/dev_pair.json")
    # url_base = 'https://developer.android.com'

    data_all = FileUtil.load_data_list(OrgAndroidData.source_crawl_DIR)
    trg2src_path = str(Path(DATA_DIR) / "android/en_cn/source_trg2src.json")
    pair_path = str(Path(DATA_DIR) / "android/en_cn/source_pair.json")
    url_base = 'https://source.android.com'

    url2title = get_url2title(data_all)
    trg2src = {}
    for data in tqdm(data_all):
        # print(data['url'])
        all_html = data['html']
        url = data['url']
        if '?hl=zh-cn' in url:
            continue
        soup = BeautifulSoup(all_html)
        body_tag = soup.find('div', ["devsite-article-body", "clearfix"])
        if not body_tag:
            continue
        a_tags = body_tag.find_all('a')
        if not a_tags:
            continue
        for a_tag in a_tags:
            try:
                url_in_a = a_tag['href']
                if '/' != url_in_a[0]:
                    continue
            except:
                continue
            text_in_a = a_tag.get_text()
            text_in_a = text_in_a.strip()
            src = " ".join(text_in_a.split())
            src = src.lower()
            if text_in_a == 'Get started' or text_in_a == 'Learn more' or text_in_a == "See what's new":
                continue
            url_in_a = url_base + url_in_a
            std_url_in_a = AndroidDU.url2std(url_in_a)
            subtitle = None
            if '#' in url_in_a:
                subtitle = url_in_a.split('#')[-1]
                subtitle = " ".join(subtitle.split('-'))
                if len(subtitle) > 25:
                    subtitle = None
            if std_url_in_a not in url2title:
                continue
            title = url2title[std_url_in_a]
            if subtitle:
                title += ', ' + subtitle
            # easy filter
            trg = " ".join(title.strip().split())
            trg = trg.lower()
            if src == trg:
                continue
            if len(src) < len(trg):
                if src in trg:
                    continue
            else:
                if trg in src:
                    continue
            if "what's new" in trg:
                continue
            trg_re_findall = re.findall(r"\d\.\d\.\d", trg)
            if trg_re_findall != []:
                continue
            src_re_findall = re.findall(r"\d\.\d\.\d", src)
            if src_re_findall != []:
                continue
            if trg not in trg2src.keys():
                trg2src[trg] = []
                trg2src[trg].append(src)
            else:
                if src not in trg2src[trg]:
                    trg2src[trg].append(src)
    with open(trg2src_path, "w+", encoding='utf-8') as f:
        f.write(json.dumps(trg2src, ensure_ascii=False, indent=4))
    model_path = str(Path(MODEL_DIR) / 'TinySeBert_student_43w_retrieval2')
    model = SentenceTransformer(model_path)
    ret = []
    for key in tqdm(trg2src.keys()):
        if len(trg2src[key]) == 1:
            ret.append([key, trg2src[key][0]])
        else:
            srcs = trg2src[key]
            trg_emb = model.encode(key)
            tmp_score = 1
            for src in srcs:
                score = util.cos_sim(trg_emb, model.encode(src))
                if score < tmp_score:
                    tmp_score = score
                    tmp_pair = [key, src]
            ret.append(tmp_pair)
    with open(pair_path, "w+", encoding='utf-8') as f:
        f.write(json.dumps(ret, ensure_ascii=False, indent=4))


def get_url2title(data_all):
    url2title = {}
    for data in data_all:
        if 'title' not in data:
            continue
        std_url = AndroidDU.url2std(data['url'])
        url2title[std_url] = data['title']
    return url2title


def filter_by_similarity(sentence_pairs):
    ret = []
    model_path = str(Path(MODEL_DIR) / 'TinySeBert_student_43w_retrieval2')
    model = SentenceTransformer(model_path)
    min_score = 1
    max_score = 0
    mean_score = 0
    for pair in tqdm(sentence_pairs):
        emb1 = model.encode(pair[0])
        emb2 = model.encode(pair[1])
        cos_sim = util.cos_sim(emb1, emb2)
        if cos_sim < min_score:
            min_score = cos_sim
        if cos_sim > max_score:
            max_score = cos_sim
        mean_score += cos_sim
        # print(cos_sim)
        if cos_sim < 0.6:
            continue
        if cos_sim == 1:
            continue
        ret.append(pair)
    mean_score /= len(sentence_pairs)
    print(min_score)
    print(max_score)
    print(mean_score)
    return ret


def show_cos():
    datas = FileUtil.load_data_list(str(Path(DATA_DIR) / "android/en_cn/dev_pair.json"))
    model_path = str(Path(MODEL_DIR) / 'TinySeBert_student_43w_retrieval2')
    model = SentenceTransformer(model_path)
    score_pairs = []
    for pair in tqdm(datas):
        cos_score = util.cos_sim(model.encode(pair[0]), model.encode(pair[1]))
        score_pairs.append([cos_score, pair])
    score_pairs.sort(key=lambda score_pair: score_pair[0])
    pprint(score_pairs)


if __name__ == '__main__':
    # robort = AndroidTitleIdMilvusQc()
    # query = 'parse json'
    # retrieve_top_k = 30
    # ret = robort.ask_one_query_api(query, retrieve_top_k)
    # for ret_ in ret:
    #     ret_dict = ret_.to_dict()
    #     print(ret_dict['content'])
    # en_pair_filter2()
    make_en_android_similarity_data()
    # show_cos()
