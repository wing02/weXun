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

class ChinaOnceSpider(scrapy.Spider):
    name='chinaOnce'
    allowed_domains=["china.com"]
    start_urls = ["http://news.china.com/domestic/945/20160726/23155558.html"]
    curTime=time.time()

    def parse(self, response):
        return NewsParser(self,response).getNewsItem()

    def getPrePath(self,url):
        return re.search('(.*/)',url).group(1)

