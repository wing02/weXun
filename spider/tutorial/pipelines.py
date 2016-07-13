# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exceptions import DropItem

class TutorialPipeline(object):
    def __init__(self):
        self.people=open('data/people.data','wb')

    def process_item(self, item, spider):
        if item['title']:
            deli='\t'
            self.people.write((item['url']+deli+item['title']+deli+item['date']+deli+item['time']+deli+item['label']+deli+item['contentWithImg']+'\n').encode('u8'))
            #self.people.write((item['title']+deli+item['url']+deli+item['date']+deli+item['time']+deli+item['label']+deli+item['content']+deli+item['contentWithImg']+'\n').encode('u8'))
            return item
        else:
            raise DropItem("Missing")
