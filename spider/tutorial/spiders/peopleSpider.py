# -*- coding: utf-8 -*- import scrapy
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from tutorial.items import PeopleItem
import time
import scrapy
import re

class PeopleSpider(scrapy.Spider):
        
    name = 'www.people.com.cn'
    prefixDomains1=['www','pic','politics','world','finance','tw','military','opinion','leaders','renshi','theory','legal','society','edu','kpzg','sports','culture','art','house','auto','travel','health','scitech','tv']
    prefixDomains2=['bj','tj','he','sx','nm','ln','jl','hlj','sh','js','zj','ah','fj','jx','sd','henan','hb','hn','gd','gx','hi','cq','sc','gz','yn','xz','sn','gs','qh','nx','xj','sz']
    prefixDomains=prefixDomains1+prefixDomains2
    allowed_domains =map(lambda x:x+'.people.com.cn',prefixDomains)
    start_urls = map(lambda x:'http://'+x,allowed_domains)

    now=time.time()
    #news in 14 days will be crawled, date format is y/md.
    timeArray=[time.strftime('%Y%m%d',time.localtime(now-i*24*60*60)) for i in range(1)]

    def parse(self, response):
        prefix=re.search('http://[a-z.]*',response.url).group(0)
        for url in response.xpath('//a/@href').extract():
            if url[0:-4] != 'http':
                url=prefix+url
            yield scrapy.Request(url,callback=self.parseDir)

    def parseDir(self, response):
        prefix=re.search('http://[a-z.]*',response.url).group(0)
        for url in response.xpath('//a/@href').extract():
            date=''.join(url.split('/')[-3:-1])
            if date in PeopleSpider.timeArray:
                if url[0:-4] != 'http':
                    url=prefix+url
                yield scrapy.Request(url,callback=self.parseItem)

    def parseItem(self, response):
        prefix=re.search('http://[a-z.]*',response.url).group(0)
        item = PeopleItem()
        item['url']=response.url
        item['title'] = response.xpath('//title/text()').extract()[0].replace('\t','').split('--')[0]
        #item['content']=''.join(response.xpath('//div[@class="content clear clearfix"]//p//text()').extract()).replace('\n','').replace('\t','')
        item['contentWithImg']=''.join(response.xpath('//div[@class="content clear clearfix"]//p//text()|//div[@class="content clear clearfix"]//img').extract()).replace('\n','').replace('\t','')
        if not item['contentWithImg']:
            #item['content']=''.join(response.xpath('//div[@class="box_con"]//p//text()').extract()).replace('\n','').replace('\t','')
            item['contentWithImg']=''.join(response.xpath('//div[@class="box_con"]//p//text()|//div[@class="box_con"]//img').extract()).replace('\n','').replace('\t','')
        item['date']=''.join(response.url.split('/')[-3:-1])
        item['label']=response.url.lstrip('http:').lstrip('/').split('.')[0]
        item['time']=response.selector.re(u'\d+年\d+月\d+日\d+:\d+')[0]
        item['source']=response.xpath('//meta[@name="source"]/@content').extract()[0][3:]
        yield item
        
        for url in response.xpath('//a/@href').extract():
            date=''.join(url.split('/')[-3:-1])
            if date in PeopleSpider.timeArray:
                if url[0:-4] != 'http':
                    url=prefix+url
                yield scrapy.Request(url,callback=self.parseItem)
