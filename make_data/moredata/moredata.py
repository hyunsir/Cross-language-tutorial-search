# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
-----------------------------------------
@Author: gaoya
@Email: 21212010053@m.fudan.edu.cn
@Created: 2022/08/30
------------------------------------------
@Modify: 2022/08/30
------------------------------------------
@Description:
"""

import nlpaug.augmenter.char as nac
import nlpaug.augmenter.word as naw
import nlpaug.augmenter.sentence as nas

# from definitions import DATA_DIR, Path, MODEL_DIR


class MoreData:

    def __init__(self):
        # model_dir = str(Path(DATA_DIR) / 'GoogleNews-vectors-negative300.bin')
        # self.aug = naw.WordEmbsAug(
        #     model_type='word2vec', model_path=model_dir, action="substitute")  # substitute

        # model_path = str(Path(MODEL_DIR) / 'bert-base-uncased')
        # self.aug = naw.ContextualWordEmbsAug(model_path='bert-base-uncased', action="substitute")

        self.aug = naw.SynonymAug(aug_src='wordnet')

        # self.aug = naw.BackTranslationAug(
        #     from_model_name='facebook/wmt19-en-de',
        #     to_model_name='facebook/wmt19-de-en'
        # )

    def one_n(self, text, n_times=1):
        aug_text = self.aug.augment(text, n=n_times)
        return aug_text

    def n_n(self, sentences):
        augmented_text = self.aug.augment(sentences)
        ret = augmented_text
        return ret


def power_set(set_a: list):
    print(set_a)
    if len(set_a) == 0:
        return [[]]
    else:
        power_set_l = power_set(set_a[0:-1])
        ret = power_set_l
        print(f"pre ret {ret}")
        print(len(power_set_l))
        for l in power_set_l:
            print(f"l:{l}")
            append_set = l + [set_a[-1]]
            ret += [append_set]
        print(f'return ret {ret}')
        return ret


if __name__ == '__main__':
    md = MoreData()
    sentences = ['A man is eating food.',
                 'A man is eating a piece of bread.',
                 'The girl is carrying a baby.',
                 'A man is riding a horse.',
                 'A woman is playing violin.',
                 'Two men pushed carts through the woods.',
                 'A man is riding a white horse on an enclosed ground.',
                 'A monkey is playing drums.',
                 'Someone in a gorilla costume is playing a set of drums.'
                 ]
    ret = md.n_n(sentences)
    print(ret)
    # print(power_set([1]))
