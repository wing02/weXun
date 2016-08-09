import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from news.spiders.newsParser import NewsParser
from news.spiders.sexySpider import SexyParser
import time
import os.path as osp



class JiasuCrawlSpider(CrawlSpider):
    name='12jiasu'
    allowed_domain=['12jiasu.com','c9cc.com']
    start_urls = ['http://apj8fdsq.12jiasu.com/cvbf08r/8ey3z16hixd.html']
    rules = (
        #Rule(LinkExtractor(allow=('/(20\d{2})/([01]\d)/([0123]\d)/', )), follow=True, callback='parse_item'),
        Rule(LinkExtractor(allow=('.', )), follow=True,callback='parse_item'),
    )
    custom_settings={
        'IMAGES_STORE':osp.join('../data',time.strftime('%Y%m%d',time.localtime(time.time())),name),
    }
    def parse_item(self, response):
        return SexyParser(response).getNewsItem()

process = CrawlerProcess({
    #'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
    'ITEM_PIPELINES' :{
        #'scrapy.pipelines.images.ImagesPipeline': 1,
        'news.pipelines.JsonPipeline': 300,
        },
    'DEPTH_LIMIT':8,
    #'REDIRECT_ENABLED': True,
    #'AUTOTHROTTLE_ENABLED':True,
    #'LOG_LEVEL' : 'INFO',
    #'CONCURRENT_REQUESTS':100,
    #'REACTOR_THREADPOOL_MAXSIZE':20,
    #'COOKIES_ENABLED':False,
    #'RETRY_ENABLED':True,
    #'DOWNLOAD_TIMEOUT':15,
    #'REDIRECT_ENABLED': False,
    })

process.crawl(JiasuCrawlSpider)
process.start()
