from caffe import layers as L, params as P
import caffe

def lenet(lmdb,mean, batch_size):
    # our version of LeNet: a series of linear and simple nonlinear transformations
    n = caffe.NetSpec()
    
    n.data, n.label = L.Data(batch_size=batch_size, backend=P.Data.LMDB, source=lmdb,
            transform_param=dict(scale=1./255,mirror=True,mean_file=mean), ntop=2)
    
    #n.conv1 = L.Convolution(n.data,lr_mult=1, kernel_size=5,stride=2,pad=2, num_output=32, weight_filler=dict(type='xavier'))
    n.conv1 = L.Convolution(n.data,param=[{'lr_mult':1},{'lr_mult':2}],kernel_size=5,stride=1,pad=2, num_output=32, weight_filler=dict(type='xavier'))
    n.pool1 = L.Pooling(n.conv1, kernel_size=3, stride=2, pool=P.Pooling.MAX)
    n.relu1 = L.ReLU(n.pool1, in_place=True)

    n.norm1 = L.LRN(n.pool1,local_size=3,alpha=5e-05,beta=0.75,norm_region=1)

    n.conv2 = L.Convolution(n.norm1, param=[{'lr_mult':1},{'lr_mult':2}], kernel_size=5,stride=1,pad=2, num_output=32, weight_filler=dict(type='xavier'))
    n.relu2 = L.ReLU(n.conv2, in_place=True)
    n.pool2 = L.Pooling(n.conv2, kernel_size=3, stride=2, pool=P.Pooling.MAX)
    #n.fc1 =   L.InnerProduct(n.pool2, num_output=500, weight_filler=dict(type='xavier'))
    n.norm2 = L.LRN(n.pool2,local_size=3,alpha=5e-05,beta=0.75,norm_region=1)

    n.conv3 = L.Convolution(n.norm2, kernel_size=5,stride=1,pad=2, num_output=64, weight_filler=dict(type='xavier'))
    n.relu3 = L.ReLU(n.conv3, in_place=True)
    n.pool3 = L.Pooling(n.conv3, kernel_size=3, stride=2, pool=P.Pooling.MAX)

    n.ip = L.InnerProduct(n.pool3,param=[{'lr_mult':1,'decay_mult': 250},{'lr_mult':2,'decay_mult': 0}],  num_output=2, weight_filler=dict(type='xavier'))
    n.loss =  L.SoftmaxWithLoss(n.ip, n.label)
    n.accuracy =  L.Accuracy(n.ip, n.label)
    
    return n.to_proto()
    
with open('data/train.prototxt', 'w') as f:
    f.write(str(lenet('data/lmdb/trainLmdb','data/mean/trainMean.binaryproto', 128)))
    
with open('data/test.prototxt', 'w') as f:
    f.write(str(lenet('data/lmdb/testLmdb','data/mean/testMean.binaryproto', 128)))
