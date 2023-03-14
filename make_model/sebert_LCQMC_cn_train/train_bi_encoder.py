#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import os
import random
from pathlib import Path
from sentence_transformers.evaluation import EmbeddingSimilarityEvaluator
from torch.utils.data import DataLoader
import math
from sentence_transformers import SentenceTransformer, LoggingHandler, losses, models
from sentence_transformers.readers import InputExample
import logging

# ROOT_DIR = os.path.dirname(os.path.abspath(__file__))  # This is your Project Root
# DATA_DIR = str(Path(ROOT_DIR) / "data")  # This is the data of this project
# MODEL_DIR = str(Path(ROOT_DIR) / "model")
from definitions import DATA_DIR,MODEL_DIR


def load_json_array(path):
    data = []
    with open(path, "r", encoding="utf-8") as f:
        while True:
            line = f.readline()
            if not line:
                break
            data.append(json.loads(line))
    return data


logging.basicConfig(format='%(asctime)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.INFO,
                    handlers=[LoggingHandler()])


def read_train_data_LCQMC(train_path, test_path):
    train_data = load_json_array(train_path)
    test_data = load_json_array(test_path)
    train_list = []
    test_list = []
    for data in train_data:
        label = -1.0 if data['gold_label'] == '0' else 1.0
        one_data = InputExample(texts=[data['sentence1'], data['sentence2']], label=label)
        train_list.append(one_data)
    for data in test_data:
        label = -1.0 if data['gold_label'] == '0' else 1.0
        one_data = InputExample(texts=[data['sentence1'], data['sentence2']], label=label)
        test_list.append(one_data)
    return train_list, test_list


def train_model(model_name, model_save_path, train_data):
    # Read the dataset
    num_epochs = 2
    train_batch_size = 4

    # Use Huggingface/transformers model (like BERT, RoBERTa, XLNet, XLM-R) for mapping tokens to embeddings
    word_embedding_model = models.Transformer(model_name)

    # Apply mean pooling to get one fixed sized sentence vector
    pooling_model = models.Pooling(word_embedding_model.get_word_embedding_dimension(),
                                   pooling_mode_mean_tokens=True,
                                   pooling_mode_cls_token=False,
                                   pooling_mode_max_tokens=False)

    model = SentenceTransformer(modules=[word_embedding_model, pooling_model], device='cuda:0')

    train_dataloader = DataLoader(train_data, shuffle=True, batch_size=train_batch_size)
    train_loss = losses.MultipleNegativesRankingLoss(model=model)

    # Configure the training. We skip evaluation in this example
    warmup_steps = math.ceil(len(train_dataloader) * num_epochs * 0.1)  # 10% of train data for warm-up
    logging.info("Warmup-steps: {}".format(warmup_steps))

    # ir_evaluator = get_answer_bot_ir_evaluator()

    # Train the model
    model.fit(train_objectives=[(train_dataloader, train_loss)],
              # evaluator=ir_evaluator,
              epochs=num_epochs,
              optimizer_params={'lr': 1e-5},
              evaluation_steps=10000,
              warmup_steps=warmup_steps,
              output_path=model_save_path,
              save_best_model=True,
              use_amp=True)


def test_model(model_save_path, test_data):
    model = SentenceTransformer(model_save_path, device='cuda:0')
    test_evaluator = EmbeddingSimilarityEvaluator.from_input_examples(test_data)
    test_evaluator(model, output_path=model_save_path)


if __name__ == '__main__':
    train_path = Path(DATA_DIR) / "LCQMC/LCQMC_train.json"
    test_path = Path(DATA_DIR) / "LCQMC/LCQMC_test.json"
    model_save_path_ = str(Path(MODEL_DIR) / 'cn_bert_LCQMC_retrieval')
    model_name_ = 'bert-base-chinese'
    train_sample, test_sample = read_train_data_LCQMC(train_path, test_path)
    train_model(model_name_, model_save_path_, train_sample)
    test_model(model_save_path_, test_sample)
    test_data = load_json_array(test_path)
    print(test_data)