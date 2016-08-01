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

    deny_domains=['\.jpg$','\.pdf$','\.apk$','\.swf$','\.rar$','\.doc$','\.bmp$']

    def isNews(self,url):
        result=re.search('/(20\d{2})[-/]?([01]\d)[-/]?([0123]\d)/',url)
        if result:
            return result.group(1)+result.group(2)+result.group(3)

    def fillPath(self,shortUrl,response):
        try:
            prePath=re.search('(https?://.*/)',response.url).group(1)
            domainPath=re.search('(https?://.*?)/',response.url).group(1)
        except:
            prePath=response.url+'/'
            domainPath=response.url

        if shortUrl[:4]=='http':
            return shortUrl
        elif shortUrl[:1]=='/':
            return domainPath+shortUrl
        else:
            return prePath+shortUrl
    
    def isDenyDomains(self,url):
        for reg in self.deny_domains:
            if re.search(reg,url,re.I):
                return True
