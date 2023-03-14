# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
-----------------------------------------
@Author: gaoya
@Email: 21212010053@m.fudan.edu.cn
@Created: 2022/08/26
------------------------------------------
@Modify: 2022/08/26
------------------------------------------
@Description:
"""
from sentence_transformers import SentenceTransformer, util


class EmbeddingModelCosPair:
    def __init__(self, model_name):
        self.model = SentenceTransformer(model_name)

    def get_pair_cos(self, sent1, sent2):
        emb1 = self.model.encode(sent1)
        emb2 = self.model.encode(sent2)
        cos_sim = util.cos_sim(emb1, emb2)
        # print("Cosine-Similarity:", cos_sim)
        return cos_sim

