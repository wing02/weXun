from a import TextFilter
import jieba
from sklearn.naive_bayes import MultinomialNB
import logging
import cPickle
import re
import os
import sys
import numpy as np
from sklearn.cross_validation import train_test_split
from sklearn import feature_extraction
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn import svm
import glob
import json
from sklearn.feature_extraction.text import TfidfVectorizer
import cPickle
from sklearn.linear_model import LogisticRegression

textFilter=TextFilter()
goodList=textFilter.load(textFilter.goodFile)
badList=textFilter.load(textFilter.badFile)

x=goodList+badList
y=[0]*len(goodList)+[1]*len(badList)

xTrain,xTest,yTrain,yTest=train_test_split(x,y,test_size=0.2,random_state=42) 
xTrainTfidf=cPickle.load(open('xTrainTfidf.pkl','r'))
xTestTfidf=cPickle.load(open('xTestTfidf.pkl','r'))
tfidfVectorizer=cPickle.load(open('tfidf.pkl'))

clf=LogisticRegression()
clf.fit(xTrainTfidf,yTrain)
print clf.score(xTrainTfidf,yTrain)


coe=dict()
for i in range(len(clf.coef_[0])):
    coe[i]=clf.coef_[0][i]

coeArray=sorted(coe.items(), lambda x, y: cmp(x[1], y[1]))
feaNames=tfidfVectorizer.get_feature_names()

vecRank=[]
for item in coeArray:
    vecRank.append(feaNames[item[0]])

for i in range(1,100):
    print vecRank[-i],


