#!/usr/bin/env python
__author__ = 'ihradis'

import sys
import numpy as np
from caffe.proto import caffe_pb2
import caffe
import cv2


# take an array of shape (n, height, width) or (n, height, width, channels)
#  and visualize each (height, width) thing in a grid of size approx. sqrt(n) by sqrt(n)
def vis_square(data, padsize=1, padval=0):
    data -= data.min()
    data /= data.max()

    # force the number of filters to be square
    n = int(np.ceil(np.sqrt(data.shape[0])))
    padding = ((0, n ** 2 - data.shape[0]), (0, padsize), (0, padsize)) + ((0, 0),) * (data.ndim - 3)
    data = np.pad(data, padding, mode='constant', constant_values=(padval, padval))

    # tile the filters into an image
    data = data.reshape((n, n) + data.shape[1:]).transpose((0, 2, 1, 3) + tuple(range(4, data.ndim + 1)))
    data = data.reshape((n * data.shape[1], n * data.shape[3]) + data.shape[4:])

    #cv2.imshow('Filters', data)
    return data

paramFile = sys.argv[1]
defFile = sys.argv[2]

p = caffe_pb2.NetParameter()

#caffe.set_phase_test()
#caffe.set_mode_cpu()
net = caffe.Classifier( defFile, paramFile)
print 'DONE'

#with open(file, 'r') as f:
#    p.ParseFromString(f.read())

b = net.params[sys.argv[3]][0].data #p.layers[1].blobs[0]
filters = np.asarray(b)
print str(b.shape)

#for i in range( filters.shape[0]):
#  f = filters[ i, :, :, :].squeeze().transpose(1, 2, 0)
#  print str( f.shape)
#  f = f - np.amin(f)
#  f = f / np.amax(f)
#  print str( f)
#  f = cv2.resize( f, (256, 256), interpolation=cv2.INTER_NEAREST)
#  cv2.imshow('filter', f)
#  cv2.imwrite('test.png', f * 256)
#  cv2.waitKey(0)


data =vis_square(filters.transpose(0, 2, 3, 1))
cv2.imwrite(sys.argv[1] + '.png', data*256)


#cv2.waitKey(0)


#net = caffe.Classifier(dir + 'net_train_val.prototxt', dir + 'net_iter_15000.solverstate')
#print net.params.items()[0]
