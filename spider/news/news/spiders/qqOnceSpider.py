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


class QQOnceSpider(scrapy.Spider):
    name='qqOnce'
    allowed_domains=["qq.com"]
    start_urls = ["http://view.news.qq.com/a/20160724/006143.htm"]
    curTime=time.time()

    def parse(self, response):
        prePath=self.getPrePath(response.url)
        item = NewsItem()

        item['url']=response.url

        item['label']=re.search('//.*?/(\w+)/',response.url).group(1)

        item['title']=response.xpath('/html/head/title/text()').extract()[0].strip('\r\n')

        item['keyWords']=''.join(response.xpath('/html/head/meta[@name="keywords"]/@content').extract()).strip('\r\n')

        item['source']=''.join(response.xpath('//span[@id="source"]/text()').extract()).strip('\r\n')
        
        item['time']=''.join(response.selector.re(u'(\d+)年(\d+)月(\d+)日\s*(\d+):(\d+):?(\d+)?'))
        if item['time']=='':
            item['time']=''.join(response.xpath('//meta[@name="pubdate"]/@content').re(u'(\d+)-(\d+)-(\d+).*?(\d+):(\d+):(\d+)'))
        else:
            item['time']=item['time'][:14]
        if item['time']=='':
            item['time']=time.strftime('%Y%m%d%H%M%S',time.localtime(self.curTime))

        if response.selector.re(u'幻灯播放'):
            js=urllib2.urlopen(re.search('.*\.',response.url).group()+'hdBigPic.js').read().replace('&nbsp;',' ')
            item['image_urls']=re.findall('''http://[^']*\.jpg''',js)
            newJs=re.sub('''http://[^']*\.jpg''','IMG0$',js)
            item['contentWithImg']=re.sub('</?p>','',''.join(re.findall('<p>.*?</p>|IMG0\$',newJs))).decode('gbk')
        else:
            tex=TextExtract(response.body_as_unicode())
            item['contentWithImg']=tex.content
            item['image_urls']=map(lambda url:url if re.search('^http',url) else prePath+url,tex.imgs)

        return item

    def getPrePath(self,url):
        return re.search('(.*/)',url).group(1)
    
