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

class XinhuanetStaticSpider(StaticSpider):
    name='xinhuanet'
    allowed_domains=["xinhuanet.com","news.cn"]
    start_urls=cPickle.load(open('../data/chgPage/xinhuanetDynamic_ChgUrl.pkl'))
    deny_domains=[]
    curTime=time.time()
    days=1

    def parseNews(self, response):
        prePath=self.getPrePath(response.url)
        item = NewsItem()

        item['url']=response.url

        item['label']=re.search('//.*?/(\w+)/',response.url).group(1)

        item['title']=response.xpath('/html/head/title/text()').extract()[0].strip('\r\n')

        item['keyWords']=''.join(response.xpath('/html/head/meta[@name="keywords"]/@content').extract()).strip('\r\n')

        item['source']=''.join(response.xpath('//span[@id="source"]/text()').extract()).strip('\r\n')
        
        item['time']=''.join(response.selector.re(u'(\d+)年(\d+)月(\d+)日\s*(\d+):(\d+):(\d+)'))
        if item['time']=='':
            item['time']=''.join(response.xpath('//meta[@name="pubdate"]/@content').re(u'(\d+)-(\d+)-(\d+).*?(\d+):(\d+):(\d+)'))
        if item['time']=='':
            item['time']=time.strftime('%Y%m%d%H%M%S',time.localtime(self.curTime))

        tex=TextExtract(response.body_as_unicode())
        item['contentWithImg']=tex.content
        item['image_urls']=map(lambda url:url if re.search('^http',url) else prePath+url,tex.imgs)

        #imageUrls=response.xpath('//img[@id]/@src').extract()
        #item['image_urls']=map(lambda url:url if re.search('^http',url) else prePath+url,imageUrls)

        #item['contentWithImg']=re.sub(r'<img.[^>]*>','IMG0$',''.join(response.xpath('//div[@class="article"]//p/text()|//img[@id]').extract())).replace('\n','').replace('\r','')

        self.recentUrl[response.url]=int(item['time'])
        return item

name='xinhuanet'
os.environ['SPIDER_NAME']=name

date=time.strftime('%Y%m%d',time.localtime(XinhuanetStaticSpider.curTime))
imageStore=osp.join('../data',date,name)
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

process.crawl(XinhuanetStaticSpider)
process.start()
