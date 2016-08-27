# -*- coding=utf-8 -*-
import getSimhash
import MySQLdb
import time
import pdb
import sys
import json
import re
import logging
import conf

class Uniquer(object):

    def __init__(self):
        self.hashLen=16#as hex
        self.db = MySQLdb.connect(conf.dbIp,conf.dbUser,conf.dbPasswd,conf.dbName )
        self.cursor = self.db.cursor()
        #self.distance=3

    def __del__(self):
        self.db.close()

    def checkNews(self,content,add=True):
        try:
            simLong=getSimhash.getSimhash(content.encode('u8'))
        except:
            print content
            return False
        #logging.info(simLong)
        items=[]
        others=[]
        isUnique=True
        itemResults=['']*4

        tmpSimLong=simLong
        for i in range(4):
            items.append(tmpSimLong&((1<<16)-1) )
            tmpSimLong=tmpSimLong>>16

        for i in range(4):
            tmp=(1<<i*16)-1
            result=simLong>>16
            result-=tmp&result
            result|=tmp&simLong
            others.append(result)
            if not self.isUniqueItem(i,items,others,itemResults):
                isUnique=False
                break
        if isUnique:
            if add:
                self.addNews(items,others,itemResults)
            return True
        else:
            return False
    
    def isUniqueItem(self,tableNum,items,others,itemResults):
        item=items[tableNum]
        other=others[tableNum]
        sql='''SELECT other FROM item%d WHERE item = %d'''%(tableNum,item)
        isUnique=True
        try:
            self.cursor.execute(sql)
            results=self.cursor.fetchone()
        except:
            print "Error: unable to fetch data"
        if results:
            results=results[0]
            itemResults[tableNum]=results
            for resultHex in results.split(','):
                result=int(resultHex,16)
                #pdb.set_trace()
                if getSimhash.isEqual(other,result):
                    isUnique=False
                    break
        return isUnique

    def addNews(self,items,others,itemResults):
        for i in range(4):
            otherHex=hex(others[i])[2:-1]
            if itemResults[i]:
                sql='''UPDATE item%d SET other='%s' WHERE item = %d '''%(i,itemResults[i]+','+otherHex,items[i])
                try:
                    self.cursor.execute(sql)
                    self.db.commit()
                except:
                    self.db.rollback()
            else:
                sql=''' INSERT INTO item%d VALUES(%d,'%s')'''%(i,items[i],otherHex)
                try:
                    self.cursor.execute(sql)
                    self.db.commit()
                except:
                    self.db.rollback()

    def checkFile(self,fileName,add=True):
        f=open(fileName)
        for line in f:
            item=json.loads(line)
            #content=item['contentWithImg']
            #content=re.sub('{img}|{p}','',content)
            content=item['title']
            if self.checkNews(content,add):
                yield item
            else:
                logging.info('Repeated Item:'+str(item))
        f.close()

if __name__ =="__main__":
    uniquer=Uniquer()
    s1="王毅暗示韩国外长：想知道韩将如何维护两国关系,萨德,韩外长,王毅,中韩关系{img}原标题：部署萨德公布后首见韩外长 王毅：维护两国关系需实际行动据韩联社7月24日消息，中国外交部长王毅和韩国外交部长官尹炳世24日晚在老挝万象举行>双边会谈，就双方共同关心的问题交换意见。这是韩美军方本月8日公布决定在韩部署“萨德”反导系统后，中韩外长首次会面。王毅表示，最近韩方的行为损害中韩双方互信，中方对此感到遗憾，中方想了解韩方将为维护两国关系采取哪些实际行动。分析认为，王毅提及的“实际行动”可能是指中断部署“萨德”反导系统，>王毅的发言也暗示韩国部署“萨德”可能会对韩中关系带来不利影响。尹炳世在席间表示，两国关系越紧密，越有可能面临各种挑战。两国一直以来保持着良好关>系，我认为双方没有解决不了的问题。为维护朝鲜半岛和平与繁荣，双方都需要付出努力。另外，王毅在会晤尹炳世前就“今明有无可能会晤朝鲜外务相李勇浩”>的记者提问表示，有这种可能。"
    s2="王毅暗示韩国外长：想知道韩将如何维护两国关系,萨德,韩外长,王毅,中韩关系{img}原标题 王毅：维护两国关系需实际行动据韩联社7月24日消息，中国外交部长王毅和韩国外交部长官尹炳世24日晚在老挝万象举行>双边会谈，就双方共同关心的问题交换意见。这是韩美军方本月8日公布决定在韩部署“萨德”反导系统后，中韩外长首次会面。王毅表示，最近韩方的行为损害中韩双方互信，中方对此感到遗憾，中方想了解韩方将为维护两国关系采取哪些实际行动。分析认为，王毅提及的“实际行动”可能是指中断部署“萨德”反导系统，>王毅的发言也暗示韩国部署“萨德”可能会对韩中关系带来不利影响。尹炳世在席间表示，两国关系越紧密，越有可能面临各种挑战。两国一直以来保持着良好关>系，我认为双方没有解决不了的问题。为维护朝鲜半岛和平与繁荣，双方都需要付出努力。另外，王毅在会晤尹炳世前就“今明有无可能会晤朝鲜外务相李勇浩”>的记者提问表示，有这种可能。"
    s3='快艇翻沉后续下落不明人员增至4人. 2016-07-30 14:04:50 来源：中国新闻网 作者 ：${中新记者姓名} 责任编辑：. 2016年07月30日14:04 来源：中国新闻网 参与互动'
    s4="在当前的行贿受贿现象中，“权色交易”成了与“权钱交易”并列的一种重要权力交易形式。但颇为遗憾的是，法律只规定了对“权钱交易”的惩罚，而对“权色交易”却听之任之。这种只用一条腿走路的方式，使得“权色>交易”有恃无恐，极大泛滥而不能受到应有的惩处，以至于引起人们对法律正义的怀疑。尤其是，日前备受关注的原铁道部部长刘志军案，因有“性贿赂”情节而检方未对其提出指控，再度引发各界对“性贿赂”入刑话题的热议。刑法第三百八十五条和第三百八十九条，对受贿罪和行贿罪的界定，仅仅限于收受和给予财物行>为，而对“权色交易”、“权权交易”等收受、给予财物外的其他污染和亵渎权力的行为并不进行处置，显然是对以其他形式亵渎权力行为的放纵，是非常不妥的。>反腐败公约》对涉及贿赂罪行的相关界定是，贿赂特征在于提供不正当好处。这里提到的“不正当好处”，意味着包括财产性贿赂和“性贿赂”等非物质利益贿赂。>用“好处”取代“财物”，就会使任何形式的权力交易都能受到有效禁止和追究，而不会像当前的刑法这样眼睁睁地对“性贿赂”无奈。所以，为最大限度地保持公权>力的纯洁性，特别是为改变当前这种“性贿赂”猖獗而不能有效进行抑制的权力滥用局面，有必要参照反腐公约的规定，对刑法相关条款进行修改。而且，与性交>易合法化的一些国家不同，我国不承认性交易的合法性，并一直致力于铲除“钱色交易”，政府也一贯用铁拳进行扫黄打非。无可否认的是，相对于卖淫嫖娼这种>用当事者自己的钱财所发生的“钱色交易”，“权色交易”则由于滥用不属于自己的公权力而更没有正当性，性质更恶劣，危害更大，就更不应被允许。而且“钱色交易”主要是普通民众行为，而“权色交易”则是官员们利用职权进行的性交易。毫无疑问，对官员们的道德要求应当高于普通民众，才是正常的做法。只有根据现实情况及时进行法律修改，才能克服成文法的僵化性，使法律跟上时代的发展需要，而不是成为新时代的发展障碍。"
    s5="新浪网新闻中心是新浪网最重要的频道之一，24小时滚动报道国内、国际及社会新闻。每日编发新闻数以万计。"
    print uniquer.checkNews(s1)
    print uniquer.checkNews(s2)
    print uniquer.checkNews(s3)
    print uniquer.checkNews(s4)
    print uniquer.checkNews(s5)
