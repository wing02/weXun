#coding=utf8
from __future__ import (division,absolute_import,print_function,unicode_literals)
import conf
import sys
import os.path as osp
import MySQLdb
import pytfs
import glob
import json
import re

class DataInserter:
    def __init__(self,updateTime):
        self.filters=[]
        self.dbIp=conf.dbIp
        self.dbUser=conf.dbUser
        self.dbPasswd=conf.dbPasswd
        self.dbName=conf.dbName
        self.tableName=conf.tableName
        self.tfsUrl='%s:%s'%(conf.dbIp,conf.tfsPort)
        self.dataPrePath='spider/news/'
        self.tfsPrePath='http://%s:%s/tfs/'%(conf.dbIp,conf.tfsNginxPort)
        self.updateTime=updateTime

        self.db = MySQLdb.connect(self.dbIp,self.dbUser,self.dbPasswd,self.dbName, charset='utf8')
        self.cursor = self.db.cursor()
        self.tfs = pytfs.TfsClient()
        self.tfs.init(self.tfsUrl)

    def __del__(self):
        self.db.close()

    def insertFromRexpath(self,rexpath):
        for path in glob.glob(rexpath):
            self.insertFromFile(path)

    def insertFromFile(self,filePath):
        f=open(filePath)
        for line in f:
            item=json.loads(line)
            self.insertFromJson(item)
        f.close()

    def insertFromJson(self,jsItem):
        images=jsItem['images']
        imageTfsNames=[]
        subImageTfsNames=[]
        item=dict()

        content=jsItem['contentWithImg']
        #drop news that is too short
        if len(content)>10:
            return
        content='<p>'+re.sub('{u?p}','</p><p>',content)+'</p>'

        for image in images:
            path=self.dataPrePath+image['path']
            with open(path) as f:
                imageTfsNames.append(self.tfs.put(f.read()))

        for imageTfsName in imageTfsNames:
            src=self.tfsPrePath+imageTfsName
            content=re.sub('{img}','<p><img align="center" src="'+src+'"></p>',content,1)
        content=re.sub('{img}','',content)
        item['news_data']=self.tfs.put(content.encode('u8'))

        for i,image in enumerate(images):
            if len(images)==2 and i==1:
                break
            if i==3:
                break
            path=self.dataPrePath+re.sub('full','thumbs/small',image['path'])
            with open(path) as f:
                subImageTfsNames.append(self.tfs.put(f.read()))

        item['news_imgs']=','.join(subImageTfsNames)


        title=re.search('[^|]*',jsItem['title']).group()
        item['news_title']=self.escape(title[:100])

        item['news_resource_link']=re.search('[^?]*',jsItem['url']).group()[:100]
        item['news_time']=jsItem['time']
        item['update_time']=self.updateTime
        item['agency_name']=jsItem['spider'][:20]
        item['news_flag']='unknown'
        item['news_abstract']=self.escape(re.sub('{u?p}|{img}','',jsItem['contentWithImg'])[:255])
        item['news_type']=u'新获取新闻'
        item['news_label']=self.escape(jsItem['label'][:10])

        sql=''' INSERT INTO %s(%s) VALUES('%s')'''%(self.tableName,','.join(item.keys()) ,"','".join(item.values() ) )
        sql=sql.encode('u8')
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except MySQLdb.Error,e:
            self.db.rollback()
            print ("MySQL Error:%s"%str(e))
            print (sql)

    def escape(self,txt):
        tmp=re.sub(r"\\",r"\\\\",txt)
        tmp=re.sub("'",r"\'",tmp)
        return tmp

if __name__=="__main__":
    update_time='20160818112230'
    dataInserter=DataInserter(update_time)
    dataInserter.insertFromRexpath('')
