#!/home/ihradis/anaconda/bin/python2.7

import sys
import re
import random
import copy
from collections import OrderedDict, defaultdict
from operator import itemgetter
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from scipy import signal



def noException( func):
    def dec(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except:
            print "Exception"
            raise
    return dec

@noException
def plotLoss(loss, test, plotName):
    print plotName
    fig, axes1 = plt.subplots(figsize=(22, 14), dpi=120)
    axes2 = axes1.twinx()
    allVal = loss.copy()
    allVal.update(test)
    for name in allVal:
        iterations = np.array([x[0] for x in allVal[name]])
        values = np.array([x[1] for x in allVal[name]])
        if "loss" in name:
            axes1.semilogy(iterations, values, label=name)
            axes2._get_lines.color_cycle.next()
        else:
            axes2.plot(iterations, values, label=name)
            axes1._get_lines.color_cycle.next()
    lines, labels = axes1.get_legend_handles_labels()
    lines2, labels2 = axes2.get_legend_handles_labels()
    axes2.legend(lines + lines2, labels + labels2, loc="lower right")
    plt.savefig(plotName)
    plt.close(fig)

def smooth(data, filterSize):
    if filterSize == 1:
        return copy.copy( data)
    assert(filterSize % 2 == 1)
    filterKernel = np.asarray([1.0/filterSize] * filterSize)
    padding = int(filterSize / 2)

    extendedData = np.array([data[0]] * padding + data + [data[-1]] * padding)
    return signal.convolve(extendedData, filterKernel, mode="valid")


@noException
def plotStat(stat, getter, plotName, filterSize=1, logPlot=True):
    """

    :type stat: dict of list of pairs (iteration, list of values)
    :type getter: function returning one value from stat values to plot
    :type plotName: string
    :type filterSize: int
    """
    print plotName
    fig, axes1 = plt.subplots(figsize=(22, 14), dpi=120)
    colormap = plt.get_cmap("spectral")
    plt.gca().set_color_cycle([colormap(i) for i in np.linspace(0, 0.95, len(stat))])

    for name in stat:
        iterations = np.array([x[0] for x in stat[name]])
        values = [getter(x[1]) for x in stat[name]]
        values = smooth(values, filterSize)
        if logPlot:
            axes1.semilogy(iterations, values, label=name)
        else:
            axes1.plot(iterations, values, label=name)
        axes1.annotate(name, xy=(iterations[-1], values[-1]))

    axes1.legend(loc="upper right")
    plt.savefig(plotName)
    plt.close(fig)


@noException
def plotAll( stat, name):
    print name
    plt.figure(figsize=(16, 8), dpi=120)
    plt.title(name)
    plt.xlabel('Iteration')
    iterations = [x[0] for x in stat]
    data = [x[1][0] for x in stat]
    plt.plot(iterations, data, label="abs_mean")
    data = [x[1][4] for x in stat]
    plt.plot(iterations, data, label="mean")
    data = [x[1][5] for x in stat]
    plt.plot(iterations, data, label="q_005")
    data = [x[1][6] for x in stat]
    plt.plot(iterations, data, label="q_25")
    data = [x[1][7] for x in stat]
    plt.plot(iterations, data, label="q_50")
    data = [x[1][8] for x in stat]
    plt.plot(iterations, data, label="q_75")
    data = [x[1][9] for x in stat]
    plt.plot(iterations, data, label="q_995")
    plt.legend()
    plt.savefig(name + ".png")
    plt.close()


forward = OrderedDict()
backward = OrderedDict()
updateData = OrderedDict()
updateDiff = OrderedDict()

loss = defaultdict(list)
test = defaultdict(list)


lastIteration = -1
iteration = -1
lossID = 0
#f = open("/home/ihradis/CAFE_projects/CALTECH-2/log.txt", "r")
for line in sys.stdin.readlines():
    words = [x.strip() for x in line.split()]
    if len(words) < 6:
        continue
    try:
        if words[4] == "Iteration":
            iteration = int(words[5].strip(','))
            if iteration != lastIteration:
                lastIteration = iteration
                lossID = 0
            if words[6] == "loss":
                loss[str(lossID) + "_loss"].append((iteration, float(words[8])))
                lossID += 1
        elif words[4] == "Test":
            name = words[7] + words[8]
            name = name.replace(":", "_")
            test[name].append((iteration, float(words[10]) ))
        elif words[4] == "[Forward]" or words[4] == "[Backward]":
            name = words[6] + "_" + words[9] + "_" + words[10].strip(':')
            name = name.replace(',', '-')
            content = [float(x) for x in words[11:]]
            if words[4] == "[Forward]":
                forward.setdefault(name, []).append((iteration, content))
            if words[4] == "[Backward]":
                backward.setdefault(name, []).append((iteration, content))
        elif words[4] == "[Update]":
            words[9] = words[9].strip(':')
            name = words[6] + "_" + words[8] + "_" + words[9]
            name = name.replace(',', '-')
            content = [float(x) for x in words[10:]]
            if words[9] == "data":
                updateData.setdefault(name, []).append((iteration, content))
            if words[9] == "diff":
                updateDiff.setdefault(name, []).append((iteration, content))
    except IOError:
        print "XX"
        pass



plotLoss(loss, test, "loss.png")
weightData = OrderedDict([(k,v) for (k,v) in updateData.iteritems() if "_0" in k])
biasData = OrderedDict([(k,v) for (k,v) in updateData.iteritems() if not "_0" in k])
weightUpdate = OrderedDict([(k,v) for (k,v) in updateDiff.iteritems() if "_0" in k])
biasUpdate = OrderedDict([(k,v) for (k,v) in updateDiff.iteritems() if not "_0" in k])
for filterKernel in [15]:
    plotStat(weightUpdate, lambda x: x[0], "net_weight_update_meanAbs_%02d.png" % filterKernel, filterSize=filterKernel)
    plotStat(biasUpdate, lambda x: x[0], "net_bias_update_meanAbs_%02d.png" % filterKernel, filterSize=filterKernel)

for filterKernel in [1]:
    plotStat(weightData, lambda x: x[0], "net_weight_data_meanAbs_%02d.png" % filterKernel, filterSize=filterKernel)
    plotStat(biasData, lambda x: x[0], "net_bias_data_meanAbs_%02d.png" % filterKernel, filterSize=filterKernel)

#for filterKernel in [1]:
#    plotStat(weightData, lambda x: x[1]/x[3], "net_weight_data_mean2_%02d.png" % filterKernel, filterSize=filterKernel)
#    plotStat(biasData, lambda x: x[1]/x[3], "net_bias_data_mean2_%02d.png" % filterKernel, filterSize=filterKernel)

#for filterKernel in [15]:
#    plotStat(weightUpdate, lambda x: x[1]/x[3], "net_weight_update_mean2_%02d.png" % filterKernel, filterSize=filterKernel)
#    plotStat(biasUpdate, lambda x: x[1]/x[3], "net_bias_update_mean2_%02d.png" % filterKernel, filterSize=filterKernel)
#for filterKernel in [15]:
#    plotStat(weightUpdate, lambda x: x[1], "net_weight_update_energy_%02d.png" % filterKernel, filterSize=filterKernel)
#    plotStat(biasUpdate, lambda x: x[1], "net_bias_update_energy_%02d.png" % filterKernel, filterSize=filterKernel)


rawActivations = OrderedDict([(k,v) for (k,v) in forward.iteritems() if "FC" == k[:2] or "CONV" == k[:4]])
plotStat(rawActivations, lambda x: x[0], "net_activations_raw_meanAbs.png")

reluActivations = OrderedDict([(k,v) for (k,v) in forward.iteritems() if "RELU" in k])
plotStat(reluActivations, lambda x: x[0], "net_activations_relu_meanAbs.png")
plotStat(reluActivations, lambda x: x[2]/x[3], "net_activations_sparsity.png", logPlot=False)

activationDiff = OrderedDict([(k,v) for (k,v) in backward.iteritems() if "RELU" == k[:4]])
plotStat(activationDiff, lambda x: x[0], "net_activations_diff_21.png", filterSize=21)

weightDiff = OrderedDict([(k,v) for (k,v) in backward.iteritems() if "_0_" in k])
biasDiff = OrderedDict([(k,v) for (k,v) in backward.iteritems() if "_1_" in k])
plotStat(weightDiff, lambda x: x[0], "net_weight_diff_15.png", filterSize=15)
plotStat(biasDiff, lambda x: x[0], "net_bias_diff_15.png", filterSize=15)

for name in updateData:
    plotAll(updateData[name], "stat_param_" + name)
for name in updateDiff:
    plotAll(updateDiff[name], "stat_update_" + name)
for name in forward:
    plotAll(forward[name], "stat_forward_" + name)
for name in backward:
    plotAll(backward[name], "stat_backward_" + name)

