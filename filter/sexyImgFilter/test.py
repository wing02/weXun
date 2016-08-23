#!/usr/bin/python
import sys 
import os
import numpy as np
import os.path as osp
import matplotlib.pyplot as plt
from pylab import *
import lmdb
import scipy.io as sio
import io
import cPickle

sys.path.append('/home/lab401/Project/caffe/python')
import caffe 

class Test:
    def __init__(self):
        model_def = 'data/train.prototxt'
        model_weights = 'data/snapshot/_iter_10000.caffemodel'
        meanFile='data/mean/trainMean.binaryproto'
        caffe.set_mode_cpu()
        caffe.set_device(0)
        self.net = caffe.Net(model_def,model_weights,caffe.TEST) 
        blob=caffe.proto.caffe_pb2.BlobProto()
        data=open(meanFile,'rb').read()
        blob.ParseFromString(data)
        mu=np.array(caffe.io.blobproto_to_array(blob))
        self.transformer = None
        self.transformer = caffe.io.Transformer({'data': self.net.blobs['data1'].data.shape})
        self.transformer.set_transpose('data', (2,0,1))  # move image channels to outermost dimension
        self.transformer.set_mean('data', mu[0]*0.00390625)            # subtract the dataset-mean value in each channel
        self.transformer.set_channel_swap('data', (2,1,0)) # swap channels from RGB to BGR

    def testImg(self,data)
        image=self.loadImgFromBinary(data)
        transformed_image = self.transformer.preprocess('data', image)
        self.net.blobs['data1'].data[...] = transformed_image
        output = self.net.forward()
        result=self.net.blobs['ip'].data[0]
        return result

    def loadImgFromBinary(self,data):
        srcPath=io.BytesIO(data)
        image = caffe.io.load_image(srcPath)
        return image
    
if __name__=="__main__":
    dataPath='data/test.txt'
    desPath='data/result.pkl'
    results=[]
    flags=[]
    test=Test()
    with open(dataPath) as f:
        for line in f:
            tmp=line.split(' ')
            path=tmp[0]
            flags.append(int(tmp[1]))
            with open(path) as fImg:
                result=test.testImg(fImg.read())
                results.append(result)
    cPickle.dump((results,flags),open(desPath,'w'))
