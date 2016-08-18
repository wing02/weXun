#coding=utf8
from __future__ import (division,absolute_import,print_function,unicode_literals)
import conf
from filter.dataInserter import DataInserter
from filter.filterSet import FilterSet
from filter.keyFilter.keyFilter import keyFilter

if __name__=="__main__":
    update_time='20160817232230'
    #dataInserter=DataInserter(update_time)
    #dataInserter.insertFromRexpath('spider/data/20160817/*/*.json')
    filterSet=FilterSet(update_time)
    filterSet.append(keyFilter)
    filterSet.start()
