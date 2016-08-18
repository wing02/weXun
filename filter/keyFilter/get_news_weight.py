#!/bin/python
#encoding=utf-8
from __future__ import (division,absolute_import,print_function,unicode_literals)

from filter.keyFilter.tfidf_get_news_keyword import tfidf_keyword
import sys
try:
        reload(sys)
        sys.setdefaultencoding('utf-8')
except:
        pass
        
prePath='filter/keyFilter/data/'

def read_words(filename):
    fo = open(filename, 'r')
    list=[]
    for line in fo.readlines():
        list.append(line.strip('\r\n'))
    fo.close()
    return list
    
title=u"菲外长：中菲一致同意在南海仲裁案后不做挑衅性声明"
label=u"新闻频道"
text=u'菲律宾新旧两任总统对待中国态度有明显不同{p}据BBC中文网消息，菲律宾外交部长亚赛8日在接受法新社采访时表示，菲律宾即使下周赢了南海仲裁案，也愿意同中国分享南海争议地区的自然资源。{p}亚赛说，杜特尔特总统领导的政府希望在12日仲裁判决后迅速开始同中国直接会谈，谈判内容包括在菲律宾的专属经济区内联合利用天然气资源和渔场。{p}亚赛说，我们甚至要探索如何联合勘探有关地区，如何能够从有争议的专属经济区共同受益。{p}在阿基诺领导时期，菲律宾向海牙国际仲裁法院提交了诉讼，挑战中国南海主权。{p}此举激怒了中国，中方一再表示不会理睬仲裁。近日，中国在南海北部举行了军事演习。{p}不过，自杜特尔特在6月30日担任菲律宾总统后，摆出了更加和解的姿态。{p}前任总统阿基诺拒绝同中国展开直接谈判，还把中国在南海的行为同纳粹德国在二战前在欧洲的扩张相提并论。{p}亚赛8日表示，杜特尔特不会做类似比喻，并且强调新菲律宾政府要谋求确保同中国尽可能建立最好的关系。{p}他还表示，中国和菲律宾一致同意，在南海仲裁判决做出后，双方不做任何挑衅性声明。他说菲律宾届时会仔细研究判决，并且同盟友协商，然后尽早同中国展开会谈。{p}亚赛说，菲律宾在分享具有丰富渔业资源的黄岩岛问题上持开放态度，菲律宾称黄岩岛位于其专属经济区，但2012年开始被中国控制。{p}亚赛说，菲律宾还会考虑在菲律宾专属经济区内的礼乐滩的天然气资源问题上同中国合作进行联合勘探。不过他坚持说菲律宾不会放弃任何属于自己的海洋权利。{p}杜特尔特和亚赛7日会见了中国驻菲律宾大使赵鉴华。8日赵鉴华大使又在菲律宾外交部现身。{p}另据观察者网此前报道，菲律宾新总统杜特尔特5日表示，如果南海仲裁案的结果对菲律宾有利，他已经准备好和中国对话，避免战争'


def json_keywords(title,label,text):
        #news_keyword_dict=get_news_keyword(title,text)
        news_keyword_dict=tfidf_keyword(title,text)  #import tfidf
        news_keyword_list=news_keyword_dict.items()
        first=''
        head1=''
        head2=''

        if len(news_keyword_list)==0:
            print ('error')
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
                        news_keyword_list.remove(first)
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

            news_keyword_list=news_keyword_list[:15]

        return head1,head2,news_keyword_list

#json_keywords('news20160728.json','keywordtesttfidf.txt')

if __name__=='__main__':
    print ("title:",title)
    print ("label:",label)
    h1,h2,li=json_keywords(title,label,text)
    print ("head1:",h1)
    print ("head2:",h2)
    print (li)
    for key in li:
        print (key[0]+':'+str(key[1])),
    print ('')




