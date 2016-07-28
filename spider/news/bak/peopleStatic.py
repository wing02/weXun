import scrapy
from scrapy import signals
from pydispatch import dispatcher
import time
import os
import re
import cPickle
import os.path as osp
from news.items import NewsItem
import hashlib
from news.spiders.myExt import TextExtract
from news.spiders.staticSpider import StaticSpider

class PeopleStaticSpider(StaticSpider):
    name='people'
    allowed_domains=["people.com.cn"]
    start_urls=cPickle.load(open('../data/chgPage/'+name+'Dynamic_ChgUrl.pkl'))
    deny_domains=[]
    curTime=time.time()
    days=1

    def parseNews(self, response):
        prePath=self.getPrePath(response.url)
        item = NewsItem()

        item['url']=response.url

        item['title']=response.xpath('/html/head/title/text()').extract()[0].strip('\r\n')

        self.recentUrl[response.url]=int(item['time'])
        return item

os.environ['SPIDER_NAME']=PeopleStaticSpider.name

date=time.strftime('%Y%m%d',time.localtime(PeopleStaticSpider.curTime))
imageStore=osp.join('../data',date,PeopleStaticSpider.name)
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

process.crawl(PeopleStaticSpider)
process.start()
