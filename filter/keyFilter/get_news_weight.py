#!/bin/python
#encoding=utf-8
from __future__ import (division,absolute_import,print_function,unicode_literals)
from filter.keyFilter.tfidf_get_news_keyword import tfidf_keyword
import sys
prePath='filter/keyFilter/data/'
try:
        reload(sys)
        sys.setdefaultencoding('utf-8')
except:
        pass

title=u"湖南省茶博会9月2日开幕 八大茶主题活动等您来“品”"
label=u"湖南频道"
text=u"人民网长沙8月18日电 今天湖南省湖南协会发布消息，2016第八届湖南茶业博览会将于9月2日至5日在长沙红星国际会展中心举行。展位面积达2万平方米，截至目前，2200多个展位已全部预订一空。{up}茶博会组委会办公室主任曹文成介绍：湖南茶业博览会是“展示魅力湘茶、弘扬湘茶文化，发展茶叶经济、扩大茶叶消费”的重要平台，已连续举办了七届。在9月2日至5日茶博会期间，还将组织开展“2016第八届湖南茶业博览会开幕式暨潇湘·石门银峰茶推介会”、“2016湖南茶叶“‘十大公共品牌’、‘十大杰出营销经理人’、‘十强最美茶叶村（茶园）’”与 “第三届湖南‘茶与健康’万人广场舞大赛”等八大主题活动。{up}据介绍，石门县将借助本届茶博会开幕式平台举行潇湘·石门银峰茶推介汇报会。石门县是湖南茶叶主产县，是大湘西茶叶产业发展重点县，石门县人民政府将组织全县茶企走进省会长沙，宣传石门县茶历史、茶文化，推介石门县生态有机茶和石门县改革开放以来取得的成绩，届时将邀请社会各界人士和广大市民共品石门银峰茶。"


def read_words(filename):
    fo = open(filename, 'r')
    list=[]
    for line in fo.readlines():
        list.append(line.strip('\r\n'))
    fo.close()
    return list

def json_keywords(title,label,text):
        #news_keyword_dict=get_news_keyword(title,text)
        news_keyword_dict=tfidf_keyword(title,text)  #import tfidf

        first=''
        head1=''
        head2=''

        if len(news_keyword_dict)==0:
            print ('error')
            return head1, head2, []
        else:
            if label and len(label)<6:
                if label[:2] in [u'凤凰', u'新浪']:
                    first=label[2:4]
                else:
                    first=label[:2]

            #新闻贴标签
            classify_list=['国内','国际','社会','生活','财经','娱乐','体育','科技']
            templist=news_keyword_dict.keys()


            #print first

            if first in classify_list:
                head1=first

            else:
                if first in ['家居','汽车','教育','旅游','健康']:
                    head1=classify_list[3]
                    head2=first
                elif first in ['商讯','经济','金融','理财','投资','股票']:
                    head1=classify_list[4]
                    head2=first
                elif first in ['电视剧','综艺','电影']:
                    head1=classify_list[5]
                    head2=first
                elif first in ['NBA', '奥运','足球']:
                    head1=classify_list[6]
                    head2=first
                elif first in ['互联网', '游戏','数码','手机']:
                    head1=classify_list[7]
                    head2=first
                elif first in ['文化', '历史','社区']:
                    head1=classify_list[2]
                    head2=first
                elif first in ['军事','政治','时政']:
                    foreign_list=read_words(prePath+'foreign.txt')
                    if len(set(templist) & set(foreign_list))>0:
                        head1= classify_list[1]
                    else:
                        head1=classify_list[0]
                    head2=first

                elif first in set(read_words(prePath+'society.txt')):
                    if news_keyword_dict.has_key(first):
                        del news_keyword_dict[first]
                    head1=classify_list[2]
                    head2=first

                elif len(set(templist) & set(read_words(prePath+'domestic.txt')))>0:
                    head1=classify_list[0]
                elif len(set(templist) & set(read_words(prePath+'foreign.txt')))>0:
                    head1=classify_list[1]
                elif len(set(templist) & set(read_words(prePath+'society.txt')))>0:
                    head1=classify_list[2]
                elif len(set(templist) & set(read_words(prePath+'economy.txt'))) > 0:
                    head1=classify_list[4]
                elif len(set(templist) & set(read_words(prePath+'sport.txt'))) > 0:
                    head1=classify_list[6]
                elif len(set(templist) & set(read_words(prePath+'technology.txt'))) > 0:
                    head1=classify_list[7]
                elif len(set(templist) & set(read_words(prePath+'amuse.txt'))) > 0:
                    head1=classify_list[5]
                else:
                    head1=classify_list[3]

            news_keyword_list = news_keyword_dict.items()
            news_keyword_list=news_keyword_list[:15]

        return head1,head2,news_keyword_list

#json_keywords('news20160728.json','keywordtesttfidf.txt')

