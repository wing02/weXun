import scrapy
from scrapy.crawler import CrawlerProcess
from xinhua.spiders.xinhuaSpider import XinhuaSpider
import time
import os
import os.path as osp

curTime=time.time()
name='xinhua'
date=time.strftime('%Y%m%d',time.localtime(curTime))
imageStore=osp.join('../data',date,name)
if not osp.isdir(imageStore):
    os.makedirs(imageStore)

XinhuaSpider.curTime=curTime
#XinhuaSpider.custom_settings={
#        'IMAGES_STORE':imageStore,
#        'DEPTH_LIMIT':'3',
#        }

process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
    'ITEM_PIPELINES' :{
        'scrapy.pipelines.images.ImagesPipeline': 1,
        'xinhua.pipelines.XinhuaPipeline': 300,
        },
    'IMAGES_STORE':imageStore,
    })

process.crawl(XinhuaSpider)
process.start()
