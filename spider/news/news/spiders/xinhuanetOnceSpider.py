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
from news.spiders.myExt import TextExtract
from news.spiders.newsParser import NewsParser
import urllib2
from bs4 import BeautifulSoup
import json

class XinhuanetOnceSpider(scrapy.Spider):
    name='xinhuanetOnce'
    allowed_domains=["xinhuanet.com"]
    start_urls = ["http://news.xinhuanet.com/finance/2016-07/27/c_129183218.htm"]
    curTime=time.time()

    def parse(self, response):
        return XinhuanetParser(response).getNewsItem()

class XinhuanetParser(NewsParser):
    def getTitleLabel(self):
        self.item['title']=self.response.xpath('/html/head/title/text()').extract()[0].strip('\r\n')
        self.item['label']=re.search('(\w+)\.\w+\.\w+/',self.response.url).group(1)
        if self.item['label']=='www':
            self.item['label']=re.search('\w+\.\w+\.\w+/(\w+)/',self.response.url).group(1)

