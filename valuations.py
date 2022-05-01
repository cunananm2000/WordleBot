import numpy as np
from utils import getSplits, check

# aback
def firstValid(g, G):
    return 0 if g in G else 1


# tares
def maxSizeSplit(g, G):
    splits = getSplits(g, G)
    return max(splits.values())


def avgSizeSplit(g, G):
    splits = getSplits(g, G)
    return np.mean(list(splits.values()))

def expSizeSplit(g, G):
    splits = getSplits(g, G)
    return sum(t/len(G) * t for t in splits.values())

def expAsymptote(g, G):
    splits = getSplits(g, G)
    return sum(t * (1 - np.exp(-t)) for t in splits.values())


def maxSumReciprocals(g, G):
    splits = getSplits(g, G)
    return 1 / sum(1 / t for t in splits.values())

def harmonicMean(g, G):
    splits = getSplits(g, G)
    return len(splits.values()) / sum((1/t) for t in splits.values())

def mostParts(g, G):
    splits = getSplits(g, G)
    return -len(splits.values())


def information(g, G):
    splits = getSplits(g, G)
    return sum(t * np.log(t) for t in splits.values())


def probsGreen(g, G):
    splits = getSplits(g, G)

    t = 0
    for k, v in splits.items():
        s = k.count("1") + 2 * k.count("2")
        t += s * v / len(G)

    return -t
