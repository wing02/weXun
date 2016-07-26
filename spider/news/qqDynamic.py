import scrapy
from scrapy.crawler import CrawlerProcess
from news.spiders.dynamicSpider import DynamicSpider
import time
import os
import os.path as osp

class QQDynamicSpider(DynamicSpider):
    name='qqDynamic'
    allowed_domains=["qq.com"]
    start_urls = ["http://news.qq.com/"]
    deny_domains=["v.qq.com","class.qq.com","club.auto.qq.com","db.house.qq.com","t.qq.com"]
    curTime=time.time()
    oldTime=''

#QQDynamicSpider.oldTime='20160723114000'
process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
    })

process.crawl(QQDynamicSpider)
process.start()
