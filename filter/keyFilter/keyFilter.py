#coding=utf8
from __future__ import (division,absolute_import,print_function,unicode_literals)

from filter.keyFilter.get_news_weight import json_keywords

class KeyFilter:
    def doFilter(self,item):
        item.head1,item.head2,item.keywords=json_keywords(item.title,item.label,item.getTxt())
        item.staticKeywords=item.keywords
