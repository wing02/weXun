#coding=utf8
from __future__ import (division,absolute_import,print_function,unicode_literals)

from filter.keyFilter.get_news_weight import json_keywords

class keyFilter:
    def doFilter(self,item):
        self.head1,self.head2,self.keywords=json_keywords(item.title,item.label,item.getTxt())
