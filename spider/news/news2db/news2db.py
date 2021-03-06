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
        self.db = MySQLdb.connect("localhost",conf.dbUser,conf.dbPasswd,conf.dbName, charset='utf8')
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

        item['keyWords']=item['keyWords'][:33]

        item['title']=item['title'][:33]

        result=re.search('(.*?)\?',item['url'])
        if result:
            item['url']=result.group(1)

        for jsKey in self.jsKeys:
            if not jsKey in item:
                item[jsKey]=''

        sql=''' INSERT INTO news(%s) VALUES('%s')'''%(','.join(self.dbKeys),"','".join(map(lambda x:self.escape(item[x]),self.jsKeys)))
        sql=sql.encode('u8')
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except MySQLdb.Error,e:
            self.db.rollback()
            print "MySQL Error:%s"%str(e)
            print sql

    def calcSha1(self,content):
        sha1Obj=hashlib.sha1()
        sha1Obj.update(content.encode('u8'))
        return sha1Obj.hexdigest()

    def escape(self,content):
        return re.sub("'",r"\'",content)



if __name__=="__main__":
    news2Db=News2Db()
    news2Db.insertJson("../data/20160806/sznews/183646.json")
