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

from android_recommend.util import FileUtil
from definitions import DATA_DIR, MODEL_DIR


def test_accuracy_for_embedding_model(test_data, model_path, accuracy_result_path, accuracy_file_name):
    src_sentences = []
    trg_sentences = []
    for data in test_data:
        src_sentences.append(data[0])
        trg_sentences.append(data[1])
    data_length = 30000
    src_sentences = src_sentences[:data_length]
    trg_sentences = trg_sentences[:data_length]
    model = SentenceTransformer(model_path)
    dev_trans_acc = evaluation.TranslationEvaluator(src_sentences, trg_sentences, show_progress_bar=True,
                                                    name=accuracy_file_name, print_wrong_matches=True)
    dev_trans_acc(model, accuracy_result_path)


if __name__ == '__main__':
    # load data
    line_path = str(Path(DATA_DIR) / "android_en_cn/en_cn.json")
    en_cn_data = FileUtil.load_data_list(line_path)

    # config
    # dev_file = str(Path(DATA_DIR) / "android_en_cn/en_cn.json")
    accuracy_result_path = str(Path(DATA_DIR) / 'trans_evaluation')
    accuracy_file_name = 'accuracy_TinySeBert_student_43w_retrieval2_TSDAE_en_cn_30000'
    model_path = str(Path(MODEL_DIR) / 'TinySeBert_student_43w_retrieval2_TSDAE')

    test_accuracy_for_embedding_model(en_cn_data, model_path, accuracy_result_path, accuracy_file_name)
