#coding=utf8
from __future__ import (division,absolute_import,print_function,unicode_literals)
import jieba
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
import logging
import cPickle
import re
import os
import os.path as osp
import sys
import numpy as np
from sklearn.cross_validation import train_test_split
from sklearn import feature_extraction
from sklearn.feature_extraction.text import CountVectorizer
from sklearn import svm
import glob
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.special import expit
import cPickle

class PolTfidf:
    def __init__(self):
        prePath='filter/polTxtFilter/data/model/'
        tfidfPath=prePath+'tfidf.pkl'
        clfPath=prePath+'clf.pkl'
        self.tfidfVectorizer=cPickle.load(open(tfidfPath))
        self.clf=cPickle.load(open(clfPath))

    def loadData(self,path):
        #path=good/people
        cutPath='data/cut/'+path+'.txt'
        if osp.isfile(cutPath):
            contents=[i.strip() for i in open(cutPath)]
            return contents
        else:
            srcPath='data/src/'+path+'.json'
            cut=open(cutPath,'w')
            contents=[]
            for line in open(srcPath):
                item=json.loads(line)
                content=re.sub('{p}|{img}','',item['contentWithImg'])
                content=' '.join(jieba.cut(content))
                contents.append(content)
                cut.write(content.encode('u8')+'\n')
            cut.close()
            return contents

    def loadStopWords(self):
        path='data/stop_words.utf8'
        return [i.strip('\n').decode('u8') for i in open(path)]
    
    def recall(self,yPred,yVal):
        TF=[i==1 and j==1 for i,j in zip(yPred,yVal)]
        return float(sum(TF))/sum(yVal)

    def precision(self,yPred,yVal):
        TF=[i==1 and j==1 for i,j in zip(yPred,yVal)]
        return float(sum(TF))/sum(yPred)

    def top(self,yDecision,yVal,rate=0.9):
        maxNum=max(yDecision)
        minNum=min(yDecision)
        yDecison=map(lambda i:(i-minNum)/(maxNum-minNum),yDecision)
        yPred=[i>0.9 for i in yDecision]
        print ("The top"+str(rate)+'has :',float(sum(yPred))/len(yVal))
        TF=[i==1 and j==1 for i,j in zip(yPred,yVal)]
        return float(sum(TF))/sum(yPred)

    def getScore(self,content):
        xTfidf=self.tfidfVectorizer.transform([content])
        score=self.clf.decision_function(xTfidf)
        #print (self.clf.predict(xTfidf))
        return expit(score[0])

    def getSenWords(self):
        coe=dict()
        for i in range(len(self.clf.coef_[0])):
            coe[i]=self.clf.coef_[0][i]

        coeArray=sorted(coe.items(), lambda x, y: cmp(x[1], y[1]))
        feaNames=self.tfidfVectorizer.get_feature_names()

        vecRank=[]
        for item in coeArray:
            vecRank.append(feaNames[item[0]])
        return vecRank

def test():
    textFilter=PolTfidf()
    goodList=textFilter.loadData('good/mynewsTrain')
    badList=textFilter.loadData('bad/tencent')
    prePath='data/model/'
    tfidfPath=prePath+'tfidf.pkl'
    xTrainTfidfPath=prePath+'xTrainTfidf.pkl'
    xTestTfidfPath=prePath+'xTestTfidf.pkl'
    clfPath=prePath+'clf.pkl'

    x=goodList+badList
    y=[0]*len(goodList)+[1]*len(badList)

    xTrain,xTest,yTrain,yTest=train_test_split(x,y,test_size=0.2,random_state=42) 

    logging.info('Start train TFIDF')

    if osp.isfile(tfidfPath):
        tfidfVectorizer=cPickle.load(open(tfidfPath))
    else:
        tfidfVectorizer=TfidfVectorizer().fit(xTrain,yTrain)
        cPickle.dump(tfidfVectorizer,open(tfidfPath,'w'))

    logging.info('Start test TFIDF')
    if osp.isfile(xTrainTfidfPath):
        xTrainTfidf=cPickle.load(open(xTrainTfidfPath))
    else:
        xTrainTfidf=tfidfVectorizer.transform(xTrain)
        cPickle.dump(xTrainTfidf,open(xTrainTfidfPath,'w'))

    if osp.isfile(xTestTfidfPath):
        xTestTfidf=cPickle.load(open(xTestTfidfPath))
    else:
        xTestTfidf= tfidfVectorizer.transform(xTest)
        cPickle.dump(xTestTfidf,open(xTestTfidfPath,'w'))

    logging.info('Start CLF')
    if osp.isfile(clfPath):
        clf=cPickle.load(open(clfPath))
    else:
        clf =LogisticRegression()
        clf.fit(xTrainTfidf,yTrain)
        cPickle.dump(clf,open(clfPath,'w'))

    logging.info('Start SCORE')
    print ("TrainScore:",clf.score(xTrainTfidf,yTrain))
    print ("TestScore:",clf.score(xTestTfidf,yTest))

    logging.info('Done.')

    minghuiPath='bad/minghui'
    minghuiData=textFilter.loadData(minghuiPath)
    mynewsTestPath='good/mynewsTest'
    mynewsTestData=textFilter.loadData(mynewsTestPath)
    xVal=mynewsTestData+minghuiData
    yVal=[0]*len(mynewsTestData)+[1]*len(minghuiData)
    xValTfidf=tfidfVectorizer.transform(xVal)
    #result=clf.decision_function(xVal)
    
    yPred=clf.predict(xValTfidf)
    yDecision=clf.decision_function(xValTfidf)
    print ("Recall:",textFilter.recall(yPred,yVal))
    print ("Precision:",textFilter.precision(yPred,yVal))
    print ("Top90:",textFilter.top(yDecision,yVal))

    return clf,xValTfidf,yVal

if __name__=='__main__':
    #logging.basicConfig(level=logging.DEBUG,format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',datefmt='%a, %d %b %Y %H:%M:%S')
    #test()
    polTfidf=PolTfidf()
    goodFile='filter/polTxtFilter/data/goodTest.json'
    badFile='filter/polTxtFilter/data/src/bad/minghui.json'
    file=badFile
    scores=[]
    for line in open(file):
        content=json.loads(line)['contentWithImg']
        content=re.sub('{up}{img}','',content)
        content=' '.join(jieba.cut(content))
        score=polTfidf.getScore(content)
        scores.append(score)
        #print (score)
    #cPickle.dump(scores,open('scores.pkl','w'))
    cPickle.dump(scores,open('scores2.pkl','w'))

    #words=polTfidf.getSenWords()
    #for i in range(1,100):
    #    print (words[-i],end=' ')
    #print ('\n')

