# -*- coding=utf-8 -*-
import MySQLdb
import time
import pdb
import sys
import json
import re
import logging
import glob
#from uniq.simhash.uniquer import Uniquer
from uniq.simhash import getSimhash

srcPath='../data/20160807/qq/233836.json'
paths=glob.glob(srcPath)
#uniquer=Uniquer()
simhashs=dict()

fout=open('test.log','w')
for path in paths:
    f=open(path)
    for line in f:
        item=json.loads(line)
        content=item['contentWithImg']
        content=re.sub('{img}|{p}','',content)
        content=item['title']
        simLong=getSimhash.getSimhash(content.encode('u8'))
        for sim in simhashs:
            if getSimhash.isEqual(sim,simLong):
                fout.write((item['url']+'\t'+simhashs[simLong]['url']+'\t').encode('u8'))
                fout.write((item['title']+'\t'+simhashs[simLong]['title']+'\n').encode('u8'))
        simhashs[simLong]=item
        #print simLong
fout.close()
f.close()