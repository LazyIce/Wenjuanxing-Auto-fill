#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
自动填问卷星（http://www.sojump.com）
复杂的题目类型
"""
# 举例： http://www.sojump.com/jq/4738641.aspx
# 注意：该页面添加了验证码，所以此程序已经失效

# 题与题之间以 '{' 分隔，序号与答案以 ‘$‘ 分隔
# 输入类型      表示方式         解释
# 多选         1｜2｜3｜4      答案以 '｜' 号分隔
# 填空         shiyanlou      答案就是字符串
# 下拉选择          2         答案就是序列号，和单选是一样一样的
# 选择＋填空   5^shiyanlou    序号和填空间加^就行


import re
from urllib import request, parse
from time import time, strftime, localtime, sleep
import random


class Sojump(object):
    def __init__(self, jq_url):
        self.answer_list = []
        self._uri_param = {}
        self._jq_url = jq_url
        self._jq_base = "https://www.sojump.com"
        self._uri_base = "https://www.sojump.com/handler/processjq.ashx?{}"
        self._jq_sum = 0
        self._init_param()

    @staticmethod
    # 返回submitdata字符串（单选为例）
    # ([(1,2),(2,4),(3,1)]) => '1$2}2$4}3$1'
    def gen_post_string(answer):
        def concat_pair(pair):
            return '$'.join([str(pair[0]), str(pair[1])])

        tmp_list = []
        for x in answer:
            tmp_list.append(concat_pair(x))
        return '}'.join(tmp_list)

    def _init_param(self):
        resp = request.urlopen(self._jq_url)
        text = resp.read().decode()

        self._jq_sum = int(re.findall(r'div(\d+)', text)[-1])  # 取最后一个
        self._uri_param['submittype'] = '1'
        self._uri_param['t'] = str(int(time() * 1000))
        self._uri_param['starttime'] = strftime(
            "%Y/%m/%d %H:%M:%S", localtime())
        self._uri_param['rn'] = re.search(
            r'rndnum="(\d+)(.\d*)*"', text).group(1)
        self._uri_param['curID'] = re.search(
            r'(\d+).aspx', resp.geturl()).group(1)

    def submit(self):
        if len(self.answer_list) == self._jq_sum:
            answer = zip(range(1, self._jq_sum + 1), self.answer_list)
            post_data = parse.urlencode(
                {'submitdata': self.gen_post_string(answer)})
            get_data = parse.urlencode(self._uri_param)
            request_url = self._uri_base.format(get_data)
            req = request.Request(request_url, post_data.encode())
            self._result = request.urlopen(req)
        else:
            print("Error:the length of answer list doesn't match")

    def redirect_url(self):
        path = re.search(r'(/wjx.*)', self._result.read().decode()).group(0)
        # self._result.read().decode() 的内容为：您输入的验证码有误，请重新输入！
        # 程序在此失效
        print(self._jq_base + path)


def single_choice(n, tl):
    r = random.randint(1, n)
    a = 0
    i = 0
    for t in tl:
        i = i + 1
        a = a + t
        if r <= a:
            return i
    return i


def mult_choice(n, tl):
    li = []
    count = len(tl)
    for i in range(1, count + 1):
        r = random.randint(1, n)
        if r <= tl[i - 1]:
            li.append("%d" % i)
    return '|'.join(li)


def single_choice_s100(tl):
    return single_choice(100, tl)


def mult_choice_s100(tl):
    return mult_choice(100, tl)


def answer_gen_teacher():
    answer = []
    answer.append(single_choice(100, [11, 12, 9, 11, 10, 11, 8, 13, 15]))
    answer.append(single_choice(100, [54, 32, 14]))
    answer.append(single_choice(100, [46, 15, 39]))
    answer.append(single_choice(100, [86, 13, 1, 0]))
    answer.append(mult_choice(100, [98, 76, 100, 100, 63, 98, 23, 47]))
    answer.append(mult_choice(100, [100, 98, 89, 99]))
    answer.append(single_choice(100, [4, 14, 32, 49, 1]))
    answer.append(single_choice(100, [62, 32, 3, 2, 1]))
    answer.append(single_choice(100, [99, 1]))
    answer.append(single_choice(100, [89, 6, 5, 0]))
    return answer


def answer_gen_parent():
    answer = []
    answer.append(single_choice_s100([35, 65]))
    answer.append(single_choice_s100([3, 23, 67, 5, 2]))
    answer.append(single_choice_s100([43, 57]))
    answer.append(single_choice_s100([82, 18]))
    answer.append(single_choice_s100([7, 22, 61, 10]))
    answer.append(single_choice_s100([36, 51, 13]))
    answer.append(single_choice_s100([14, 11, 67, 3, 5]))
    answer.append(single_choice_s100([31, 47, 19, 3]))
    answer.append(single_choice_s100([35, 65]))

    return answer


def run():
    sj = Sojump("https://sojump.com/jq/11341805.aspx")
    sj.answer_list = answer_gen_parent()
    try:
        for x in range(1, 1000):
            sj.submit()
            sleep(30)
            sj.redirect_url()
    except Exception:
        print("exception!")
        sleep(30)


if __name__ == '__main__':
    while(1):
        run()
