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

class Sharer:
    def __init__(self):
        self.dbIp=conf.dbIp
        self.dbUser=conf.dbUser
        self.dbPasswd=conf.dbPasswd
        self.dbName=conf.dbName
        self.tableName=conf.tableName
        self.db = MySQLdb.connect(self.dbIp,self.dbUser,self.dbPasswd,self.dbName, charset='utf8')
        self.cursor = self.db.cursor()

    def __del__(self):
        self.db.close()

    def doShare(self,tableName,updateTime):
        if tableName='news':
            sql='''INSERT INTO news(news_id,agency_name,news_time,news_data,news_imgs,news_title,news_abstract) SELECT news_id,agency_name,news_time,news_data,news_imgs,news_title,news_abstract FROM tmp_news WHERE update_time=%s '''%(updateTime)
        elif tableName='rec_news':
            sql='''INSERT INTO news(id,title,update_time,type,agency,head1,head2,key_data,label_data) SELECT news_id,news_title,update_time,news_type,agency_name,head1,head2,keys_data,news_label FROM tmp_news WHERE update_time=%s '''%(updateTime)
        else:
            print ("Error: no this tableName")

        sql=sql.encode('u8')
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except MySQLdb.Error,e:
            self.db.rollback()
            print ("MySQL Error:%s"%str(e))
            print (sql)
