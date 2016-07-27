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

class WangyiOnceSpider(scrapy.Spider):
    name='wangyiOnce'
    allowed_domains=['news.163.com']
    start_urls = ['http://news.163.com/16/0727/17/BT0FALPU00014JB6.html']
    curTime=time.time()

    def parse(self, response):
        return NewsParser(response).getNewsItem()

