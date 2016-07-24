import scrapy
from scrapy.crawler import CrawlerProcess
from news.spiders.qqStaticSpider import QQStaticSpider
import time
import os
import os.path as osp

name='qq'
os.environ['SPIDER_NAME']=name

date=time.strftime('%Y%m%d',time.localtime(QQStaticSpider.curTime))
imageStore=osp.join('../data',date,name)
if not osp.isdir(imageStore):
    os.makedirs(imageStore)

process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
    'ITEM_PIPELINES' :{
        'scrapy.pipelines.images.ImagesPipeline': 1,
        'news.pipelines.NewsPipeline': 300,
        },
    'IMAGES_STORE':imageStore,
    })

process.crawl(QQStaticSpider)
process.start()
