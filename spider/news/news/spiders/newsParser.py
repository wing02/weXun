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
import urllib2
from bs4 import BeautifulSoup
import json

class NewsParser(object):

    def __init__(self,response):
        self.response=response
        self.prePath=re.search('(.*/)',response.url).group(1)
        self.domainPath=re.search('(https?://.*?)/',response.url).group(1)

    def getNewsItem(self):
        self.item = NewsItem()
        self.getUrl()
        self.getContentImg()
        self.getTitle()
        self.getTime()
        self.getKeyWords()
        self.getSource()
        self.getReplayNum()
        self.getReadNum()
        return self.item

    def getUrl(self):
        self.item['url']=self.response.url
        
    def getContentImg(self):
        tex=TextExtract(self.response.body_as_unicode())
        self.item['contentWithImg']=tex.content
        self.item['image_urls']=map(self.fillPath,tex.imgs)

    def getTitle(self):
        try:
            titles=re.split('_',self.response.xpath('/html/head/title/text()').extract()[0].strip('\r\n'))
            self.item['title']=titles[0]
            self.item['label']=titles[1]
        except:
            try:
                titles=re.split('--',self.response.xpath('/html/head/title/text()').extract()[0].strip('\r\n'))
                self.item['title']=titles[0]
                self.item['label']=titles[1]
            except:
                self.item['title']=self.response.xpath('/html/head/title/text()').extract()[0].strip('\r\n')

    def getLabel(self):
        pass
    
    def getTime(self):
        newsTime=''.join(self.response.selector.re(u'(\d+)[年-](\d+)[月-](\d+)日?\s*(\d+):(\d+):?(\d+)?'))
        self.item['time']=newsTime[:14]
        if len(self.item['time'])==12:
            self.item['time']+='00'
        elif self.item['time']=='':
            self.item['time']=''.join(self.response.xpath('//meta[@name="pubdate"]/@content').re(u'(\d+)-(\d+)-(\d+).*?(\d+):(\d+):(\d+)'))
            if self.item['time']=='':
                self.item['time']=time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))

    def getKeyWords(self):
        self.item['keyWords']=''.join(self.response.xpath('/html/head/meta[@name="keywords"]/@content').extract()).strip('\r\n')

    def getSource(self):
        try:
            item['source']=response.xpath('//span[@id="source"]/text()').extract()[0].strip('\r\n')
        except:
            try:
                item['source']=response.xpath('//em[@id="source"]/text()').extract()[0].strip('\r\n')
            except:
                pass

    def getReplayNum(self):
        pass

    def getReadNum(self):
        pass

    def fillPath(self,shortUrl):
        if shortUrl[:4]=='http':
            return shortUrl
        elif shortUrl[0]=='/':
            return self.domainPath+shortUrl
        else:
            return self.prePath+shortUrl

