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

class SexyParser(NewsParser):
    def getContentImg(self):
        imgs=self.response.xpath('//img/@src').extract()
        self.item['images']=map(self.fillPath,imgs)
        self.item['contentWithImg']='1'
