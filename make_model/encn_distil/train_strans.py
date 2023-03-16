# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
-----------------------------------------
@Author: gaoya
@Email: 21212010053@m.fudan.edu.cn
@Created: 2022/07/25
------------------------------------------
@Modify: 2022/07/25
------------------------------------------
@Description:
"""

from sentence_transformers import SentenceTransformer, LoggingHandler, models, evaluation, losses
from torch.utils.data import DataLoader
from sentence_transformers.datasets import ParallelSentencesDataset
from datetime import datetime

import os
import logging
import gzip
import numpy as np
from pathlib import Path

from sentence_transformers import evaluation, SentenceTransformer

from definitions import DATA_DIR, MODEL_DIR
from util.file_util import FileUtil

from util.file_util import FileUtil

logging.basicConfig(format='%(asctime)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.INFO,
                    handlers=[LoggingHandler()])
logger = logging.getLogger(__name__)

teacher_model_name = 'distiluse-base-multilingual-cased-v1'  # Our monolingual teacher model, we want to convert to multiple languages
student_model_name = 'distiluse-base-multilingual-cased-v1'  # Multilingual base model we use to imitate the teacher model
# teacher_model_path = str(Path(MODEL_DIR) / "distiluse-base-multilingual-cased-v1")
student_model_path = str(Path(MODEL_DIR) / "distiluse-base-multilingual-cased-v1")


max_seq_length = 128  # Student model max. lengths for inputs (number of word pieces)
train_batch_size = 64  # Batch size for training
inference_batch_size = 64  # Batch size at inference
max_sentences_per_trainfile = 500000  # Maximum number of  parallel sentences for training
train_max_sentence_length = 250  # Maximum length (characters) for parallel training sentences

num_epochs = 5  # Train for x epochs
num_warmup_steps = 10000  # Warumup steps

num_evaluation_steps = 1000  # Evaluate performance after every xxxx steps

output_path = "output/make-multilingual-sys-" + datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
evaluator_name = 'en_cn'
# load mydata
en_cn_data = FileUtil.load_data_list(str(Path(DATA_DIR) / "android_en_cn/en_cn.json"))
len_data = len(en_cn_data)
# dev_start = int(len_data * 0.8)
dev_start = 38400
# test_start = int(len_data * 0.9)
test_start = 43264


train_datas = en_cn_data[:dev_start]
print(f'length of train data: {len(train_datas)}')
dev_datas = en_cn_data[dev_start:test_start]
print(f'length of dev data: {len(dev_datas)}')
# test_starts = en_cn_data[test_start:]
# print(f'length of test data: {len(test_starts)}')

# Read passed arguments

######## Start the extension of the teacher model to multiple languages ########
logger.info("Load teacher model")

teacher_model = SentenceTransformer(teacher_model_name)

logger.info("Create student model from scratch")
# word_embedding_model = models.Transformer(student_model_path, max_seq_length=max_seq_length)
# # Apply mean pooling to get one fixed sized sentence vector
# pooling_model = models.Pooling(word_embedding_model.get_word_embedding_dimension())  # 768
# student_model = SentenceTransformer(modules=[word_embedding_model, pooling_model])
student_model = SentenceTransformer(student_model_name)

###### Read Parallel Sentences Dataset ######
train_data = ParallelSentencesDataset(student_model=student_model, teacher_model=teacher_model,
                                      batch_size=inference_batch_size, use_embedding_cache=True)
train_data.add_dataset(train_datas, max_sentences=max_sentences_per_trainfile,
                       max_sentence_length=train_max_sentence_length)
train_dataloader = DataLoader(train_data, shuffle=True, batch_size=train_batch_size)
train_loss = losses.MSELoss(model=student_model)

#### Evaluate cross-lingual performance on different tasks #####
evaluators = []  # evaluators has a list of different evaluator classes we call periodically
logger.info("Create evaluator for " + "zgy dev_file")
src_sentences = []
trg_sentences = []
for line in dev_datas:
    src_sentences.append(line[0])
    trg_sentences.append(line[1])

# Mean Squared Error (MSE) measures the (euclidean) distance between teacher and student embeddings
dev_mse = evaluation.MSEEvaluator(src_sentences, trg_sentences, name=evaluator_name,
                                  teacher_model=teacher_model, batch_size=inference_batch_size)
evaluators.append(dev_mse)

# TranslationEvaluator computes the embeddings for all parallel sentences. It then check if the embedding of source[i] is the closest to target[i] out of all available target sentences
dev_trans_acc = evaluation.TranslationEvaluator(src_sentences, trg_sentences, name=evaluator_name,
                                                batch_size=inference_batch_size)
evaluators.append(dev_trans_acc)

# Train the model
student_model.fit(train_objectives=[(train_dataloader, train_loss)],
                  evaluator=evaluation.SequentialEvaluator(evaluators,
                                                           main_score_function=lambda scores: np.mean(scores)),
                  epochs=num_epochs,
                  warmup_steps=num_warmup_steps,
                  evaluation_steps=num_evaluation_steps,
                  output_path=output_path,
                  save_best_model=True,
                  optimizer_params={'lr': 2e-5, 'eps': 1e-6}
                  )
student_model.save(path=str(Path(MODEL_DIR) / "distiluse-base-multilingual-cased-v1-selfdistil-v2"))
