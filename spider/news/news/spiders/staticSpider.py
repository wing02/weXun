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
from news.spiders.myExt import TextExtract
from news.spiders.newsSpider import NewsSpider

class StaticSpider(NewsSpider):
    #name='static'
    #allowed_domains=[]
    #start_urls=cPickle.load(open('../data/chgPage/qqDynamicChg.url'))
    #start_urls=[]
    #deny_domains=[]
    #curTime=time.time()
    #days=1

    def __init__(self):
        scrapy.Spider.__init__(self)
        dispatcher.connect(self.__del__, signals.spider_closed)

        self.dateRange=[time.strftime('%Y%m%d',time.localtime(self.curTime-i*24*60*60)) for i in range(self.days)]
        self.crawledPath='../data/recent/'+self.name+'.pkl'

        if os.path.isfile(self.crawledPath):
            f=open(self.crawledPath,'r')
            self.recentUrl=cPickle.load(f)
            f.close()
            # 2 day 
            outTime=int(time.strftime('%Y%m%d%H%M%S',time.localtime(self.curTime-2*24*60*60)))
            for url,t in self.recentUrl.items():
                if t < outTime:
                    self.recentUrl.pop(url)
        else:
            self.recentUrl={}

        try:
            imageStore=self.custom_settings['IMAGES_STORE']
            if not osp.isdir(imageStore):
                os.makedirs(imageStore)
        except:
            pass

    def __del__(self):
        f=open(self.crawledPath,'w')
        cPickle.dump(self.recentUrl,f)
        f.close()

    def parse(self,response):
        prePath=self.getPrePath(response.url)
        for url in response.xpath("//a/@href").extract():
            if self.isDenyDomains(url):
                continue
            url=url if re.search('^http',url) else prePath+url
            newsDate=self.isNews(url)
            if newsDate:
                if self.isInTime(newsDate):
                    if not url in self.recentUrl:
                        yield scrapy.Request(url,callback=self.parseNews)


    def isInTime(self,date):
        return date in self.dateRange

