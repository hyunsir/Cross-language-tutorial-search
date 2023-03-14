# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
-----------------------------------------
@Author: gaoya
@Email: 21212010053@m.fudan.edu.cn
@Created: 2022/08/18
------------------------------------------
@Modify: 2022/08/18
------------------------------------------
@Description:
"""
import json
from pathlib import Path

from sentence_transformers import SentenceTransformer, LoggingHandler
from sentence_transformers import models, util, datasets, evaluation, losses
from torch.utils.data import DataLoader

from android_recommend.util import FileUtil
from definitions import MODEL_DIR, DATA_DIR
from model_maker.trans_accuracy import test_accuracy_for_embedding_model

model_name_or_path = str(Path(DATA_DIR) / 'model/TinySeBert_student_43w_retrieval2')
save_path = str(Path(DATA_DIR) / 'model/TinySeBert_student_43w_retrieval2_TSDAE')


def fineturn_by_TSDAE(train_sentences, model_name_or_path='bert-base-uncased', save_path='output/tsdae-model'):
    # Define your sentence transformer model using CLS pooling
    word_embedding_model = models.Transformer(model_name_or_path)
    pooling_model = models.Pooling(word_embedding_model.get_word_embedding_dimension(), 'mean')
    model = SentenceTransformer(model_name_or_path)
    # Define a list with sentences (1k - 100k sentences)
    # Create the special denoising dataset that adds noise on-the-fly
    train_dataset = datasets.DenoisingAutoEncoderDataset(train_sentences)
    train_dataloader = DataLoader(train_dataset, batch_size=8, shuffle=True)
    # Use the denoising auto-encoder loss
    train_loss = losses.DenoisingAutoEncoderLoss(model, decoder_name_or_path=model_name_or_path,
                                                 tie_encoder_decoder=True)
    # Call the fit method
    model.fit(
        train_objectives=[(train_dataloader, train_loss)],
        epochs=1,
        weight_decay=0,
        scheduler='constantlr',
        optimizer_params={'lr': 3e-5},
        show_progress_bar=True
    )
    model.save(save_path)


def load_en_data():
    data_path = str(Path(DATA_DIR) / 'android/en_cn/en_cn.json')
    en_cn_data = FileUtil.load_data_list(data_path)
    ret = []
    for data_pair in en_cn_data:
        en_data = data_pair[0]
        en_data = ' '.join(en_data.split())
        if len(en_data) < 45 or len(en_data) > 335:
            continue
        ret.append(en_data)
    return ret

def test_accuracy_TSDAE():
    test_data = FileUtil.load_data_list(str(Path(DATA_DIR) / "android/en_cn/dev_pair.json"))
    model_path = str(Path(DATA_DIR) / 'model/TinySeBert_student_43w_retrieval2_android')
    accuracy_result_path = str(Path(DATA_DIR) / 'android/accuracy')
    accuracy_file_name = 'TinySeBert_student_43w_retrieval2_android'
    test_accuracy_for_embedding_model(test_data,model_path,accuracy_result_path,accuracy_file_name)

if __name__ == '__main__':
    # en_data = load_en_data()[0:5000]
    # model_name_or_path = str(Path(DATA_DIR) / 'model/TinySeBert_student_43w_retrieval2')
    # save_path = str(Path(DATA_DIR) / 'model/TinySeBert_student_43w_retrieval2_android')
    # fineturn_by_TSDAE(en_data,model_name_or_path,save_path)
    test_accuracy_TSDAE()

