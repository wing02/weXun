import scrapy
from scrapy.crawler import CrawlerProcess
from news.spiders.dynamicSpider import DynamicSpider
import time
import os
import os.path as osp
import re

class BBCDynamicSpider(DynamicSpider):
    name='bbcDynamic'
    allowed_domains=["www.bbc.com"]
    start_urls = ["http://www.bbc.com/zhongwen/simp"]
    oldTime=''
    def isNews(self,url):
        result=re.search('/(20\d{2})/([01]\d)/\d{4}([0123]\d)',url)
        if result:
            return result.group(1)+result.group(2)+result.group(3)
    def getPrePath(self,url):
        return re.search('(https?://.*?)/',url).group(1)

class ChinaDynamicSpider(DynamicSpider):
    name='chinaDynamic'
    allowed_domains=['china.com']
    start_urls = ['http://news.china.com/']
    oldTime=''
    def getPrePath(self,url):
        return re.search('(.*/)',url).group(1)

class ChinanewsDynamicSpider(DynamicSpider):
    name='chinanewsDynamic'
    allowed_domains=['chinanews.com']
    start_urls = ['http://www.chinanews.com/']
    oldTime=''
    def getPrePath(self,url):
        return re.search('(https?://.*?)/',url).group(1)
    
class IfengDynamicSpider(DynamicSpider):
    name='ifengDynamic'
    allowed_domains=['news.ifeng.com']
    start_urls = ['http://news.ifeng.com/']
    oldTime=''
    def getPrePath(self,url):
        return re.search('(https?://.*?)/',url).group(1)

class PeopleDynamicSpider(DynamicSpider):
    name='peopleDynamic'
    allowed_domains=["people.com.cn"]
    start_urls = ["http://www.people.com.cn"]
    oldTime=''
    def getPrePath(self,url):
        return re.search('(.*/)',url).group(1)

class QQDynamicSpider(DynamicSpider):
    name='qqDynamic'
    allowed_domains=["qq.com"]
    start_urls = ["http://news.qq.com/"]
    deny_domains=["v.qq.com","class.qq.com","club.auto.qq.com","db.house.qq.com","t.qq.com"]
    curTime=time.time()
    oldTime=''
    def getPrePath(self,url):
        return re.search('(.*/)',url).group(1)

class SinaDynamicSpider(DynamicSpider):
    name='sinaDynamic'
    allowed_domains=["sina.com.cn"]
    start_urls = ["http://news.sina.com.cn/"]
    oldTime=''
    def getPrePath(self,url):
        return re.search('(https?://.*?)/',url).group(1)

class SohuDynamicSpider(DynamicSpider):
    name='sohuDynamic'
    allowed_domains=['news.sohu.com']
    start_urls = ['http://news.sohu.com/']
    oldTime=''
    def getPrePath(self,url):
        return re.search('(https?://.*?)/',url).group(1)

class SznewsDynamicSpider(DynamicSpider):
    name='sznewsDynamic'
    allowed_domains=['sznews.com']
    start_urls = ['http://www.sznews.com/']
    oldTime=''
    def getPrePath(self,url):
        return re.search('(.*/)',url).group(1)

class WangyiDynamicSpider(DynamicSpider):
    name='wangyiDynamic'
    allowed_domains=['news.163.com']
    start_urls = ['http://news.163.com/']
    oldTime=''
    def getPrePath(self,url):
        return re.search('(.*/)',url).group(1)

class XinhuanetDynamicSpider(DynamicSpider):
    name='xinhuanetDynamic'
    allowed_domains=["xinhua.com","news.cn"]
    start_urls = ["http://www.xinhuanet.com"]
    deny_domains=['sike\.news\.cn','info\.search\.news\.cn','qnssl\.com']
    oldTime=''
    def getPrePath(self,url):
        return re.search('(.*/)',url).group(1)
    
process = CrawlerProcess({
    })
process.crawl(BBCDynamicSpider)
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
