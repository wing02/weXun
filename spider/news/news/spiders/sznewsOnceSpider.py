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

class SznewsOnceSpider(scrapy.Spider):
    name='sznewsOnce'
    allowed_domains=['sznews.com']
    start_urls = ['http://www.sznews.com/news/content/2016-07/27/content_13656228.htm']
    curTime=time.time()

    def parse(self, response):
        return NewsParser(response).getNewsItem()

