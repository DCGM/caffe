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
    parser.add_argument( "-o", "--output", help="Output leveldb directory.")
    parser.add_argument( "-s", "--size", help="Size to rescale images to.", type=int)
    args = parser.parse_args()
    

    env_in = lmdb.open(args.input)
    env_out = lmdb.open(args.output, map_size=100000000000)
    
    size = (int(args.size), int(args.size))

    counter = 0
    t1 = time.time()
    with env_in.begin() as txn_in:
        with env_out.begin(write=True) as txn_out:
             c_in = txn_in.cursor();
             c_out = txn_out.cursor()
             for it_in in c_in:
                datum = caffe_pb2.Datum()
                datum.ParseFromString(it_in[1])
                
                img = np.fromstring(datum.data, dtype=np.uint8)
                img = img.reshape((datum.channels, datum.height, datum.width))
                img = img.transpose((1, 2, 0))
                img = cv2.resize(img, dsize=size, interpolation=cv2.INTER_AREA)
                img = img.transpose((2, 0, 1))
                
                datum.height = size[1]
                datum.width = size[0]
                datum.data = str(np.ascontiguousarray(img).data)
                c_out.put(it_in[0], datum.SerializeToString())
                
                counter += 1
                if counter % 1000 == 0:
                   print "DONE %d in %f s" % (counter, time.time() - t1)
                  
if __name__ == '__main__':
    main( sys.argv)
 
