from twisted.internet import reactor
from scrapy.crawler import Crawler
from scrapy import  signals
from xinhua.spiders.xinhuaSpider import XinhuaSpider
from scrapy.utils.project import get_project_settings
import time
import os
import os.path as osp

def crawl(name='xinhua'):
    spider = XinhuaSpider(time.time())
    date=time.strftime('%Y%m%d',time.localtime(spider.curTime))
    settings = get_project_settings()
    imageStore=osp.join('../data',date,name)
    if not osp.isdir(imageStore):
        os.makedirs(imageStore)

    settings.set('IMAGES_STORE',imageStore)

    crawler = Crawler(spider,settings)
    crawler.signals.connect(reactor.stop, signal=signals.spider_closed)
    #crawler.configure()
    #crawler.crawl(spider)
    #crawler.start()
    #log.start()
    reactor.run() # the script will block here until the spider_closed signal was sent

if __name__=="__main__":
    crawl("xinhua")
