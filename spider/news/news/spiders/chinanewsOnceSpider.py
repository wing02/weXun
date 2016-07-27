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

class ChinaNewsOnceSpider(scrapy.Spider):
    name='chinanewsOnce'
    allowed_domains=['chinanews.com']
    start_urls = ['http://www.chinanews.com/gn/2016/07-25/7951231.shtml']
    curTime=time.time()

    def parse(self, response):
        return NewsParser(self,response).getNewsItem()

    def getPrePath(self,url):
        return re.search('(https?://.*?)/',url).group(1)


class ChinaNewsParser(NewsParser):
    def getLabel(self):
        try:
            self.item['label']=response.xpath('//div[@id="nav"]//text()').extract()[-2]
        except:
            pass
