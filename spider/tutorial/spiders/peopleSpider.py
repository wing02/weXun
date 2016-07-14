# -*- coding: utf-8 -*-
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher
from tutorial.items import PeopleItem
import time
import scrapy
import re
import cPickle
import os
import urllib2
from bs4 import BeautifulSoup

class PeopleSpider(scrapy.Spider):
        
    name = 'people'
    channels=['www','pic','politics','world','finance','tw','military','opinion','leaders','renshi','theory','legal','society','edu','kpzg','sports','culture','art','house','auto','travel','health','scitech','tv']
    provinces=['bj','tj','he','sx','nm','ln','jl','hlj','sh','js','zj','ah','fj','jx','sd','henan','hb','hn','gd','gx','hi','cq','sc','gz','yn','xz','sn','gs','qh','nx','xj','sz']
    prefixDomains=channels+provinces
    allowed_domains =map(lambda x:x+'.people.com.cn',prefixDomains)
    start_urls = map(lambda x:'http://'+x,allowed_domains)

    #news in 1 days will be crawled, date format is y/md.
    def __init__(self):
        dispatcher.connect(self.__del__, signals.spider_closed)
        now=time.time()
        self.timeArray=[time.strftime('%Y%m%d',time.localtime(now-i*24*60*60)) for i in range(2)]
        today=time.strftime('%Y%m%d',time.localtime(now))
        self.crawledPath='data/'+today+'/peopleCrawled.pickle'
        if not os.path.exists('data/'+today):
            os.mkdir('data/'+today)
        if os.path.isfile(self.crawledPath):
            f=open(self.crawledPath,'r')
            self.crawledUrl=cPickle.load(f)
            f.close()
        else:
            self.crawledUrl=set()

    def __del__(self):
        f=open(self.crawledPath,'w')
        cPickle.dump(self.crawledUrl,f)
        f.close()

    def parse(self, response):
        for subUrl in self.getAllUrl(response):
            date=''.join(subUrl.split('/')[-3:-1])
            if date in self.timeArray:
                if self.addUrl(subUrl):
                    yield scrapy.Request(subUrl,callback=self.parseItem)

    def parseItem(self, response):
        yield self.getInfo(response)
        for subUrl in self.getAllUrl(response):
            date=''.join(subUrl.split('/')[-3:-1])
            if date in self.timeArray:
                if self.addUrl(subUrl):
                    yield scrapy.Request(subUrl,callback=self.parseItem)

    def getInfo(self,response):
        item = PeopleItem()
        item['url']=response.url
        item['title'] = response.xpath('//title/text()').extract()[0].replace('\t','').split('--')[0]
        item['contentWithImg']=''.join(response.xpath('//div[@class="content clear clearfix"]//p//text()|//div[@class="content clear clearfix"]//img').extract()).replace('\n','').replace('\t','')
        if not item['contentWithImg']:
            item['contentWithImg']=''.join(response.xpath('//div[@class="box_con"]//p//text()|//div[@class="box_con"]//img').extract()).replace('\n','').replace('\t','')
        item['label']=response.url.lstrip('http:').lstrip('/').split('.')[0]
        item['time']=''.join(response.selector.re(u'(\d+)年(\d+)月(\d+)日(\d+):(\d+)'))
        item['source']=response.xpath('//meta[@name="source"]/@content').extract()[0][3:]
        bbsUrl=response.xpath('//div[@id="rwb_bbstop"]/a/@href').extract()
        if bbsUrl:
            bbsContent=urllib2.urlopen(urllib2.Request(bbsUrl[0])).read()
            soup=BeautifulSoup(bbsContent,'html.parser')
            item['readNum']=soup.find("span",class_="readNum").string
            item['replayNum']=soup.find("span",class_="replayNum").string
        else:
            item['readNum']=''
            item['replayNum']=''
        return item

    def getAllUrl(self,response):
        prefix=re.search('http://[a-z.]*',response.url).group(0)
        for url in response.xpath('//a/@href').extract():
            if url[0:-4] != 'http':
                url=prefix+url
            yield url

    def addUrl(self,url):
        if url in self.crawledUrl:
            return False
        else:
            self.crawledUrl.add(url)
            return True

