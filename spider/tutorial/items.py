# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class PeopleItem(scrapy.Item):
    url=scrapy.Field()
    title=scrapy.Field()
    content=scrapy.Field()
    contentWithImg=scrapy.Field()
    date=scrapy.Field()
    time=scrapy.Field()
    label=scrapy.Field()
    source=scrapy.Field()

#class DmozItem(scrapy.Item):
#    title=scrapy.Field()
#    link=scrapy.Field()
#    desc=scrapy.Field()
    # define the fields for your item here like:
    # name = scrapy.Field()

