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
from news.spiders.newsParser import NewsParser
import urllib2
from bs4 import BeautifulSoup
import json

class QQOnceSpider(scrapy.Spider):
    name='qqOnce'
    allowed_domains=["qq.com"]
    start_urls = ["http://news.qq.com/a/20160725/029157.htm"]
    curTime=time.time()

    def parse(self, response):
        return QQParser(response).getNewsItem()

class QQParser(NewsParser):

    def getReplayNum(self):
        try:
            cmtId=self.response.selector.re('cmt_id = (\d+)')[0]
            cmtJs=urllib2.urlopen('http://coral.qq.com/article/'+cmtId+'/commentnum')
            cmt=json.load(cmtJs)
            self.item['replayNum']=cmt['data']['commentnum']
        except:
            pass

    def getContentImg(self):
        if self.response.selector.re(u'幻灯播放'):
            js=urllib2.urlopen(re.search('.*\.',self.response.url).group()+'hdBigPic.js').read().replace('&nbsp;',' ')
            self.item['image_urls']=re.findall('''http://[^']*\.jpg''',js)
            newJs=re.sub('''http://[^']*\.jpg''','{img}',js)
            self.item['contentWithImg']=re.sub('</?p>','',''.join(re.findall('<p>.*?</p>|{img}',newJs))).decode('gbk')
        else:
            tex=QQTextExtract(self.response.body_as_unicode())
            self.item['contentWithImg']=tex.content
            self.item['image_urls']=map(self.fillPath,tex.imgs)



class QQTextExtract(TextExtract):
    def remove_tags(self):
        self.text_body = self.re_doc_type.sub('', self.text_body)
        self.text_body = self.re_js.sub('', self.text_body)
        self.text_body = self.re_css.sub('', self.text_body)
        self.text_body = self.re_special.sub('', self.text_body)
        self.text_body = re.sub('((<[^>]*>)*<!--/?keyword-->(<[^>]*>)*)','',self.text_body)
        self.text_body = self.re_comment.sub('', self.text_body)
        self.replaceImg()
        if self.doRemoveLF:
            self.text_body = self.text_body.replace('\r\n','').replace('\n','')
        self.text_body = self.re_p.sub('{p}', self.text_body)
