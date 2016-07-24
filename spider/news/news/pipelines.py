# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exceptions import DropItem
import time
import os
import os.path as osp

class NewsPipeline(object):
    def __init__(self):
        self.savePath='../data'
        self.spiderName=os.getenv('SPIDER_NAME','defaultPipe')
        #self.spiderName='xinhua'
        curDate=time.strftime('%Y%m%d',time.localtime(time.time()))
        curTime=time.strftime('%H%M%S',time.localtime(time.time()))
        self.dirPath=osp.join(self.savePath,curDate,self.spiderName)
        if not osp.isdir(self.dirPath):
            os.makedirs(self.dirPath)
        self.news=open(osp.join(self.dirPath,curTime),'w')

    def process_item(self, item, spider):

        keys=['time','url','title','label','keyWords','source','readNum','replayNum','images','contentWithImg']
        for key in keys:
            if not key in item:
                item[key]=''

        for image in item['images']:
            image['path']=osp.join(self.dirPath,image['path'])
            

        if item['title']:
            line=self.connItem(item,keys,';\t')
            self.news.write(line)
            return item
        else:
            raise DropItem("Missing")

    def connItem(self,item,keys,deli):
        values=map(lambda key:item[key] if key != 'images' else str(item[key]),keys)
        return (deli.join(values)+'\n').encode('u8')
