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

class PeopleOnceSpider(scrapy.Spider):
    name='peopleOnce'
    allowed_domains=["people.com.cn"]
    start_urls = ["http://politics.people.com.cn/n1/2016/0726/c1001-28583763.html"]
    curTime=time.time()

    def parse(self, response):
        return parsePeopleNews(self,response)

    def getPrePath(self,url):
        return re.search('(.*/)',url).group(1)

def parsePeopleNews(spider,response):
    prePath=spider.getPrePath(response.url)
    item = NewsItem()

    item['url']=response.url
    item['title'] = response.xpath('//title/text()').extract()[0].replace('\t','').split('--')[0]
    item['label']=response.url.lstrip('http:').lstrip('/').split('.')[0]
    item['time']=''.join(response.selector.re(u'(\d+)年(\d+)月(\d+)日(\d+):(\d+)'))
    item['source']=response.xpath('//meta[@name="source"]/@content').extract()[0][3:]
    bbsUrl=response.xpath('//div[@id="rwb_bbstop"]/a/@href').extract()
    if bbsUrl:
        bbsContent=urllib2.urlopen(urllib2.Request(bbsUrl[0])).read()
        soup=BeautifulSoup(bbsContent,'html.parser')
        item['readNum']=soup.find("span",class_="readNum").string
        item['replayNum']=soup.find("span",class_="replayNum").string

    tex=TextExtract(response.body_as_unicode())
    item['contentWithImg']=tex.content
    item['image_urls']=map(lambda url:url if re.search('^http',url) else prePath+url,tex.imgs)

    return item


    
