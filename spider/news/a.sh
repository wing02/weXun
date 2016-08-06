#!/bin/sh
time=`date "+%Y%m%d%H"`
cd /home/lab401/Project/weXun/spider/news
python allStatic.py 2> ./log/`date "+%Y%m%d%H%M%S"`
python after.py $time
