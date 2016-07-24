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

class QQDynamicSpider(scrapy.Spider):
    name='qqDynamic'
    allowed_domains=["qq.com"]
    start_urls = ["http://news.qq.com/"]
    deny_domains=["v.qq.com"]
    curTime=time.time()
    oldTime=''

    def __init__(self):
        scrapy.Spider.__init__(self)
        newTime=time.strftime('%Y%m%d%H%M%S',time.localtime(self.curTime))

        self.crawledPath='../data/chgPage/'+self.name+self.oldTime+'.md5'
        dispatcher.connect(self.__del__, signals.spider_closed)
        self.chgUrl=set()
        if os.path.isfile(self.crawledPath):
            f=open(self.crawledPath,'r')
            self.urlMd5=cPickle.load(f)
            f.close()
        else:
            self.urlMd5={}
        self.crawledPath='../data/chgPage/'+self.name+newTime+'.md5'
        self.chgUrlPath='../data/chgPage/'+self.name+'Chg.url'

    def __del__(self):
        f=open(self.crawledPath,'w')
        cPickle.dump(self.urlMd5,f)
        f.close()
        f=open(self.chgUrlPath,'w')
        cPickle.dump(self.chgUrl,f)
        f.close()

    def parse(self,response):
        toNews=False
        prePath=self.getPrePath(response.url)
        for url in response.xpath("//a/@href").extract():
            if self.isDenyDomains(url):
                continue
            url=url if re.search('^http',url) else prePath+url
            newsDate=self.isNews(url)
            if newsDate:
                toNews=True
            else:
                yield scrapy.Request(url,callback=self.parseHome)
        if toNews:
            self.addUrl(response)

    def parseHome(self,response):
        toNews=False
        prePath=self.getPrePath(response.url)
        for url in response.xpath('//a/@href').extract():
            if self.isDenyDomains(url):
                continue
            url=url if re.search('^http',url) else prePath+url
            newsDate=self.isNews(url)
            if newsDate:
                toNews=True
            else:
                yield scrapy.Request(url,callback=self.parsePart)
        if toNews:
            self.addUrl(response)

    def parsePart(self,response):
        toNews=False
        prePath=self.getPrePath(response.url)
        for url in response.xpath('//a/@href').extract():
            url=url if re.search('^http',url) else prePath+url
            newsDate=self.isNews(url)
            if newsDate:
                toNews=True
                self.addUrl(response)
                break

    def isNews(self,url):
        result=re.search('/(20\d{2})-?([01]\d)[-/]?([0123]\d)/',url)
        if result:
            return result.group(1)+result.group(2)+result.group(3)

    def getPrePath(self,url):
        return re.search('(.*/)',url).group(1)
    
    def isDenyDomains(self,url):
        for reg in self.deny_domains:
            if re.search(reg,url):
                return True
        return False
    
    def addUrl(self,response):
        #newMd5=getMd5(response.body)
        newMd5=getMd5(''.join(response.xpath('//a/@href').extract()))
        if response.url in self.urlMd5:
            if self.urlMd5[response.url]!=newMd5:
                chgUrl.add(response.url)
        else:
            self.urlMd5[response.url]=newMd5


def getMd5(url):
    md5=hashlib.md5()
    md5.update(url)
    return md5.hexdigest()

