import numpy as np


def getSplits(g, G, checker):
    splits = {}
    for g0 in G:
        res = checker(g, g0)
        splits[res] = splits.get(res, 0) + 1

    return splits


# aback
def firstValid(g, G, checker):
    return 1 - (g in G)


# tares
def maxSizeSplit(g, G, checker):
    splits = getSplits(g, G, checker)
    return max(splits.values()) - (g in G)


def avgSizeSplit(g, G, checker):
    splits = getSplits(g, G, checker)
    return np.mean(splits.values()) - (g in G)


def expAsymptote(g, G, checker):
    splits = getSplits(g, G, checker)
    return sum(t * (1 - np.exp(-t)) for t in splits.values()) - (g in G) * (
        1 - np.exp(-1)
    )


def maxSumReciprocals(g, G, checker):
    splits = getSplits(g, G, checker)
    return 1 / sum(1 / t for t in splits.values())


def information(g, G, checker):
    splits = getSplits(g, G, checker)
    return sum(t * np.log(t) for t in splits.values()) - (g in G) * (2 * np.log(2))
