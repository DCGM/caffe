#!/usr/bin/env python
__author__ = 'ihradis'

import sys
from google.protobuf import text_format
import argparse

from caffe.proto import caffe_pb2

parser = argparse.ArgumentParser()
parser.add_argument(
    "-i", "--input",
    help="Input net definition.",
    required=True
)
parser.add_argument(
    "-o", "--output",
    help="Output net definition",
    required=True
)
parser.add_argument(
    "-r", "--remove",
    help="Remove layers. Expects comma separated list of layer names.",
    required=True
)
parser.add_argument(
    "--input_name",
    help="Optional comma-separated list of input layer names for deploy configuration.",
)
parser.add_argument(
    "--input_dim",
    help="Optional comma-separated list of input layer dimensions for deploy configuration.",
)


args = parser.parse_args()

net = caffe_pb2.NetParameter()
text_format.Merge(open(args.input).read(), net)

toRemove = args.remove.split(',')

print str(toRemove)

#net.layers = [x for x in net.layers if not (x.name in toRemove)]

net2 = caffe_pb2.NetParameter()
net2.CopyFrom(net)
net2.ClearField("layers")
net2.ClearField("input")
net2.ClearField("input_dim")

for inputName in args.input_name.split(','):
    net2.input.append(inputName)

for inputDim in args.input_dim.split(','):
    net2.input_dim.append(int(inputDim))

for layer in net.layers:
    if not (layer.name in toRemove):
        net2.layers.add()
        net2.layers[-1].CopyFrom(layer)


with open(args.output, 'w') as f:
    f.write(str(net2))
