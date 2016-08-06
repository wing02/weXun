# -*- coding=utf-8 -*-
from uniq.simhash.uniquer import Uniquer
from wordCensor.wordCensor import Trie
from news2db.news2db import News2Db
import sys
import glob
import re
import os
import time

if __name__ =="__main__":
    shellTime=sys.argv[1]
    newsFiles=glob.glob('../data/'+shellTime[:8]+'/*/'+shellTime[8:10]+'*.json')
    triePath='wordCensor/sensitive.pkl'

    uniquer=Uniquer()
    news2db=News2Db()
    trie=Trie.loadTrie(triePath)
    
    curTime=time.time()
    for newsFile in newsFiles:

        dirPath=re.search('(.*)\.json$',newsFile).group(1)+'Content'
        if not os.path.isdir(dirPath):
            os.makedirs(dirPath)

        for item in uniquer.checkFile(newsFile,True):
            content=re.sub('{img}|{p}','',item['contentWithImg'])
            result=trie.hasSensi(content)
            if result:
                print result[0]
                continue
            else:
                news2db.insertItem(item,dirPath)

    print time.time()-curTime
