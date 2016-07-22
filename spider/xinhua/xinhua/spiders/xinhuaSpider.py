# -*- coding: utf-8 -*-
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy import signals
from pydispatch import dispatcher
from xinhua.items import NewsItem
import time
import scrapy
import re
import cPickle
import os
class XinhuaRssSpider(scrapy.Spider):
    name='xinhuaRss'
    allowed_domains=["xinhuanet.com","news.cn"]
    start_urls = ["http://www.xinhuanet.com/rss.htm"]

    def parse(self, response):
        rssXml=response.xpath("//body/table[2]//tr//td[1]//table[2]/tbody//a/text()").extract()
        for rss in rssXml:
            yield scrapy.Request(rss,callback=self.parseXml)

    def parseXml(self, response):
        newsLinks=response.xpath('/rss/channel/item/link/text()').extract()
        for newsLink in newsLinks:
            yield scrapy.Request(newsLink,callback=self.parseNews)
                
    def parseNews(self, response):
        prePath=re.search('(.*?/)\w+\.s?htm',response.url).group(1)
        item = NewsItem()
        item['url']=response.url
        item['title']=response.xpath('/html/head/title/text()').extract()[0].strip('\r\n')
        imageUrls=response.xpath('//img[@id]/@src').extract()
        item['image_urls']=map(lambda url:url if re.search('^http',url) else prePath+url,imageUrls)
        return item

#class XinhuaSpider(CrawlSpider):
#    name='xinhua'
#    allowed_domains=["xinhuanet.com","news.cn"]
#    start_urls=["http://www.xinhuanet.com"]
#
#    curTime=time.time()
#    #news in 14 days will be crawled, date format is y/md.
#    dateRange=[time.strftime('/%Y-%m/%d/',time.localtime(curTime-i*24*60*60)) for i in range(2)]
#
#    rules = (
#        Rule(LinkExtractor( allow=tuple(dateRange) ), callback='parseNews'),
#        Rule(LinkExtractor( allow=('.*'), deny=('/20\d{2}-[01]\d[-/][0123]\d/') ), follow=True),
#    )
#
#    def __init__(self):
#        CrawlSpider.__init__(self)
#        self.crawledPath='xinhua.pickle'
#        dispatcher.connect(self.__del__, signals.spider_closed)
#        if os.prePath.isfile(self.crawledPath):
#            f=open(self.crawledPath,'r')
#            self.recentUrl=cPickle.load(f)
#            f.close()
#            # 2 day 
#            outTime=int(time.strftime('%Y%m%d%H%M%S',time.localtime(XinhuaSpider.curTime-2*24*60*60)))
#            for url,t in self.recentUrl.items():
#                if t < outTime:
#                    self.recentUrl.pop(url)
#        else:
#            self.recentUrl={}
#
#    def __del__(self):
#        f=open(self.crawledPath,'w')
#        cPickle.dump(self.recentUrl,f)
#        f.close()
#
#    def parseNews(self, response):
#        if response.url in self.recentUrl:
#            return
#        item = NewsItem()
#        item['url']=response.url
#        item['title']=response.xpath('/html/head/title/text()').extract()[0].strip('\r\n')
#        item['time']=''.join(response.selector.re(u'(\d+)年(\d+)月(\d+)日\s*(\d+):(\d+):(\d+)'))
#        if item['time']=='':
#            item['time']=''.join(response.xpath('//meta[@name="pubdate"]/@content').re(u'(\d+)-(\d+)-(\d+).*?(\d+):(\d+):(\d+)'))
#        if item['time']=='':
#            item['time']=time.strftime('%Y%m%d%H%M%S',time.localtime(XinhuaSpider.curTime))
#        #imageUrls=response.xpath('//img[@id]/@src').extract()
#        #item['image_urls']=map(lambda url:url if re.search('^http',url) else prePath+url,imageUrls)
#        self.recentUrl[response.url]=int(item['time'])
#        return item

class XinhuaSpider(scrapy.Spider):
    name='xinhua'
    allowed_domains=["xinhuanet.com","news.cn"]
    start_urls=["http://www.xinhuanet.com"]
    deny_domains=['sike\.news\.cn']

    #news in 14 days will be crawled, date format is y/md.

    def __init__(self,curTime=time.time(),days=1):
        scrapy.Spider.__init__(self)
        self.curTime=curTime
        self.dateRange=[time.strftime('/%Y-%m[-/]%d/',time.localtime(self.curTime-i*24*60*60)) for i in range(days)]
        self.crawledPath='xinhua.pickle'
        dispatcher.connect(self.__del__, signals.spider_closed)
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

    def __del__(self):
        f=open(self.crawledPath,'w')
        cPickle.dump(self.recentUrl,f)
        f.close()

    def parse(self,response):
        for url in response.xpath('//div[@id="navBody"]//a/@href').extract():
            if self.isDenyDomains(url):
                continue
            yield scrapy.Request(url,callback=self.parseHome)

    def parseHome(self,response):
        prePath=self.getPrePath(response.url)
        for url in response.xpath('//a/@href').extract():
            if self.isDenyDomains(url):
                continue
            url=url if re.search('^http',url) else prePath+url
            if self.isNews(url):
                if self.isInTime(url):
                    yield scrapy.Request(url,callback=self.parseNews)
            else:
                yield scrapy.Request(url,callback=self.parsePart)

    def parsePart(self,response):
        prePath=self.getPrePath(response.url)
        for url in response.xpath('//a/@href').extract():
            url=url if re.search('^http',url) else prePath+url
            if self.isNews(url):
                if self.isInTime(url):
                    yield scrapy.Request(url,callback=self.parseNews)

    def parseNews(self, response):
        if response.url in self.recentUrl:
            return
        prePath=self.getPrePath(response.url)
        item = NewsItem()

        item['url']=response.url

        #item['label']=re.search('//.*?/(\w+)/',response.url).group(1)

        item['title']=response.xpath('/html/head/title/text()').extract()[0].strip('\r\n')

        #item['keyWords']=''.join(response.xpath('/html/head/meta[@name="keywords"]/@content').extract()).strip('\r\n')

        #item['source']=''.join(response.xpath('//span[@id="source"]/text()').extract()).strip('\r\n')
        
        item['time']=''.join(response.selector.re(u'(\d+)年(\d+)月(\d+)日\s*(\d+):(\d+):(\d+)'))
        if item['time']=='':
            item['time']=''.join(response.xpath('//meta[@name="pubdate"]/@content').re(u'(\d+)-(\d+)-(\d+).*?(\d+):(\d+):(\d+)'))
        if item['time']=='':
            item['time']=time.strftime('%Y%m%d%H%M%S',time.localtime(self.curTime))

        #imageUrls=response.xpath('//img[@id]/@src').extract()
        #item['image_urls']=map(lambda url:url if re.search('^http',url) else prePath+url,imageUrls)

        #item['contentWithImg']=''.join(response.xpath('//div[@class="article"]//p/text()|//img[@id]').extract())

        self.recentUrl[response.url]=int(item['time'])
        return item

    def isNews(self,url):
        return  re.search('/20\d{2}-[01]\d[-/][0123]\d/',url)

    def isInTime(self,url):
        for reg in self.dateRange:
            if re.search(reg,url):
                return True
        return False

    def getPrePath(self,url):
        return re.search('(.*/)',url).group(1)
    
    def isDenyDomains(self,url):
        for reg in XinhuaSpider.deny_domains:
            if re.search(reg,url):
                return True
        return False
