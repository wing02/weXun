# -*- coding: utf-8 -*-
import scrapy
from scrapy.crawler import CrawlerProcess
from news.spiders.dynamicSpider import DynamicSpider
import time
import os
import os.path as osp
import re

#class BBCDynamicSpider(DynamicSpider):
#    name='bbcDynamic'
#    allowed_domains=["bbc.com"]
#    start_urls = ["http://www.bbc.com/zhongwen/simp"]
#    #oldTime=''
#    def isNews(self,url):
#        result=re.search('/(20\d{2})/([01]\d)/\d{4}([0123]\d)',url)
#        if result:
#            return result.group(1)+result.group(2)+result.group(3)
#    custom_settings={
#        'REDIRECT_ENABLED': True,
#    }

class ChinaDynamicSpider(DynamicSpider):
    name='chinaDynamic'
    allowed_domains=['china.com']
    start_urls = ['http://news.china.com/']
    #oldTime=''

class ChinanewsDynamicSpider(DynamicSpider):
    name='chinanewsDynamic'
    allowed_domains=['chinanews.com']
    start_urls = ['http://www.chinanews.com/']
    #oldTime=''
    
class IfengDynamicSpider(DynamicSpider):
    name='ifengDynamic'
    allowed_domains=['ifeng.com']
    start_urls = ['http://news.ifeng.com/']
    #oldTime=''

class PeopleDynamicSpider(DynamicSpider):
    name='peopleDynamic'
    allowed_domains=["people.com.cn"]
    start_urls = ["http://www.people.com.cn"]
    #oldTime=''

class QQDynamicSpider(DynamicSpider):
    name='qqDynamic'
    allowed_domains=["qq.com"]
    start_urls = ["http://news.qq.com/"]
    deny_domains=["v.qq.com","class.qq.com","club.auto.qq.com","db.house.qq.com","t.qq.com"]+DynamicSpider.deny_domains
    curTime=time.time()
    #oldTime=''

class SinaDynamicSpider(DynamicSpider):
    name='sinaDynamic'
    allowed_domains=["sina.com.cn"]
    start_urls = ["http://news.sina.com.cn/"]
    deny_domains=['roll.news.sina.com.cn']+DynamicSpider.deny_domains
    #oldTime=''

class SohuDynamicSpider(DynamicSpider):
    name='sohuDynamic'
    allowed_domains=['sohu.com']
    start_urls = ['http://news.sohu.com/']
    #oldTime=''

class SznewsDynamicSpider(DynamicSpider):
    name='sznewsDynamic'
    allowed_domains=['sznews.com']
    start_urls = ['http://www.sznews.com/']
    #oldTime=''

class WangyiDynamicSpider(DynamicSpider):
    name='wangyiDynamic'
    allowed_domains=['163.com']
    start_urls = ['http://news.163.com/']
    #oldTime=''
    def isNews(self,url):
        result=re.search('/(\d{2})/([01]\d)([0123]\d)/',url)
        if result:
            return '20'+result.group(1)+result.group(2)+result.group(3)

class XinhuanetDynamicSpider(DynamicSpider):
    name='xinhuanetDynamic'
    allowed_domains=["xinhua.com","news.cn"]
    start_urls = ["http://www.xinhuanet.com"]
    deny_domains=['sike\.news\.cn','info\.search\.news\.cn','qnssl\.com','game\.news\.cn']+DynamicSpider.deny_domains
    #oldTime=''
    
process = CrawlerProcess({
    'ITEM_PIPELINES' : {
        #'scrapy.pipelines.images.ImagesPipeline': 1,
        #'news.pipelines.JsonPipeline': 300,
    },
    'AUTOTHROTTLE_ENABLED':True,
    #'LOG_LEVEL' : 'INFO',
    'CONCURRENT_REQUESTS':100,
    'REACTOR_THREADPOOL_MAXSIZE': 20,
    'COOKIES_ENABLED': False,
    'RETRY_ENABLED':True,#
    'DOWNLOAD_TIMEOUT': 15,
    'REDIRECT_ENABLED': False,
    })

process.crawl(ChinanewsDynamicSpider)
process.crawl(ChinaDynamicSpider)
process.crawl(IfengDynamicSpider)
process.crawl(PeopleDynamicSpider)
process.crawl(QQDynamicSpider)
process.crawl(SinaDynamicSpider)
process.crawl(SohuDynamicSpider)
process.crawl(SznewsDynamicSpider)
process.crawl(WangyiDynamicSpider)
process.crawl(XinhuanetDynamicSpider)
process.start()
