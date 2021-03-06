import scrapy
from scrapy.crawler import CrawlerProcess
from news.spiders.qqSpider import QQSpider
import time
import os
import os.path as osp

curTime=time.time()
name='qq'
os.environ['SPIDER_NAME']=name

date=time.strftime('%Y%m%d',time.localtime(curTime))
imageStore=osp.join('../data',date,name)
if not osp.isdir(imageStore):
    os.makedirs(imageStore)

QQSpider.curTime=curTime

process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
    'ITEM_PIPELINES' :{
        'scrapy.pipelines.images.ImagesPipeline': 1,
        'news.pipelines.NewsPipeline': 300,
        },
    'IMAGES_STORE':imageStore,
    })

process.crawl(QQSpider)
process.start()
