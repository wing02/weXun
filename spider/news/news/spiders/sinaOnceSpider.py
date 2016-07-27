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

class SinaOnceSpider(scrapy.Spider):
    name='sinaOnce'
    allowed_domains=["sina.com.cn"]
    start_urls = ["http://news.sina.com.cn/c/nd/2016-07-27/doc-ifxuifip3664479.shtml"]
    curTime=time.time()

    def parse(self, response):
        return NewsParser(response).getNewsItem()

