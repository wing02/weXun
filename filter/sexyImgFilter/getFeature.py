#!/usr/bin/python
import sys 
import os
import numpy as np
import os.path as osp
import matplotlib.pyplot as plt
from pylab import *
import lmdb
import scipy.io as sio

sys.path.append('/home/lab401/Project/caffe/python')
import caffe 

class Test:
    def __init__(self):
        srcPath=sys.argv[1]#.jpg
        desPath=sys.argv[2]#.mat
        model_def = 'getDeepId/deploy.prototxt'
        model_weights = 'getDeepId/deploy.caffemodel'
        meanFile='getDeepId/mean.binaryproto'
        caffe.set_mode_gpu()
        caffe.set_device(0)
        net = caffe.Net(model_def,model_weights,caffe.TEST) 
        blob=caffe.proto.caffe_pb2.BlobProto()
        data=open(meanFile,'rb').read()
        blob.ParseFromString(data)
        mu=np.array(caffe.io.blobproto_to_array(blob))
        transformer = None
        transformer = caffe.io.Transformer({'data': net.blobs['data1'].data.shape})
        transformer.set_transpose('data', (2,0,1))  # move image channels to outermost dimension
        transformer.set_mean('data', mu[0]*0.00390625)            # subtract the dataset-mean value in each channel
        transformer.set_channel_swap('data', (2,1,0)) # swap channels from RGB to BGR

        image = caffe.io.load_image(srcPath)
        transformed_image = transformer.preprocess('data', image)
        net.blobs['data1'].data[...] = transformed_image
        output = net.forward()
        deepid=net.blobs['ip1'].data[0]
        sio.savemat(desPath,{'data':deepid})

