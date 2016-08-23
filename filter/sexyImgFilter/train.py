import sys 
import os
import numpy as np
import os.path as osp
import matplotlib.pyplot as plt
from pylab import *
import caffe 
import pickle


class Train:
    def __init__(self):
        plt.rcParams['figure.figsize'] = (6, 6)
        caffe.set_mode_gpu()
        caffe.set_device(0)
        workdir='.'
        self.solver = None
        self.solver = caffe.SGDSolver(osp.join(workdir, 'solver.prototxt'))
        self.train_loss = []
        self.train_acc = []
        self.test_loss = []
        self.test_acc = []
        self.oneStep=100

    def step(self,stepSize):
        niter = stepSize/self.oneStep
        for it in range(niter):
            self.solver.step(self.oneStep)  # SGD by Caffe
            self.train_loss.append(self.solver.net.blobs['loss'].data+0)
            self.train_acc.append(self.solver.net.blobs['accuracy'].data+0)
            self.test_loss.append(self.solver.test_nets[0].blobs['loss'].data+0)
            self.test_acc.append(self.solver.test_nets[0].blobs['accuracy'].data+0)

    def drawAll(self):
        _, ax1 = subplots()
        ax2 = ax1.twinx()
        line1,=ax1.plot(self.oneStep*arange(len(self.train_loss)), self.train_loss,'b',label='trainLoss')
        line2,=ax2.plot(self.oneStep*arange(len(self.train_acc)), self.train_acc,'r',label='trainAcc')
        line3,=ax1.plot(self.oneStep*arange(len(self.test_loss)), self.test_loss,'g',label='testLoss')
        line4,=ax2.plot(self.oneStep*arange(len(self.test_acc)), self.test_acc,'y',label='testAcc')
        ax1.legend(loc=2)
        ax2.legend(loc=1)
        ax1.set_xlabel('iteration')
        ax1.set_ylabel('loss')
        ax2.set_ylabel('accuracy')
        show()

    def saveLog(self):
        with open('log.pkl','w') as f:
            log={'trainLoss':self.train_loss,'trainAcc':self.train_acc,'testLoss':self.test_loss,'testAcc':self.test_acc}
            pickle.dump((log),f)

    def loadLog(self):
        with open('log.pkl','r') as f:
            result = pickle.load(f)

    def drawTrain(self):
        _, ax1 = subplots()
        ax2 = ax1.twinx()
        ax1.plot(self.oneStep*arange(len(self.train_loss)), self.train_loss)
        ax2.plot(self.oneStep*arange(len(self.train_acc)), self.train_acc,'r')
        ax1.set_xlabel('iteration')
        ax1.set_ylabel('train loss')
        ax2.set_ylabel('train accuracy')

    def drawTest(self):
        _, ax1 = subplots()
        ax2 = ax1.twinx()
        ax1.plot(self.oneStep*arange(len(self.test_loss)), self.test_loss)
        ax2.plot(self.oneStep*arange(len(self.test_acc)), self.test_acc,'r')
        ax1.set_xlabel('iteration')
        ax1.set_ylabel('test loss')
        ax2.set_ylabel('test accuracy')
