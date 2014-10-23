import cv2
import numpy as np
import leveldb
import argparse
import sys
import time
from caffe.proto import caffe_pb2

def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument( "-i", "--input", help="Input leveldb directory.")
    parser.add_argument( "-o", "--output", help="Output leveldb directory.")
    parser.add_argument( "-s", "--size", help="Size to rescale images to.", type=int)
    args = parser.parse_args()

    dbIn = leveldb.LevelDB(args.input)
    dbOut = leveldb.LevelDB(args.output)
    size = (int(args.size), int(args.size))

    counter = 0
    t1 = time.time()
    for record in dbIn.RangeIter():
        datum = caffe_pb2.Datum()
        datum.ParseFromString(record[1])
        img = np.fromstring(datum.data, dtype=np.uint8)
        img = img.reshape((datum.channels, datum.height, datum.width))
        img = img.transpose((1, 2, 0))
        img = cv2.resize(img, dsize=size, interpolation=cv2.INTER_AREA)
        img = img.transpose((2, 0, 1))

        datum.height = size[1]
        datum.width = size[0]
        datum.data = str(np.ascontiguousarray(img).data)
        dbOut.Put(record[0], datum.SerializeToString())

        counter += 1
        if counter % 1000 == 0:
            print "DONE %d in %f s" % (counter, time.time() - t1)

if __name__ == '__main__':
    main( sys.argv)