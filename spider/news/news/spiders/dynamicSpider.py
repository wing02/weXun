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
import hashlib
from news.spiders.newsSpider import NewsSpider
import logging

class DynamicSpider(NewsSpider):
    name='dynamic'
    allowed_domains=[]
    start_urls = []
    deny_domains=[]
    curTime=time.time()
    oldTime=''

    def __init__(self):
        NewsSpider.__init__(self)
        dispatcher.connect(self.__del__, signals.spider_closed)

        self.oldPath='../data/md5/'+self.name+self.oldTime+'_MD5.pkl'
        if os.path.isfile(self.oldPath):
            f=open(self.oldPath,'r')
            self.urlMd5=cPickle.load(f)
            f.close()
        else:
            logging.warn(self.name+' oldTime pickle is not found')
            self.urlMd5={}

        self.chgUrl=set()

        newTime=time.strftime('%Y%m%d%H%M%S',time.localtime(self.curTime))
        self.newPath='../data/md5/'+self.name+newTime+'_MD5.pkl'
        self.chgUrlPath='../data/chgPage/'+self.name+'_ChgUrl.pkl'

    def __del__(self):
        f=open(self.newPath,'w')
        cPickle.dump(self.urlMd5,f)
        f.close()
        f=open(self.chgUrlPath,'w')
        cPickle.dump(self.chgUrl,f)
        f.close()

    def parse(self,response):
        toNews=False
        for url in response.xpath("//a/@href").extract():
            if self.isDenyDomains(url):
                continue
            url=self.fillPath(url,response)
            newsDate=self.isNews(url)
            if newsDate and toNews==False:
                toNews=True
            else:
                yield scrapy.Request(url,callback=self.parseHome)
        if toNews:
            self.addUrl(response)

    def parseHome(self,response):
        toNews=False
        for url in response.xpath('//a/@href').extract():
            if self.isDenyDomains(url):
                continue
            url=self.fillPath(url,response)
            newsDate=self.isNews(url)
            if newsDate and toNews==False:
                toNews=True
            else:
                yield scrapy.Request(url,callback=self.parsePart)
        if toNews:
            self.addUrl(response)

    def parsePart(self,response):
        for url in response.xpath('//a/@href').extract():
            url=self.fillPath(url,response)
            newsDate=self.isNews(url)
            if newsDate:
                self.addUrl(response)
                break
    
    def addUrl(self,response):
        newMd5=getMd5(''.join(response.xpath('//a/@href').extract()).encode('u8'))
        if response.url in self.urlMd5:
            if self.urlMd5[response.url]!=newMd5:
                self.chgUrl.add(response.url)
        else:
            self.urlMd5[response.url]=newMd5


def getMd5(links):
    md5=hashlib.md5()
    md5.update(links)
    return md5.hexdigest()

