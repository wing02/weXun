
import glob
import os
import os.path as osp

dataDir='data/srcImg'
labels=['good','bad']

txnTrain=open('data/train.txt','w')
txnTest=open('data/test.txt','w')

for i in range(len(labels)):
    label=labels[i]
    imgList=glob.glob(osp.join(dataDir,label,'*'))
    j=0
    for img in imgList:
        if j%5 ==2:
            txnTest.write(img+' '+str(i)+'\n')
        else:
            txnTrain.write(img+' '+str(i)+'\n')
        j+=1

