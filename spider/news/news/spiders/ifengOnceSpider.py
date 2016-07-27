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

class IfengOnceSpider(scrapy.Spider):
    name='ifengOnce'
    allowed_domains=['news.ifeng.com']
    start_urls = ['http://news.ifeng.com/a/20160727/49670987_0.shtml']
    curTime=time.time()

    def parse(self, response):
        return NewsParser(response).getNewsItem()


