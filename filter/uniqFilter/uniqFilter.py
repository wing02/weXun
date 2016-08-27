#coding=utf8
from __future__ import (division,absolute_import,print_function,unicode_literals)
from filter.uniqFilter.simhash.uniquer import Uniquer

class UniqFilter:
    def __init__(self):
        uniquer=Uniquer()

    def doFilter(item):
        if not uniquer.checkNews(item.getTxt()):
            item.flag='repeated'
