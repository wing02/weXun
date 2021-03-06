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

class SohuOnceSpider(scrapy.Spider):
    name='sohuOnce'
    allowed_domains=['news.sohu.com']
    start_urls = ['http://news.sohu.com/20160727/n461178082.shtml']
    curTime=time.time()

    def parse(self, response):
        return NewsParser(response).getNewsItem()


