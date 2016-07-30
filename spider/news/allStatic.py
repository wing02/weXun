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
from news.spiders.newsParser import NewsParser
from news.spiders.bbcOnceSpider import BBCParser
from news.spiders.chinanewsOnceSpider import ChinaNewsParser
from news.spiders.qqOnceSpider import QQParser
from news.spiders.peopleOnceSpider import PeopleParser
from news.spiders.xinhuanetOnceSpider import XinhuanetParser
import json

class BBCStaticSpider(StaticSpider):
    name='bbc'
    allowed_domains=["www.bbc.com"]
    start_urls=cPickle.load(open('../data/chgPage/'+name+'Dynamic_ChgUrl.pkl'))
    deny_domains=[]
    curTime=time.time()
    days=1
    custom_settings={
        'IMAGES_STORE':osp.join('../data',time.strftime('%Y%m%d',time.localtime(curTime)),name),
        'REDIRECT_ENABLED': True,
    }
    def isNews(self,url):
        result=re.search('/(20\d{2})/([01]\d)/\d{4}([0123]\d)/',url)
        if result:
            return result.group(1)+result.group(2)+result.group(3)
    def parseNews(self, response):
        return BBCParser(response).getNewsItem()

class ChinaStaticSpider(StaticSpider):
    name='china'
    allowed_domains=['china.com']
    start_urls=cPickle.load(open('../data/chgPage/'+name+'Dynamic_ChgUrl.pkl'))
    deny_domains=[]
    curTime=time.time()
    days=1
    custom_settings={
    'IMAGES_STORE':osp.join('../data',time.strftime('%Y%m%d',time.localtime(curTime)),name),
    }
    def parseNews(self, response):
        return NewsParser(response).getNewsItem()

class ChinanewsStaticSpider(StaticSpider):
    name='chinanews'
    allowed_domains=['chinanews.com']
    start_urls=cPickle.load(open('../data/chgPage/'+name+'Dynamic_ChgUrl.pkl'))
    deny_domains=[]
    curTime=time.time()
    days=1
    custom_settings={
    'IMAGES_STORE':osp.join('../data',time.strftime('%Y%m%d',time.localtime(curTime)),name),
    }
    def parseNews(self, response):
        return ChinaNewsParser(response).getNewsItem()

class IfengStaticSpider(StaticSpider):
    name='ifeng'
    allowed_domains=['news.ifeng.com']
    start_urls=cPickle.load(open('../data/chgPage/'+name+'Dynamic_ChgUrl.pkl'))
    deny_domains=[]
    curTime=time.time()
    days=1
    custom_settings={
    'IMAGES_STORE':osp.join('../data',time.strftime('%Y%m%d',time.localtime(curTime)),name),
    }
    def parseNews(self, response):
        return NewsParser(response).getNewsItem()

class PeopleStaticSpider(StaticSpider):
    name='people'
    allowed_domains=["people.com.cn"]
    start_urls=cPickle.load(open('../data/chgPage/'+name+'Dynamic_ChgUrl.pkl'))
    deny_domains=[]
    curTime=time.time()
    days=1
    custom_settings={
    'IMAGES_STORE':osp.join('../data',time.strftime('%Y%m%d',time.localtime(curTime)),name),
    }
    def parseNews(self, response):
        return PeopleParser(response).getNewsItem()

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
        return QQParser(response).getNewsItem()

class SinaStaticSpider(StaticSpider):
    name='sina'
    allowed_domains=["sina.com.cn"]
    start_urls=cPickle.load(open('../data/chgPage/'+name+'Dynamic_ChgUrl.pkl'))
    deny_domains=[]
    curTime=time.time()
    days=1
    custom_settings={
    'IMAGES_STORE':osp.join('../data',time.strftime('%Y%m%d',time.localtime(curTime)),name),
    }
    def parseNews(self, response):
        return NewsParser(response).getNewsItem()

class SohuStaticSpider(StaticSpider):
    name='sohu'
    allowed_domains=['news.sohu.com']
    start_urls=cPickle.load(open('../data/chgPage/'+name+'Dynamic_ChgUrl.pkl'))
    deny_domains=[]
    curTime=time.time()
    days=1
    custom_settings={
    'IMAGES_STORE':osp.join('../data',time.strftime('%Y%m%d',time.localtime(curTime)),name),
    }
    def parseNews(self, response):
        return NewsParser(response).getNewsItem()

class SznewsStaticSpider(StaticSpider):
    name='sznews'
    allowed_domains=['sznews.com']
    start_urls=cPickle.load(open('../data/chgPage/'+name+'Dynamic_ChgUrl.pkl'))
    deny_domains=[]
    curTime=time.time()
    days=1
    custom_settings={
    'IMAGES_STORE':osp.join('../data',time.strftime('%Y%m%d',time.localtime(curTime)),name),
    }
    def parseNews(self, response):
        return NewsParser(response).getNewsItem()

class WangyiStaticSpider(StaticSpider):
    name='wangyi'
    allowed_domains=['news.163.com']
    start_urls=cPickle.load(open('../data/chgPage/'+name+'Dynamic_ChgUrl.pkl'))
    deny_domains=[]
    curTime=time.time()
    days=1
    custom_settings={
    'IMAGES_STORE':osp.join('../data',time.strftime('%Y%m%d',time.localtime(curTime)),name),
    }
    def isNews(self,url):
        result=re.search('/(\d{2})/([01]\d)([0123]\d)/',url)
        if result:
            return '20'+result.group(1)+result.group(2)+result.group(3)
    def parseNews(self, response):
        return NewsParser(response).getNewsItem()

class XinhuanetStaticSpider(StaticSpider):
    name='xinhuanet'
    allowed_domains=["xinhua.com","news.cn"]
    start_urls=cPickle.load(open('../data/chgPage/'+name+'Dynamic_ChgUrl.pkl'))
    deny_domains=[]
    curTime=time.time()
    days=1
    custom_settings={
    'IMAGES_STORE':osp.join('../data',time.strftime('%Y%m%d',time.localtime(curTime)),name),
    }
    def parseNews(self, response):
        return XinhuanetParser(response).getNewsItem()


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
    'LOG_LEVEL' : 'INFO',
    'CONCURRENT_REQUESTS ':100,
    'REACTOR_THREADPOOL_MAXSIZE':20,
    'COOKIES_ENABLED':False,
    'RETRY_ENABLED':True,#
    'DOWNLOAD_TIMEOUT':15,
    'REDIRECT_ENABLED': False,
    })

process.crawl(BBCStaticSpider)
process.crawl(ChinanewsStaticSpider)
process.crawl(ChinaStaticSpider)
process.crawl(IfengStaticSpider)
process.crawl(PeopleStaticSpider)
process.crawl(QQStaticSpider)
process.crawl(SinaStaticSpider)
process.crawl(SohuStaticSpider)
process.crawl(SznewsStaticSpider)
process.crawl(WangyiStaticSpider)
process.crawl(XinhuanetStaticSpider)
process.start()
