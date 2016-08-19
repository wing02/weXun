#coding=utf8
from __future__ import (division,absolute_import,print_function,unicode_literals)
import conf
from filter.dataInserter import DataInserter
from filter.filterSet import FilterSet
from filter.keyFilter.keyFilter import keyFilter
from filter.sharer import Sharer
import time

if __name__=="__main__":
    start=time.clock()
    update_time='20160817232230'
    dataInserter=DataInserter(update_time)
    dataInserter.insertFromRexpath('spider/data/20160817/*/*.json')
    filterSet=FilterSet(update_time)
    filterSet.append(keyFilter)
    filterSet.start()

    tableName='rec_news'
    updateTime='20160818230000'
    sharer=Sharer()
    sharer.doShare(tableName,updateTime)
    end=time.clock()
    print (end-start)
