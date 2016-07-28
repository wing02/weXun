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

class BBCOnceSpider(scrapy.Spider):
    name='bbcOnce'
    allowed_domains=["www.bbc.com"]
    start_urls = ["http://www.bbc.com/zhongwen/simp/business/2016/07/160727_japan_economy_abe"]
    curTime=time.time()

    def parse(self, response):
        return BBCParser(response).getNewsItem()

class BBCParser(NewsParser):
    def getContentImg(self):
        tex=BBCTextExtract(self.response.body_as_unicode())
        self.item['contentWithImg']=tex.content
        self.item['image_urls']=map(self.fillPath,tex.imgs)

class BBCTextExtract(TextExtract):
    re_p = re.compile(r'</p>|</figure>', re.I|re.U|re.S)
    re_img = re.compile(r'<div\s+class="js-delayed-image-load"[^>]*>|<img[^>]*>',re.I|re.S|re.U)
    doRemoveLF=True
    blockHeight = 15

