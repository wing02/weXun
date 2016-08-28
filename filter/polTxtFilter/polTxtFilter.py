#coding=utf8
from __future__ import (division,absolute_import,print_function,unicode_literals)

from filter.polTxtFilter.polTfidf import PolTfidf

class PolTxtFilter:
    def __init__(self):
        self.polTfidf=PolTfidf()
    
    def doFilter(self,item):
        item.head1,item.head2,item.keywords=json_keywords(item.title,item.label,item.getTxt())
        item.staticKeywords=item.keywords

if __name__=="__main__":

