# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class NewsItem(scrapy.Item):
    url=scrapy.Field()
    title=scrapy.Field()
    contentWithImg=scrapy.Field()
    time=scrapy.Field()
    label=scrapy.Field()
    keyWords=scrapy.Field()
    source=scrapy.Field()
    readNum=scrapy.Field()
    replayNum=scrapy.Field()
    image_urls=scrapy.Field()
    images=scrapy.Field()
