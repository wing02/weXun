# -*- coding: utf-8 -*-
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
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

class XinhuaSpider(scrapy.Spider):
    name='xinhua'
    allowed_domains=["xinhuanet.com","news.cn"]
    start_urls = ["http://www.xinhuanet.com/rss.htm"]
    deny_domains=['sike\.news\.cn','info\.search\.news\.cn']
    curTime=time.time()
    days=1

    #news in 14 days will be crawled, date format is y/md.

    def __init__(self):
        scrapy.Spider.__init__(self)
        self.dateRange=[time.strftime('%Y%m%d',time.localtime(self.curTime-i*24*60*60)) for i in range(self.days)]
        self.crawledPath='../data/recent/xinhua.pickle'

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
        rssXml=response.xpath("//body/table[2]//tr//td[1]//table[2]/tbody//a/text()").extract()
        for rss in rssXml:
            yield scrapy.Request(rss,callback=self.parseXml)
        yield scrapy.Request('http://www.xinhuanet.com/',callback=self.parse3W)

    def parse3W(self,response):
        for home in response.xpath('//div[@id="navBody"]//a/@href').extract():
            if self.isDenyDomains(home):
                continue
            yield scrapy.Request(home,callback=self.parseHome)

    def parseXml(self, response):
        date=int(''.join(response.xpath('/rss/channel/item/link/text()|/rss/channel/item/description/text()').re('/(20\d{2})-([01]\d)[-/]([0123]\d)/')[:3]))
        #3 days
        outDate=int(time.strftime('%Y%m%d',time.localtime(self.curTime-3*24*60*60)))
        home=response.xpath('/rss/channel/image/link/text()').extract()[0]
        if date>outDate:
            yield scrapy.Request(home,callback=self.parseNone)
            newsLinks=response.xpath('/rss/channel/item/link/text()').extract()
            for newsLink in newsLinks:
                newsDate=self.isNews(newsLink)
                if newsDate:
                    if self.isInTime(newsDate):
                        yield scrapy.Request(newsLink,callback=self.parseNews)

    def parseHome(self,response):
        prePath=self.getPrePath(response.url)
        for url in response.xpath('//a/@href').extract():
            if self.isDenyDomains(url):
                continue
            url=url if re.search('^http',url) else prePath+url
            newsDate=self.isNews(url)
            if newsDate:
                if self.isInTime(newsDate):
                    yield scrapy.Request(url,callback=self.parseNews)
            else:
                yield scrapy.Request(url,callback=self.parsePart)

    def parsePart(self,response):
        prePath=self.getPrePath(response.url)
        for url in response.xpath('//a/@href').extract():
            url=url if re.search('^http',url) else prePath+url
            newsDate=self.isNews(url)
            if newsDate:
                if self.isInTime(newsDate):
                    yield scrapy.Request(url,callback=self.parseNews)

    def parseNews(self, response):
        if response.url in self.recentUrl:
            return
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

        #imageUrls=response.xpath('//img[@id]/@src').extract()
        #item['image_urls']=map(lambda url:url if re.search('^http',url) else prePath+url,imageUrls)

        #item['contentWithImg']=re.sub(r'<img.[^>]*>','IMG0$',''.join(response.xpath('//div[@class="article"]//p/text()|//img[@id]').extract())).replace('\n','').replace('\r','')

        self.recentUrl[response.url]=int(item['time'])
        return item

    def parseNone(self, response):
        pass

    def isNews(self,url):
        result=re.search('/(20\d{2})-?([01]\d)[-/]?([0123]\d)/',url)
        if result:
            return result.group(1)+result.group(2)+result.group(3)

    def isInTime(self,date):
        if date in self.dateRange:
            return True

    def getPrePath(self,url):
        return re.search('(.*/)',url).group(1)
    
    def isDenyDomains(self,url):
        for reg in XinhuaSpider.deny_domains:
            if re.search(reg,url):
                return True
        return False
