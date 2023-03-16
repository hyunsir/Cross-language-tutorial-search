# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
-----------------------------------------
@Author: gaoya
@Email: 21212010053@m.fudan.edu.cn
@Created: 2022/07/27
------------------------------------------
@Modify: 2022/07/27
------------------------------------------
@Description:
"""
import os
from pathlib import Path

from sentence_transformers import evaluation, SentenceTransformer
from definitions import DATA_DIR, MODEL_DIR
from definitions import DATA_DIR
from util.file_util import FileUtil

# config
line_path = str(Path(DATA_DIR) / "android_en_cn/en_cn.json")
dev_file = str(Path(DATA_DIR) / "android_en_cn/en_cn.json")
out_path = str(Path(DATA_DIR) / 'trans_evaluation')
name = 'selfdistil_v2_en_cn_30000'
model = SentenceTransformer(str(Path(MODEL_DIR) / 'distiluse-base-multilingual-cased-v1-selfdistil-v2'))
# load data
en_cn_data = line_datas = FileUtil.load_data_list(line_path)
# print(len(en_cn_data))  # 49718
src_sentences = []
trg_sentences = []
for data in en_cn_data:
    src_sentences.append(data[0])
    trg_sentences.append(data[1])
data_length = 30000


src_sentences = src_sentences[:data_length]
trg_sentences = trg_sentences[:data_length]
# calculate acc
dev_trans_acc = evaluation.TranslationEvaluator(src_sentences, trg_sentences,show_progress_bar=True, name=name, print_wrong_matches=True)
dev_trans_acc(model, out_path)

# sts_evaluator = evaluation.EmbeddingSimilarityEvaluator(sentences1, sentences2, scores)
