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
        curDate=time.strftime('%Y%m%d',time.localtime(time.time()))
        curTime=time.strftime('%Y%m%d',time.localtime(time.time()))
        if not os.path.exists('data/'+curDate):
            os.mkdir('data/'+curDate)
        self.news=open('data/'+curDate+'/'+curTime,'w')

    def process_item(self, item, spider):
        if item['title']:
            deli='\t'
            #self.news.write((item['url']+deli+item['title']+deli+item['time']+deli+item['label']+deli+item['readNum']+deli+item['replayNum']+deli+item['contentWithImg']+'\n').encode('u8'))
            return item
        else:
            raise DropItem("Missing")
