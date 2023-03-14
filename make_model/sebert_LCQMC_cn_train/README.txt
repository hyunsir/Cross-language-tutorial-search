+----------------------------------------------+
| 1.Large-scale Chinese Question Matching Corpus |
+----------------------------------------------+
The folder contains the corpus released in the paper:
@inproceedings{LCQMC_gdls_qcc,
    author    = {Xin Liu and Qingcai Chen and Chong Deng and Jing Chen and Dongfang Li and Huajun Zeng},
    title     = {{LCQMC:A Large-scale Chinese Question Matching Corpus}},
    booktitle = {The 27th International Conference on Computational Linguistics},
    year      = {2018}
}

+--------------+
| 2.Distribution |
+--------------+
The distribution in the corpus is as the following:
|--------------------------------------------|
|    Data    |  Total  | Positive | Negative |
|--------------------------------------------|
|  training  | 238,766 |  138,574 |  100,192 |
| validation |  8,802  |   4,402  |   4,400  |
|    test    |  12,500 |   6,250  |   6,250  |
|--------------------------------------------|

+-------------------------------------------------+
| 3.LCQMC_train.json/LCQMC_dev.json/LCQMC_test.json |
+-------------------------------------------------+
These "json" files contains three fileds in each line, each line indicates one sample:
"ID" indicates the id of the pair;
"gold_label" indicates the label of a pair, "1" means matching while "0" non-matching; 
"sentence1" indicates the first sentence in a pair;
"sentence2" indicates the second sentence in a pair.
For example,
{"gold_label": "0", "sentence1": "咸鱼怎么做好吃", "sentence2": "小咸鱼干怎么炒好吃", "ID": "1158530"}