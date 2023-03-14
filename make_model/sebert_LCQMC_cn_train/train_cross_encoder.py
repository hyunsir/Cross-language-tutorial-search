#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import logging
import random
from pathlib import Path

from sentence_transformers import LoggingHandler, InputExample, CrossEncoder, SentenceTransformer
from sentence_transformers.cross_encoder.evaluation import CEBinaryClassificationEvaluator
from torch.utils.data import DataLoader
import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))  # This is your Project Root
DATA_DIR = str(Path(ROOT_DIR) / "data")  # This is the data of this project
MODEL_DIR = str(Path(ROOT_DIR) / "model")
def load_json_array(path):
    data = []
    with open(path, "r", encoding="utf-8") as f:
        while True:
            line = f.readline()
            if not line:
                break
            data.append(json.loads(line))
    return data

os.environ["CUDA_VISIBLE_DEVICES"] = "0"

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
        label = 0.0 if data['gold_label'] == '0' else 1.0
        one_data = InputExample(texts=[data['sentence1'], data['sentence2']], label=label)
        train_list.append(one_data)
    for data in test_data:
        label = 0.0 if data['gold_label'] == '0' else 1.0
        one_data = InputExample(texts=[data['sentence1'], data['sentence2']], label=label)
        test_list.append(one_data)
    return train_list, test_list



def train_model(model_name, model_save_path, train_data, test_data):
    # Read the dataset
    num_epochs = 4
    train_batch_size = 8

    # We set num_labels=1, which predicts a continous score between 0 and 1
    model = CrossEncoder(model_name, num_labels=1, max_length=512)

    train_dataloader = DataLoader(train_data, shuffle=True, batch_size=train_batch_size)

    # Configure the training
    warmup_steps = 5000
    logging.info("Warmup-steps: {}".format(warmup_steps))

    evaluator = CEBinaryClassificationEvaluator.from_input_examples(test_data, name='cross_encoder_eval')

    # Train the model
    model.fit(train_dataloader=train_dataloader,
              evaluator=evaluator,
              epochs=num_epochs,
              optimizer_params={'lr': 1e-5},
              warmup_steps=warmup_steps,
              output_path=model_save_path,
              save_best_model=True,
              evaluation_steps=10000,
              use_amp=True)

    model.save(model_save_path)


def test_model(model_save_path, test_data):
    model = CrossEncoder(model_save_path, device='cuda')
    test_evaluator = CEBinaryClassificationEvaluator.from_input_examples(test_data)
    test_evaluator(model, output_path=model_save_path)


if __name__ == '__main__':
    train_path = Path(DATA_DIR) / "LCQMC/LCQMC_train.json"
    test_path = Path(DATA_DIR) / "LCQMC/LCQMC_test.json"
    model_save_path_ = str(Path(MODEL_DIR) / 'cn_bert_LCQMC_rerank')
    model_name_ = 'bert-base-chinese'
    train_sample, test_sample = read_train_data_LCQMC(train_path, test_path)
    train_model(model_name_, model_save_path_, train_sample, test_sample)
