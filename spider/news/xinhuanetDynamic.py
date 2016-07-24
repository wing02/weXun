import scrapy
from scrapy.crawler import CrawlerProcess
from news.spiders.dynamicSpider import DynamicSpider
import time
import os
import os.path as osp

class XinhuanetDynamicSpider(DynamicSpider):
    name='xinhuanetDynamic'
    allowed_domains=["xinhua.com","news.cn"]
    start_urls = ["http://www.xinhuanet.com"]
    deny_domains=['sike\.news\.cn','info\.search\.news\.cn']
    curTime=time.time()
    oldTime=''

#QQDynamicSpider.oldTime='20160723114000'
process = CrawlerProcess({
    #'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
    })


process.crawl(XinhuanetDynamicSpider)
process.start()
