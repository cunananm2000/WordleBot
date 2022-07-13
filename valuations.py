import numpy as np

from utils import getSplits


# aback
def inSet(g, C):
    return 0 if g in C else 1


# tares
# The best case would have the maximum be 1
def maxSizeSplit(g, C):
    splits = getSplits(g, C)
    return max(splits.values()) - 1


# The best case would have all the splits be size 1
def avgSizeSplit(g, C):
    splits = getSplits(g, C)
    return np.mean(list(splits.values())) - 1


def expSizeSplit(g, C):
    splits = getSplits(g, C)
    return sum(t / len(C) * t for t in splits.values()) - 1


def maxSumReciprocals(g, C):
    splits = getSplits(g, C)
    return 1 / sum(1 / t for t in splits.values())


def harmonicMean(g, C):
    splits = getSplits(g, C)
    return len(splits.values()) / sum((1 / t) for t in splits.values()) - 1


# Best case would have everything in its own part
def mostParts(g, C):
    splits = getSplits(g, C)
    return -len(splits) + len(C)


# In best case, they would all be size 1, and log(1) = 0
def information(g, C):
    splits = getSplits(g, C)
    return sum(t * np.log(t) for t in splits.values())


def probsGreen(g, C):
    splits = getSplits(g, C)
    t = 0
    for k, v in splits.items():
        s = k.count("1") + 2 * k.count("2")
        t += s * v / len(C)

    return -t + 10  # 2 * 5


def minRange(g, C):
    splits = getSplits(g, C)
    if len(splits) == 1: return np.inf
    return max(splits.values()) - min(splits.values())


def minStdDev(g, C):
    splits = getSplits(g, C)
    if len(splits) == 1: return np.inf
    return np.std(list(splits.values()))

def charFreqs(g, C):
    t = 0
    for i in range(len(g)):
        for c in C:
            if g[i] == c[i]: t += 2
            elif g[i] in c: t += 1
    return -t
