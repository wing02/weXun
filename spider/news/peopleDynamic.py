import scrapy
from scrapy.crawler import CrawlerProcess
from news.spiders.dynamicSpider import DynamicSpider
import time
import os
import os.path as osp

class PeopleDynamicSpider(DynamicSpider):
    name='peopleDynamic'
    allowed_domains=["people.com.cn"]
    start_urls = ["http://www.people.com.cn"]
    deny_domains=[]
    curTime=time.time()
    oldTime=''

#QQDynamicSpider.oldTime='20160723114000'
process = CrawlerProcess({
    #'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
    })


process.crawl(PeopleDynamicSpider)
process.start()
