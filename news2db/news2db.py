# -*- coding=utf-8 -*-
import getSimhash
import MySQLdb
import time
import pdb
import sys

class News2Db:
    
    def __init__(self):
        self.db = MySQLdb.connect("localhost","wexun","wexun","test" )
        self.cursor = self.db.cursor()
        self.jsKeys=['url','title','contentWithImg','images','label','time','keyWords']
        self.dbKeys=['news_resource_link','news_title','news_data','news_imgs','']

    def __del__(self):
        self.db.close()

    def insertJson(self,filePath):
        f=open(filePath)
        cutPath=filePath.split('/')
        dirName=cutPath[-1].split('.')[0]+'dir' 
        agencyName=cutPath[-2]
        dirPath='/'.join(cutPath[:-1])+'/'+dirName
        if not os.path.isdir(dirPath):
            os.makedirs(dirPath)
        for line in f:
            news=json.loads(line)
            fileName=self.calcSha1(news['title'])
            
            sql=''' INSERT INTO News(%s) VALUES('%s')'''%(','.join(self.dbKeys),"','".join(map(lambda x:news[x],self,jsKeys)))

    def calcSha1(self,content):
        sha1Obj=hashlib.sha1()
        sha1Obj.update(content)
        return sha1Obj.hexdigest()




if __name__=="__main__":
    news2Db=News2Db()
    news2Db.insertJson("test.json")


