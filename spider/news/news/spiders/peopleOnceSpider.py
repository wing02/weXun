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

class PeopleOnceSpider(scrapy.Spider):
    name='peopleOnce'
    allowed_domains=["people.com.cn"]
    start_urls = ["http://politics.people.com.cn/n1/2016/0726/c1001-28583763.html"]
    curTime=time.time()

    def parse(self, response):
        return PeopleParser(response).getNewsItem()

class PeopleParser(NewsParser):
    def getReadNum(self):
        bbsUrl=self.response.xpath('//div[@id="rwb_bbstop"]/a/@href').extract()
        if bbsUrl:
            bbsContent=urllib2.urlopen(urllib2.Request(bbsUrl[0])).read()
            soup=BeautifulSoup(bbsContent,'html.parser')
            self.item['readNum']=soup.find("span",class_="readNum").string
            self.item['replayNum']=soup.find("span",class_="replayNum").string
    def getReplayNum(self):
        pass
