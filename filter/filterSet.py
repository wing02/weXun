#coding=utf8
from __future__ import (division,absolute_import,print_function,unicode_literals)
import conf
import sys
import os.path as osp
import MySQLdb
import pytfs
from filter.keyFilter.keyFilter import keyFilter

class FilterSet:
    def __init__(self,updateTime):
        self.filters=[]
        self.dbIp=conf.dbIp
        self.dbUser=conf.dbUser
        self.dbPasswd=conf.dbPasswd
        self.dbName=conf.dbName
        self.tableName=conf.tableName
        self.updateTime=updateTime
        self.tfsUrl='%s:%s'%(conf.dbIp,conf.tfsPort)
    
    def append(self,filter):
        self.filters.append(filter)

    def start(self):
        self.db = MySQLdb.connect(self.dbIp,self.dbUser,self.dbPasswd,self.dbName, charset='utf8')
        self.cursor = self.db.cursor()
        sql='SELECT news_id,news_data,news_title,news_flag,news_label FROM %s WHERE updata_time=%s'%(self.tableName,self.updateTime)
        try:
            cursor.execute(sql.encode('u8'))
            self.results=cursor.fetchall()
        except:
            print "Error: unable to fetch data"
        self.db.close()
        self.doFilter()

    def doFilter(self):
        filterInsts=[]
        for filter in self.filters:
            filterInsts.append(filter())
        db = MySQLdb.connect(self.dbIp,self.dbUser,self.dbPasswd,self.dbName, charset='utf8')
        tfs = pytfs.TfsClient()
        tfs.tfs_init(self.tfsUrl)
        item=Item(db,tfs,self.tableName)
        for result in self.results:
            item.setItem(result)
            for filterInst in filterInsts:
                filterInst.doFilter(item)
        db.close()

        

if __name__=="__main__":
    filter=Filter()
    filter.append(keyFilter)
    filter.doFilter()
