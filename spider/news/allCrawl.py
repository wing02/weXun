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

#class BBCCrawlSpider(CrawlSpider):
#    name='bbcCrawl'
#    allowed_domains=["www.bbc.com"]
#    start_urls = ["http://www.bbc.com/zhongwen/simp"]
#    rules = (
#        Rule(LinkExtractor(allow=('/(20\d{2})/([01]\d)/\d{4}([0123]\d)', )), follow=True, callback='parse_item'),
#        Rule(LinkExtractor(allow=('.', )) ),
#    )
#    custom_settings={
#        'REDIRECT_ENABLED': True,
#    }
#    def isNews(self,url):
#        result=re.search('/(20\d{2})/([01]\d)/\d{4}([0123]\d)/',url)
#        if result:
#            return result.group(1)+result.group(2)+result.group(3)
#    def parse_item(self, response):
#        return BBCParser(response).getNewsItem()

class ChinaCrawlSpider(CrawlSpider):
    name='chinaCrawl'
    allowed_domains=['china.com']
    start_urls = ['http://news.china.com/']
    rules = (
        Rule(LinkExtractor(allow=('/(20\d{2})[-/]?([01]\d)[-/]?([0123]\d)/', )), follow=True, callback='parse_item'),
        Rule(LinkExtractor(allow=('.', )) ),
    )
    def parse_item(self, response):
        return NewsParser(response).getNewsItem()

class ChinanewsCrawlSpider(CrawlSpider):
    name='chinanewsCrawl'
    allowed_domains=['chinanews.com']
    start_urls = ['http://www.chinanews.com/gn/2016/07-25/7951231.shtml']
    rules = (
        Rule(LinkExtractor(allow=('/(20\d{2})[-/]?([01]\d)[-/]?([0123]\d)/', )), follow=True, callback='parse_item'),
        Rule(LinkExtractor(allow=('.', )) ),
    )
    def parse_item(self, response):
        return ChinaNewsParser(response).getNewsItem()

class IfengCrawlSpider(CrawlSpider):
    name='ifengCrawl'
    allowed_domains=['ifeng.com']
    start_urls = ['http://news.ifeng.com/']
    rules = (
        Rule(LinkExtractor(allow=('/(20\d{2})[-/]?([01]\d)[-/]?([0123]\d)/', )), follow=True, callback='parse_item'),
        Rule(LinkExtractor(allow=('.', )) ),
    )
    def parse_item(self, response):
        return NewsParser(response).getNewsItem()

class PeopleCrawlSpider(CrawlSpider):
    name='peopleCrawl'
    allowed_domains=["people.com.cn"]
    start_urls = ["http://www.people.com.cn"]
    rules = (
        Rule(LinkExtractor(allow=('/(20\d{2})[-/]?([01]\d)[-/]?([0123]\d)/', )), follow=True, callback='parse_item'),
        Rule(LinkExtractor(allow=('.', )) ),
    )
    def parse_item(self, response):
        return PeopleParser(response).getNewsItem()

class QQCrawlSpider(CrawlSpider):
    name='qqCrawl'
    allowed_domains=["qq.com"]
    start_urls = ["http://news.qq.com/a/20160725/029157.htm"]
    rules = (
        Rule(LinkExtractor(allow=('/(20\d{2})[-/]?([01]\d)[-/]?([0123]\d)/', )), follow=True, callback='parse_item'),
        Rule(LinkExtractor(allow=('.', )) ),
    )
    def parse_item(self, response):
        return QQParser(response).getNewsItem()

class SinaCrawlSpider(CrawlSpider):
    name='sinaCrawl'
    allowed_domains=["sina.com.cn"]
    start_urls = ["http://news.sina.com.cn/"]
    rules = (
        Rule(LinkExtractor(allow=('/(20\d{2})[-/]?([01]\d)[-/]?([0123]\d)/', )), follow=True, callback='parse_item'),
        Rule(LinkExtractor(allow=('.', )) ),
    )
    def parse_item(self, response):
        return NewsParser(response).getNewsItem()

class SohuCrawlSpider(CrawlSpider):
    name='sohuCrawl'
    allowed_domains=['sohu.com']
    start_urls = ['http://news.sohu.com/']
    rules = (
        Rule(LinkExtractor(allow=('/(20\d{2})[-/]?([01]\d)[-/]?([0123]\d)/', )), follow=True, callback='parse_item'),
        Rule(LinkExtractor(allow=('.', )) ),
    )
    def parse_item(self, response):
        return NewsParser(response).getNewsItem()

class SznewsCrawlSpider(CrawlSpider):
    name='sznewsCrawl'
    allowed_domains=['sznews.com']
    start_urls = ['http://www.sznews.com/']
    rules = (
        Rule(LinkExtractor(allow=('/(20\d{2})[-/]?([01]\d)[-/]?([0123]\d)/', )), follow=True, callback='parse_item'),
        Rule(LinkExtractor(allow=('.', )) ),
    )
    def parse_item(self, response):
        return NewsParser(response).getNewsItem()

class WangyiCrawlSpider(CrawlSpider):
    name='wangyiCrawl'
    allowed_domains=['163.com']
    start_urls = ['http://news.163.com/']
    rules = (
        Rule(LinkExtractor(allow=('/(\d{2})/([01]\d)([0123]\d)/', )), follow=True, callback='parse_item'),
        Rule(LinkExtractor(allow=('.', )) ),
    )
    def isNews(self,url):
        result=re.search('/(\d{2})/([01]\d)([0123]\d)/',url)
        if result:
            return '20'+result.group(1)+result.group(2)+result.group(3)
    def parse_item(self, response):
        return NewsParser(response).getNewsItem()

class XinhuanetCrawlSpider(CrawlSpider):
    name='xinhuanetCrawl'
    allowed_domains=["xinhuanet.com","news.cn"]
    start_urls = ["http://www.xinhuanet.com"]
    rules = (
        Rule(LinkExtractor(allow=('/(20\d{2})[-/]?([01]\d)[-/]?([0123]\d)/', )), follow=True, callback='parse_item'),
        Rule(LinkExtractor(allow=('.', )) ),
    )
    def parse_item(self, response):
        return XinhuanetParser(response).getNewsItem()

process = CrawlerProcess({
    #'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
    'ITEM_PIPELINES' :{
        'news.pipelines.JsonPipeline': 300,
        },
    'DEPTH_LIMIT':5,
    'AUTOTHROTTLE_ENABLED':True,
    'LOG_LEVEL' : 'INFO',
    'CONCURRENT_REQUESTS':100,
    'REACTOR_THREADPOOL_MAXSIZE':20,
    'COOKIES_ENABLED':False,
    'RETRY_ENABLED':True,
    'DOWNLOAD_TIMEOUT':15,
    'REDIRECT_ENABLED': False,
    })

process.crawl(ChinanewsCrawlSpider)
process.crawl(ChinaCrawlSpider)
process.crawl(IfengCrawlSpider)
process.crawl(PeopleCrawlSpider)
process.crawl(QQCrawlSpider)
process.crawl(SinaCrawlSpider)
process.crawl(SohuCrawlSpider)
process.crawl(SznewsCrawlSpider)
process.crawl(WangyiCrawlSpider)
process.crawl(XinhuanetCrawlSpider)
process.start()
