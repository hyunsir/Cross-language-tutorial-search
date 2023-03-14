# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
-----------------------------------------
@Author: gaoya
@Email: 21212010053@m.fudan.edu.cn
@Created: 2022/10/12
------------------------------------------
@Modify: 2022/10/12
------------------------------------------
@Description:
"""
import string


# def utf_8_3_checker(str):
#     remain = 0
#     for x in range(len(str)):
#         if remain == 0:
#             print(f'new word')
#             print(f"this is {str[x]}    : {ord(str[x])}")
#             if (ord(str[x]) & 0x80) == 0x00:
#                 remain = 0
#                 print(f'remain=0')
#             elif (ord(str[x]) & 0xE0) == 0xC0:
#                 remain = 1
#                 print(f'remain=1')
#             elif (ord(str[x]) & 0xF0) == 0xE0:
#                 remain = 2
#                 print(f'remain=2')
#             # elif (ord(str[x]) & 0xF8) == 0xF0:
#             #     remain = 3
#             else:
#                 print(f'start error')
#                 return False
#         else:
#             if not ((ord(str[x]) & 0xC0) == 0x80):
#                 print(f'!!!')
#                 return False
#             print('pass')
#             remain -= 1
#     if remain == 0:
#         return True
#     else:
#         return False
import re


def utf_8_3_checker(str):
    for chr in str:
        if len(chr.encode('utf-8')) > 3:
            print(f'utf_8_3_checker find bad:{chr}')
            return False
    return True


def utf_8_3_clean(str):
    ret = ""
    for chr in str:
        if len(chr.encode('utf-8')) > 3:
            continue
        ret += chr
    return ret

def de_bad_character(str):
    str = re.sub(r'(\\[\\ntrb\"]|\\x[a-zA-Z0-9]{2})',
                      lambda x: x.group(1).encode("utf-8").decode("unicode-escape"),
                      str)
    str = re.sub(r'(\\x[a-zA-Z0-9]{2})', '', str)
    result = re.sub(':\S+?:', '', str)
    return result



def is_chinese(uchar):
    if uchar >= u'\u4e00' and uchar <= u'\u9fa5':
        return True
    else:
        return False


def is_number(uchar):
    """判断一个unicode是否是数字"""
    if uchar >= u'\u0030' and uchar <= u'\u0039':
        return True
    else:
        return False


def is_alphabet(uchar):
    """判断一个unicode是否是英文字母"""
    if (uchar >= u'\u0041' and uchar <= u'\u005a') or (uchar >= u'\u0061' and uchar <= u'\u007a'):
        return True
    else:
        return False


def is_punc(uchar):
    puncs = string.punctuation
    puncs_cn = "！？｡＂＃＄％＆＇（）＊＋，－／：；＜＝＞＠［＼］＾＿｀｛｜｝～｟｠｢｣､、〃》「」『』【】〔〕〖〗〘〙〚〛〜〝〞〟〰〾〿–—‘’‛“”„‟…‧﹏."
    if uchar in puncs or uchar in puncs_cn:
        return True
    return False


def is_other(uchar):
    """判断是否非汉字，数字和英文字符"""
    if not is_chinese(uchar) or is_number(uchar) or is_alphabet(uchar) or is_punc(uchar):
        return True
    else:
        return False


def have_other(str):
    for char in str:
        if is_other(char):
            return True
    return False


if __name__ == '__main__':
    str = 'zhangzhang张나 다 루 기 쉬 운나 다 루 기 쉬 운  野兔-🐇 基于'
    print("zhang".encode("utf-8"))
    print("张".encode("utf-8"))
    print("나".encode("utf-8"))

    print("🐇".encode("utf-8"))
    print(len("🐇".encode("utf-8")))
    print(ord("🐇") & 0xF0)
    print(utf_8_3_checker("zhang张나 다 루 기 쉬 운나 다 루"))

    # print(string.punctuation)
