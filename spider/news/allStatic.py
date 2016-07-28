# -*- coding: utf-8 -*-
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy import signals
from pydispatch import dispatcher
import time
import os
import re
import cPickle
import os.path as osp
from news.items import NewsItem
import hashlib
from news.spiders.myExt import TextExtract
from news.spiders.staticSpider import StaticSpider
from news.spiders.qqOnceSpider import QQParser
import json

class BBCStaticSpider(StaticSpider):
    name='bbc'
    allowed_domains=["www.bbc.com"]
    start_urls=cPickle.load(open('../data/chgPage/'+name+'Dynamic_ChgUrl.pkl'))
    deny_domains=[]
    curTime=time.time()
    days=1
    def parseNews(self, response):
        return parseQQNews(self,response)

class QQStaticSpider(StaticSpider):
    name='qq'
    allowed_domains=["qq.com"]
    start_urls=cPickle.load(open('../data/chgPage/'+name+'Dynamic_ChgUrl.pkl'))
    deny_domains=[]
    curTime=time.time()
    days=1
    custom_settings={
    'IMAGES_STORE':osp.join('../data',time.strftime('%Y%m%d',time.localtime(curTime)),name),
    }
    def parseNews(self, response):
        return parseQQNews(self,response)

#date=time.strftime('%Y%m%d',time.localtime(time.time()))
#imageStore=osp.join('../data',date)
#if not osp.isdir(imageStore):
#    os.makedirs(imageStore)

process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
    'ITEM_PIPELINES' :{
        'scrapy.pipelines.images.ImagesPipeline': 1,
        'news.pipelines.JsonPipeline': 300,
        },
    #'IMAGES_STORE':imageStore,
    })

process.crawl(QQStaticSpider)
process.start()
