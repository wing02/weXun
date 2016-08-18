#coding=utf8
from __future__ import (division,absolute_import,print_function,unicode_literals)
import conf
import json
import re



class Item:
    def __init__(self,db,tfs,tableName,result):
        self.db=db
        self.cursor=self.db.cursor()
        self.tableName=tableName
        self.tfs=tfs

        self.id=result[0]
        self.dataTfsName=result[1]
        self.title=result[2]
        self.flag=result[3]
        self.label=result[4]
    
    def getImgs(self):
        try:
            return self.imgDatas
        except:
            self.imgDatas=[]
            imgSrcs=re.findall('src=([^>]*)',self.data)
            for imgSrc in imgSrcs:
                self.imgDatas.append(self.tfs.get(imgSrc[-18:]))
            return self.imgDatas

    def getTxt(self):
        try:
            return self.txtData
        except:
            self.txtData=re.sub('<[^>]*','',self.getData())
            return self.txtData

    def getData(self):
        try:
            return self.data
        except:
            self.data=self.tfs.get(self.dataTfsName)
            return self.data
        

    def toDb(self):
        if self.keywords:
            keyLine=json.dumps(self.keywords, ensure_ascii=False)
            sql='''UPDATE %s SET keys_data='%s' , news_flag='%s' , head1='%s' , head2='%s' WHERE news_id=%s'''%(self.tableName,keyLine,self.flag,self.head1,self.head2,self.id)
        else:
            sql='''UPDATE %s SET news_flag='%s' WHERE news_id=%s'''%(self.tableName,self.flag,self.id)
        try:
            self.cursor.execute(sql.encode('u8'))
            self.db.commit()
        except Exception,e:
	    self.db.rollback()
            print ("Error: %s"%(sql))
	    print (e)
