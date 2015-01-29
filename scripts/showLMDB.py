#!/usr/bin/env python
import sys
import time
import argparse
import lmdb

import cv2
import numpy as np

from caffe.proto import caffe_pb2

def main( argv):
    parser = argparse.ArgumentParser()
    parser.add_argument( "-i", "--input", help="Input leveldb directory.")
    args = parser.parse_args()
    

    env_in = lmdb.open(args.input)
    

    counter = 0
    t1 = time.time()
    with env_in.begin() as txn_in:
        c_in = txn_in.cursor();
        for it_in in c_in:
            datum = caffe_pb2.Datum()
            datum.ParseFromString(it_in[1])
                
            img = np.fromstring(datum.data, dtype=np.uint8)
            img = img.reshape((datum.channels, datum.height, datum.width))
            img = cv2.resize( img.transpose((1, 2, 0)), (480,480))
            
            cv2.imshow('image', img)
            cv2.waitKey(0)
                  
if __name__ == '__main__':
    main( sys.argv)
 
