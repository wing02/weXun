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
        for line in f:
            js=json.loads(line)
            sql=''' INSERT INTO News(


if __name__=="__main__":
    news2Db=News2Db()
    news2Db.insertJson("test.json")


