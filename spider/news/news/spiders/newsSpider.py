# -*- coding: utf-8 -*-
from scrapy import signals
from pydispatch import dispatcher
import time
import scrapy
import re
import cPickle
import os
import os.path as osp
from news.items import NewsItem
import hashlib

class NewsSpider(scrapy.Spider):

    def isNews(self,url):
        result=re.search('/(20\d{2})-?([01]\d)[-/]?([0123]\d)/',url)
        if result:
            return result.group(1)+result.group(2)+result.group(3)

    def getPrePath(self,url):
        return re.search('(.*/)',url).group(1)
    
    def isDenyDomains(self,url):
        for reg in self.deny_domains:
            if re.search(reg,url):
                return True
