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

class XinhuanetOnceSpider(scrapy.Spider):
    name='xinhuanetOnce'
    allowed_domains=["xinhuanet.com"]
    start_urls = ["http://travel.news.cn/2016-06/06/c_129041510.htm"]
    curTime=time.time()

    def parse(self, response):
        return parseXinhuanetNews(self,response)

    def getPrePath(self,url):
        return re.search('(.*/)',url).group(1)

def parseXinhuanetNews(spider,response):
    prePath=spider.getPrePath(response.url)
    item = NewsItem()

    item['url']=response.url 
    item['label']=re.search('(\w+)\.\w+\.\w+/',response.url).group(1)
    if item['label']=='www':
        item['label']=re.search('\w+\.\w+\.\w+/(\w+)/',response.url).group(1)


    item['title']=response.xpath('/html/head/title/text()').extract()[0].strip('\r\n')

    item['keyWords']=''.join(response.xpath('/html/head/meta[@name="keywords"]/@content').extract()).strip('\r\n')
    try:
        item['source']=response.xpath('//span[@id="source"]/text()').extract()[0].strip('\r\n')
    except:
        try:
            item['source']=response.xpath('//em[@id="source"]/text()').extract()[0].strip('\r\n')
        except:
            pass
    
    item['time']=''.join(response.selector.re(u'(\d+)年(\d+)月(\d+)日\s*(\d+):(\d+):(\d+)'))
    if item['time']=='':
        item['time']=''.join(response.xpath('//meta[@name="pubdate"]/@content').re(u'(\d+)-(\d+)-(\d+).*?(\d+):(\d+):(\d+)'))
    if item['time']=='':
        item['time']=time.strftime('%Y%m%d%H%M%S',time.localtime(self.curTime))

    tex=TextExtract(response.body_as_unicode())
    item['contentWithImg']=tex.content
    item['image_urls']=map(lambda url:url if re.search('^http',url) else prePath+url,tex.imgs)

    return item


    
