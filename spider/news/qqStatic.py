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
from news.spiders.qqOnceSpider import parseQQNews
import json

class QQStaticSpider(StaticSpider):
    name='qq'
    allowed_domains=["qq.com"]
    start_urls=cPickle.load(open('../data/chgPage/qqDynamic_ChgUrl.pkl'))
    deny_domains=[]
    curTime=time.time()
    days=1
    def parseNews(self, response):
        return parseQQNews(self,response)


date=time.strftime('%Y%m%d',time.localtime(QQStaticSpider.curTime))
imageStore=osp.join('../data',date,name)
if not osp.isdir(imageStore):
    os.makedirs(imageStore)

process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
    'ITEM_PIPELINES' :{
        'scrapy.pipelines.images.ImagesPipeline': 1,
        #'news.pipelines.NewsPipeline': 300,
        'news.pipelines.JsonPipeline': 300,
        },
    'IMAGES_STORE':imageStore,
    })

process.crawl(QQStaticSpider)
process.start()
