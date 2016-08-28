#coding=utf8
from __future__ import (division,absolute_import,print_function,unicode_literals)

class ForeignFilter:
    def __init__(self):
        self.foreignUrls=[
                'arabic\.news\.cn'
                ]

    def doFilter(self,item):
        for foreignUrl in self.foreignUrls:
            if re.search(foreignUrl,item.url):
                item.flag='foreign'
