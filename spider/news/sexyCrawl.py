import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from news.spiders.newsParser import NewsParser
from news.spiders.bbcOnceSpider import BBCParser
from news.spiders.chinanewsOnceSpider import ChinaNewsParser
from news.spiders.qqOnceSpider import QQParser
from news.spiders.peopleOnceSpider import PeopleParser
from news.spiders.xinhuanetOnceSpider import XinhuanetParser
import time
import os.path as osp



class VatCrawlSpider(CrawlSpider):
    name='51vat'
    allowed_domain=['51vat.com']
    start_urls = ['http://www.51vat.com']
    rules = (
        #Rule(LinkExtractor(allow=('/(20\d{2})/([01]\d)/([0123]\d)/', )), follow=True, callback='parse_item'),
        Rule(LinkExtractor(allow=('.', )), follow=True,callback='parse_item'),
    )
    custom_settings={
        'IMAGES_STORE':osp.join('../data',time.strftime('%Y%m%d',time.localtime(time.time())),name),
    }
    def parse_item(self, response):
        return NewsParser(response).getNewsItem()

process = CrawlerProcess({
    #'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
    'ITEM_PIPELINES' :{
        'scrapy.pipelines.images.ImagesPipeline': 1,
        'news.pipelines.JsonPipeline': 300,
        },
    'DEPTH_LIMIT':2,
    'AUTOTHROTTLE_ENABLED':True,
    'LOG_LEVEL' : 'INFO',
    'CONCURRENT_REQUESTS':100,
    'REACTOR_THREADPOOL_MAXSIZE':20,
    'COOKIES_ENABLED':False,
    'RETRY_ENABLED':True,
    'DOWNLOAD_TIMEOUT':15,
    'REDIRECT_ENABLED': False,
    })

process.crawl(VatCrawlSpider)
process.start()
