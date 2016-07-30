# -*- coding=utf-8 -*-
import getSimhash
import MySQLdb
import time

class uniqer(object):

    def __init__(self):
        self.hashLen=8
        self.db = MySQLdb.connect("localhost","roots","","test" )

        cursor = db.cursor()
        cursor.execute("SELECT VERSION()")
        data = cursor.fetchone()
        #print "Database version : %s " % data

    def __del__(self):
        self.db.close()

    def checkNews(self,content):
        simLong=getSimhash.getSimhash(content)
        simStr=self.long2Str(simLong,self.hashLen)
        items=[]
        others=[]
        isUnique=True
        for i in range(4):
            itemLen=self.hashLen/4
            lhs=itemLen*i
            rhs=itemLen*(i+1)
            items.append(simStr[lhr,rhs])
            others.append(simStr[0:lhs]+simStr[rhs:self.hashLen])
            if not self.uniqueItem(items[i],others[i]):
                isUnique=False
                break
        if isUnique:
            self.addNews(items,others)
            return True
        else:
            return False
    
    def uniqueItem(self,item,other):
        pass

    def addNews(self,items,others):
        pass

    def long2Str(self,l,length):
        s=''
        for i in range(length):
            s=s+chr(l&255)
            l=l>>8
        return s

    def str2Long(self.s):
        l=0
        i=0
        for si in s:
            l+=(1<<i)*ord(si)
            i+=8
        return l
#
#start=time.time()
#s1="王毅暗示韩国外长：想知道韩将如何维护两国关系,萨德,韩外长,王毅,中韩关系{img}原标题：部署萨德公布后首见韩外长 王毅：维护两国关系需实际行动据韩联社7月24日消息，中国外交部长王毅和韩国外交部长官尹炳世24日晚在老挝万象举行>双边会谈，就双方共同关心的问题交换意见。这是韩美军方本月8日公布决定在韩部署“萨德”反导系统后，中韩外长首次会面。王毅表示，最近韩方的行为损害中韩双方互信，中方对此感到遗憾，中方想了解韩方将为维护两国关系采取哪些实际行动。分析认为，王毅提及的“实际行动”可能是指中断部署“萨德”反导系统，>王毅的发言也暗示韩国部署“萨德”可能会对韩中关系带来不利影响。尹炳世在席间表示，两国关系越紧密，越有可能面临各种挑战。两国一直以来保持着良好关>系，我认为双方没有解决不了的问题。为维护朝鲜半岛和平与繁荣，双方都需要付出努力。另外，王毅在会晤尹炳世前就“今明有无可能会晤朝鲜外务相李勇浩”>的记者提问表示，有这种可能。"
#s2="王毅暗示韩国外长：想知道韩将如何维护两国关系,萨德,韩外长,王毅,中韩关系{img}原标题 王毅：维护两国关系需实际行动据韩联社7月24日消息，中国外交部长王毅和韩国外交部长官尹炳世24日晚在老挝万象举行>双边会谈，就双方共同关心的问题交换意见。这是韩美军方本月8日公布决定在韩部署“萨德”反导系统后，中韩外长首次会面。王毅表示，最近韩方的行为损害中韩双方互信，中方对此感到遗憾，中方想了解韩方将为维护两国关系采取哪些实际行动。分析认为，王毅提及的“实际行动”可能是指中断部署“萨德”反导系统，>王毅的发言也暗示韩国部署“萨德”可能会对韩中关系带来不利影响。尹炳世在席间表示，两国关系越紧密，越有可能面临各种挑战。两国一直以来保持着良好关>系，我认为双方没有解决不了的问题。为维护朝鲜半岛和平与繁荣，双方都需要付出努力。另外，王毅在会晤尹炳世前就“今明有无可能会晤朝鲜外务相李勇浩”>的记者提问表示，有这种可能。"
#a1=getSimhash.getSimhash(s1)
#a2=getSimhash.getSimhash(s2)
#print time.time()-start
##a1=str(bin(a1)).strip('-0b')
##a2=str(bin(a2)).strip('-0b')
#print (a1)
#print (a2)
#print (getSimhash.isEqual(a1,a2))

