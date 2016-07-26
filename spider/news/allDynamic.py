import scrapy
from scrapy.crawler import CrawlerProcess
from news.spiders.dynamicSpider import DynamicSpider
import time
import os
import os.path as osp

class BBCDynamicSpider(DynamicSpider):
    name='bbcDynamic'
    allowed_domains=["www.bbc.com"]
    start_urls = ["http://www.bbc.com/zhongwen/simp"]
    oldTime=''

class ChinaDynamicSpider(DynamicSpider):
    name='chinaDynamic'
    allowed_domains=['china.com']
    start_urls = ['http://news.china.com/']
    oldTime=''

class ChinanewsDynamicSpider(DynamicSpider):
    name='chinanewsDynamic'
    allowed_domains=['chinanews.com']
    start_urls = ['http://www.chinanews.com/']
    oldTime=''
    
class IfengDynamicSpider(DynamicSpider):
    name='ifengDynamic'
    allowed_domains=['news.ifeng.com']
    start_urls = ['http://news.ifeng.com/']
    oldTime=''

class PeopleDynamicSpider(DynamicSpider):
    name='peopleDynamic'
    allowed_domains=["people.com.cn"]
    start_urls = ["http://www.people.com.cn"]
    oldTime=''

class QQDynamicSpider(DynamicSpider):
    name='qqDynamic'
    allowed_domains=["qq.com"]
    start_urls = ["http://news.qq.com/"]
    deny_domains=["v.qq.com","class.qq.com","club.auto.qq.com","db.house.qq.com","t.qq.com"]
    curTime=time.time()
    oldTime=''

class SinaDynamicSpider(DynamicSpider):
    name='sinaDynamic'
    allowed_domains=["sina.com.cn"]
    start_urls = ["http://news.sina.com.cn/"]
    oldTime=''

class SohuTmpDynamicSpider(DynamicSpider):
    name='sohuDynamic'
    allowed_domains=['news.sohu.com']
    start_urls = ['http://news.sohu.com/']
    oldTime=''

class SznewsDynamicSpider(DynamicSpider):
    name='sznewsDynamic'
    allowed_domains=['sznews.com']
    start_urls = ['http://www.sznews.com/']
    oldTime=''

class WangyiDynamicSpider(DynamicSpider):
    name='wangyiDynamic'
    allowed_domains=['news.163.com']
    start_urls = ['http://news.163.com/']
    oldTime=''

class XinhuanetDynamicSpider(DynamicSpider):
    name='xinhuanetDynamic'
    allowed_domains=["xinhua.com","news.cn"]
    start_urls = ["http://www.xinhuanet.com"]
    deny_domains=['sike\.news\.cn','info\.search\.news\.cn','qnssl\.com']
    oldTime='20160725154342'
    
process = CrawlerProcess({
    })
process.crawl(BBCDynamicSpider)
process.crawl(ChinanewsDynamicSpider)
process.crawl(ChinaDynamicSpider)
process.crawl(IfengDynamicSpider)
process.crawl(PeopleDynamicSpider)
process.start()
