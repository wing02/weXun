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

class EpochCrawlSpider(CrawlSpider):
    name='epochtimes'
    allowed_domains=['www.epochtimes.com']
    start_urls = ['http://www.epochtimes.com']
    rules = (
        Rule(LinkExtractor(allow=('/(\d{2})/([01]?\d)/([0123]?\d)/', )), follow=True, callback='parse_item'),
        Rule(LinkExtractor(allow=('.', )) ),
    )
    def parse_item(self, response):
        return NewsParser(response).getNewsItem()

class BannedbookCrawlSpider(CrawlSpider):
    name='bannedbook'
    allowed_domains=['www.bannedbook.org']
    start_urls = ['http://www.bannedbook.org/']
    rules = (
        Rule(LinkExtractor(allow=('/(20\d{2})([01]\d)([0123]\d)/', )), follow=True, callback='parse_item'),
        Rule(LinkExtractor(allow=('.', )) ),
    )
    def parse_item(self, response):
        return NewsParser(response).getNewsItem()

class MinghuiCrawlSpider(CrawlSpider):
    name='minghui'
    allowed_domains=['minghui.org']
    start_urls = ['http://www.minghui.org/']
    rules = (
        Rule(LinkExtractor(allow=('/(20\d{2})/([01]?\d)/([0123]?\d)/', )), follow=True, callback='parse_item'),
        Rule(LinkExtractor(allow=('.', )) ),
    )
    def parse_item(self, response):
        return NewsParser(response).getNewsItem()

class NtdtvCrawlSpider(CrawlSpider):
    name='ntdtv'
    allowed_domains=['ntdtv.com']
    start_urls = ['http://www.ntdtv.com']
    rules = (
        Rule(LinkExtractor(allow=('/(20\d{2})/([01]\d)/([0123]\d)/', )), follow=True, callback='parse_item'),
        Rule(LinkExtractor(allow=('.', )) ),
    )
    def parse_item(self, response):
        return NewsParser(response).getNewsItem()

class PeoplePoliticsCrawlSpider(CrawlSpider):
    name='peoplePoliticsCrawl'
    allowed_domains=["politics.people.com.cn"]
    start_urls = ["http://politics.people.com.cn"]
    rules = (
        Rule(LinkExtractor(allow=('/(20\d{2})[-/]?([01]\d)[-/]?([0123]\d)/', )), follow=True, callback='parse_item'),
        Rule(LinkExtractor(allow=('.', )) ),
    )
    def parse_item(self, response):
        return PeopleParser(response).getNewsItem()

class XinhuanetPoliticsCrawlSpider(CrawlSpider):
    name='xinhuanetPoliticsCrawl'
    allowed_domains=["xinhuanet.com","news.cn"]
    start_urls = ["http://www.news.cn/politics/"]
    rules = (
        Rule(LinkExtractor(allow=('/politics.*/(20\d{2})[-/]?([01]\d)[-/]?([0123]\d)/', )), follow=True, callback='parse_item'),
        Rule(LinkExtractor(allow=('/politics/', )) ),
    )
    def parse_item(self, response):
        return XinhuanetParser(response).getNewsItem()

#http://www.epochtimes.com/
process = CrawlerProcess({
    #'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
    'ITEM_PIPELINES' :{
        'news.pipelines.JsonPipeline': 300,
        },
    'DEPTH_LIMIT':8,
    'AUTOTHROTTLE_ENABLED':True,
    'LOG_LEVEL' : 'INFO',
    'CONCURRENT_REQUESTS':100,
    'REACTOR_THREADPOOL_MAXSIZE':20,
    'COOKIES_ENABLED':False,
    'RETRY_ENABLED':True,
    'DOWNLOAD_TIMEOUT':15,
    'REDIRECT_ENABLED': False,
    })

process.crawl(EpochCrawlSpider)
process.crawl(BannedbookCrawlSpider)
#process.crawl(MinghuiCrawlSpider)
process.crawl(NtdtvCrawlSpider)
#process.crawl(PeoplePoliticsCrawlSpider)
#process.crawl(XinhuanetPoliticsCrawlSpider)
#process.crawl(ChinanewsCrawlSpider)
#process.crawl(ChinanewsCrawlSpider)
#process.crawl(ChinaCrawlSpider)
#process.crawl(IfengCrawlSpider)
#process.crawl(PeopleCrawlSpider)
#process.crawl(QQCrawlSpider)
#process.crawl(SinaCrawlSpider)
#process.crawl(SohuCrawlSpider)
#process.crawl(SznewsCrawlSpider)
#process.crawl(WangyiCrawlSpider)
#process.crawl(XinhuanetCrawlSpider)
process.start()
