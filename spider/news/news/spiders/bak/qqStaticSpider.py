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
from news.spiders.staticSpider import StaticSpider

class QQStaticSpider(StaticSpider):
    name='qqStatic'
    allowed_domains=["qq.com"]
    start_urls=cPickle.load(open('../data/chgPage/qqDynamic_ChgUrl.pkl'))
    deny_domains=[]
    curTime=time.time()
    days=1


    def parseNews(self, response):
        prePath=self.getPrePath(response.url)
        item = NewsItem()

        item['url']=response.url

        item['label']=re.search('//.*?/(\w+)/',response.url).group(1)

        item['title']=response.xpath('/html/head/title/text()').extract()[0].strip('\r\n')

        item['keyWords']=''.join(response.xpath('/html/head/meta[@name="keywords"]/@content').extract()).strip('\r\n')

        item['source']=''.join(response.xpath('//span[@id="source"]/text()').extract()).strip('\r\n')
        
        item['time']=''.join(response.selector.re(u'(\d+)年(\d+)月(\d+)日\s*(\d+):(\d+):(\d+)'))
        if item['time']=='':
            item['time']=''.join(response.xpath('//meta[@name="pubdate"]/@content').re(u'(\d+)-(\d+)-(\d+).*?(\d+):(\d+):(\d+)'))
        if item['time']=='':
            item['time']=time.strftime('%Y%m%d%H%M%S',time.localtime(self.curTime))

        tex=TextExtract(response.body_as_unicode())
        item['contentWithImg']=tex.content
        item['image_urls']=map(lambda url:url if re.search('^http',url) else prePath+url,tex.imgs)

        self.recentUrl[response.url]=int(item['time'])
        return item

