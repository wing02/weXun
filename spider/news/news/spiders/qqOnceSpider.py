# -*- coding: utf-8 -*-
from scrapy import signals
from pydispatch import dispatcher
import time
import scrapy
import re
import cPickle
import os
import os.path as osp
from news.items import NewsItem
from news.spiders.myExt import TextExtract
import urllib2
from bs4 import BeautifulSoup
import json

class QQOnceSpider(scrapy.Spider):
    name='qqOnce'
    allowed_domains=["qq.com"]
    start_urls = ["http://news.qq.com/a/20160725/042654.htm"]
    curTime=time.time()

    def parse(self, response):
        return parseQQNews(self,response)

    def getPrePath(self,url):
        return re.search('(.*/)',url).group(1)

def parseQQNews(spider,response):
    prePath=spider.getPrePath(response.url)
    item = NewsItem()

    item['url']=response.url

    titles=re.split('_',response.xpath('/html/head/title/text()').extract()[0].strip('\r\n'))
    item['title']=titles[0].encode('u8')

    item['label']=titles[1]

    item['keyWords']=''.join(response.xpath('/html/head/meta[@name="keywords"]/@content').extract()).strip('\r\n')

    item['source']=''.join(response.xpath('//span[@id="source"]/text()').extract()).strip('\r\n')
    
    newsTime=''.join(response.selector.re(u'(\d+)[年-](\d+)[月-](\d+)日?\s*(\d+):(\d+):?(\d+)?'))
    item['time']=newsTime[:14]
    if len(item['time'])==12:
        item['time']+='00'
    elif item['time']=='':
        item['time']=''.join(response.xpath('//meta[@name="pubdate"]/@content').re(u'(\d+)-(\d+)-(\d+).*?(\d+):(\d+):(\d+)'))
        if item['time']=='':
            item['time']=time.strftime('%Y%m%d%H%M%S',time.localtime(spider.curTime))

    try:
        cmtId=response.selector.re('cmt_id = (\d+)')[0]
        cmtJs=urllib2.urlopen('http://coral.qq.com/article/'+cmtId+'/commentnum')
        cmt=json.load(cmtJs)
        item['replayNum']=cmt['data']['commentnum']
    except:
        pass

    if response.selector.re(u'幻灯播放'):
        js=urllib2.urlopen(re.search('.*\.',response.url).group()+'hdBigPic.js').read().replace('&nbsp;',' ')
        item['image_urls']=re.findall('''http://[^']*\.jpg''',js)
        newJs=re.sub('''http://[^']*\.jpg''','IMG0$',js)
        item['contentWithImg']=re.sub('</?p>','',''.join(re.findall('<p>.*?</p>|IMG0\$',newJs))).decode('gbk')
    else:
        tex=TextExtract(response.body_as_unicode())
        item['contentWithImg']=tex.content
        item['image_urls']=map(lambda url:url if re.search('^http',url) else prePath+url,tex.imgs)

    return item


    
