# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exceptions import DropItem
import time
import os
import os.path as osp
import codecs
import json
import logging
from integra import Integra

class JsonPipeline(object):
    def open_spider(self,spider):
        self.savePath='../data'
        self.spiderName=spider.name
        curDate=time.strftime('%Y%m%d',time.localtime(time.time()))
        curTime=time.strftime('%H%M%S',time.localtime(time.time()))
        self.dirPath=osp.join(self.savePath,curDate,self.spiderName)
        self.FileName=osp.join(self.dirPath,curTime+'.json')
        if not osp.isdir(self.dirPath):
            os.makedirs(self.dirPath)
        self.news = codecs.open(self.FileName,'wb',encoding='utf-8')

        self.oCaIs=['china']
        self.aCaIs=['people','xinhuanet','sohu','qq','wangyi','sina']

    def process_item(self, item, spider):
        try:
            item.pop('image_urls')
            for image in item['images']:
                if not self.dirPath==image['path'][:len(self.dirPath)]:
                    image['path']=osp.join(self.dirPath,image['path'])
        except:
            pass
        line = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.news.write(line)
        return item

    def close_spider(self, spider):
        self.news.close()
        if spider.name in self.oCaIs:
            Integra(self.FileName).writeFile(self.FileName,'oCaI')
        elif spider.name in self.aCaIs:
            Integra(self.FileName).writeFile(self.FileName,'aCaI')

