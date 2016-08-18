#!/bin/python
#encoding=utf-8
from __future__ import (division,absolute_import,print_function,unicode_literals)
import jieba.analyse
import collections
import sys
try:
    reload(sys)
    sys.setdefaultencoding('utf-8')
except:
    pass

prePath='filter/keyFilter/data'


def tfidf_keyword(title,text):
    text=title+text
    keyword_dict=collections.OrderedDict()

    jieba.analyse.set_stop_words(prePath+"stop_word.txt")
    for x,w in jieba.analyse.extract_tags(text,withWeight=True,allowPOS=('n', 'nr', 'ns', 'nt', 'nz', 'ng', 'nn', 'ni', 'nb', 'j', 'l', 'g')):
        keyword_dict[x] = w


    news_sum = sum(keyword_dict.values())
    for key in keyword_dict:
        keyword_dict[key] =int (10000*(keyword_dict[key] / news_sum))

    return keyword_dict

