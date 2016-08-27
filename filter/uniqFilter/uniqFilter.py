#coding=utf8
from __future__ import (division,absolute_import,print_function,unicode_literals)
from filter.uniqFilter.simhash.uniquer import Uniquer

class UniqFilter:
    def __init__(self):
        self.uniquer=Uniquer()

    def doFilter(self,item):
        if not self.uniquer.checkNews(item.getTxt()):
            item.flag='repeated'
