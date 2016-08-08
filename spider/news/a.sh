#!/bin/sh
time=`date "+%Y%m%d%H"`
cd /home/lab401/Project/weXun/spider/news
python allStatic.py 2> ./log/$time
python after.py $time 2>> ./log/$time
