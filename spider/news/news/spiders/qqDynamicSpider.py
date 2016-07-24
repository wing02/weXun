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
from news.spiders.dynamicSpider import DynamicSpider
import hashlib

class QQDynamicSpider(DynamicSpider):
    name='qqDynamic'
    allowed_domains=["qq.com"]
    start_urls = ["http://news.qq.com/"]
    deny_domains=["v.qq.com","class.qq.com","club.auto.qq.com","db.house.qq.com","t.qq.com"]
    #curTime=time.time()
    oldTime=''
