#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author: CandiceYu
@Created: 2021/09/09
"""
import json


# from android_recommend.util import FileUtil
# from definitions import AndroidDataGood


class DataUtils:
    @staticmethod
    def save_json_array(path, data):
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

    @staticmethod
    def load_json_array(path):
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data

    @staticmethod
    def save_json_dict(path, data):
        with open(path, "w", encoding="utf-8") as f:
            f.write(json.dumps(data, indent=4))

    @staticmethod
    def load_json_dict(path):
        with open(path, "r", encoding="utf-8") as f:
            data = json.loads(f.read())
        return data

    @staticmethod
    def write_to_file(path, data):
        with open(path, "w", encoding="utf-8") as f:
            f.write(data)

    @staticmethod
    def read_from_file(path):
        with open(path, "r", encoding="utf-8") as f:
            data = f.readlines()
        return data


class AndroidDU:
    """
    Android Data Util
    """

    @staticmethod
    def body_to_string(body):
        str_body = ''
        for pair in body:
            if pair[0] and pair[0] != 'bodystart':
                str_body += pair[0].strip() + ' '
            if pair[1]:
                str_body += pair[1].strip() + ' '
        return str_body

    @staticmethod
    def body_to_describe(body):
        i = 0
        if not body or body == []:
            return ''
        st: str = body[i][1]
        length = len(body)
        while not st:
            i += 1
            if i >= length:
                return ''
            st = body[i][1]
        if len(st) < 300:
            return st
        else:
            return st[0:300] + '...'

    @staticmethod
    def body_line_to_paragraph_url(body_line, url):
        # sub_title = body_line[0]
        # sub_parag = body_line[1]
        sub_id = body_line[2]
        if sub_id == 'idstart':
            return url + '#'
        else:
            if '#' == sub_id[0]:
                return url + sub_id
            else:
                return url + '#' + sub_id

    @staticmethod
    def paragraph_url_to_url_id(paragraph_url):
        if paragraph_url[-1] == '#':
            return [paragraph_url[:-1], 'idstart']
        else:
            lis = paragraph_url.split('#')
            return lis

    @staticmethod
    def url2std(url):
        zh = 0
        if '?hl=en' in url:
            url_list = url.split('?hl=en')
            url = url_list[0]
        if '?hl=zh_cn' in url:
            url_list = url.split('?hl=zh_cn')
            url = url_list[0]
            zh = 1
        if '.html' in url:
            url_list = url.split('.html')
            url = url_list[0]
        if '#' in url:
            url_list = url.split('#')
            url = url_list[0]
        if zh:
            url += '?hl=zh_cn'
        return url

    @staticmethod
    def url2place(url):
        # https://developer.android.com/studio/run/win-usb?hl=zh_cn  to  /studio/run/win-usb
        url = url.split('?')[0]
        list = url.split('/')
        list = list[3:]
        re = ''
        for p in list:
            re += '/' + p
        return re

    @staticmethod
    def place2url(place, sample_std_url):
        # /studio/run/win-usb  to   https://developer.android.com/studio/run/win-usb?hl=zh_cn
        start = sample_std_url.split('.com/')[0] + '.com' + place
        if "?hl=zh_cn" in sample_std_url:
            start += "?hl=zh_cn"
        return start

    @staticmethod
    def list_to_str(title_list):
        re_str = title_list[0]
        for title in title_list[1:]:
            re_str += ', ' + title
        return re_str

    @staticmethod
    def body_to_sub_names(body, title):
        re_str = ""
        for line in body[1:7]:
            re_str += line[0] + ', '
        return re_str

# if __name__ == '__main__':
#     data_list = FileUtil.load_data_list(AndroidDataGood.en_tutorial_DIR)
#     for data in data_list:
#         st = DataUtils.body_to_describe(data['body'])
#         print(st)
