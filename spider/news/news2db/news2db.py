# -*- coding=utf-8 -*-
import MySQLdb
import time
import pdb
import sys
import re
import os
import json
import hashlib
import conf

class News2Db:
    
    def __init__(self):
        self.db = MySQLdb.connect("localhost",conf.dbUser,conf.dbPasswd,conf.dbName )
        self.cursor = self.db.cursor()
        self.jsKeys=[
                'url',
                'title',
                'contentWithImg',
                #'images',
                #'label',
                'time',
                'keyWords',
                #'replayNum',
                #'readNum',
                ]
        self.dbKeys=[
                'news_resource_link',
                'news_title',
                'news_data',
                #'news_imgs',
                #'news_type',
                'news_time',
                'news_keys',
                #'news_resource_comment_num',
                #'news_resource_click_num',
                ]

    def __del__(self):
        self.db.close()
        #print "Close"

    def insertJson(self,jsonFile):
        dirPath=re.search('(.*)\.json$',jsonFile).group(1)+'Content'
        if not os.path.isdir(dirPath):
            os.makedirs(dirPath)

        #write content to small file
        f=open(jsonFile)
        for line in f:
            item=json.loads(line)
            self.insertItem(item,dirPath)

    def insertItem(self,item,dirPath):
        fileName=self.calcSha1(item['title'])
        fullPath=os.path.join(dirPath,fileName)
        #while os.path.isfile(fullPath):
        #    fileName=self.calcSha1(fileName)
        #    fullPath=os.path.join(dirPath,fileName)
        with open(fullPath,'w') as content:
            content.write(item['contentWithImg'].encode('u8'))
            content.write('\n')
            for image in item['images']:
                content.write(image["path"])
                content.write('\t')
        item['contentWithImg']=fullPath
        item['time']=item['time'][2:]
        item['keyWords']=item['keyWords'][:50]
        for jsKey in self.jsKeys:
            if not jsKey in item:
                item[jsKey]=''

            sql=''' INSERT INTO News(%s) VALUES('%s')'''%(','.join(self.dbKeys),"','".join(map(lambda x:item[x],self.jsKeys)))
            #print sql
            try:
                self.cursor.execute(sql)
                self.db.commit()
            except:
                self.db.rollback()

    def calcSha1(self,content):
        sha1Obj=hashlib.sha1()
        sha1Obj.update(content.encode('u8'))
        return sha1Obj.hexdigest()




if __name__=="__main__":
    news2Db=News2Db()
    news2Db.insertJson("../data/20160806/sznews/183646.json")
