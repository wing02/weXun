# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exceptions import DropItem
import time
import os

class TutorialPipeline(object):
    def __init__(self):
        fileName=time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))
        if not os.path.exists('data/'+fileName):
            os.mkdir('data/'+fileName)
        self.people=open('data/'+fileName+'/people.data','w')

    def process_item(self, item, spider):
        if item['title']:
            deli='\t'
            self.people.write((item['url']+deli+item['title']+deli+item['time']+deli+item['label']+deli+item['readNum']+deli+item['replayNum']+deli+item['contentWithImg']+'\n').encode('u8'))
            return item
        else:
            raise DropItem("Missing")
