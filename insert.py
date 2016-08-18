#coding=utf8
from __future__ import (division,absolute_import,print_function,unicode_literals)
import conf
from filter.dataInserter import DataInserter

if __name__=="__main__":
    update_time='20160817232230'
    dataInserter=DataInserter(update_time)
    dataInserter.insertFromRexpath('spider/data/20160817/*/*.json')
