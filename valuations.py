import numpy as np
from utils import getSplits, check

# aback
def firstValid(g, G):
    return 1 - (g in G)


# tares
def maxSizeSplit(g, G):
    splits = getSplits(g, G)
    return max(splits.values()) - (g in G)


def avgSizeSplit(g, G):
    splits = getSplits(g, G)
    return np.mean(splits.values()) - (g in G)


def expAsymptote(g, G):
    splits = getSplits(g, G)
    return sum(t * (1 - np.exp(-t)) for t in splits.values()) - (g in G) * (
        1 - np.exp(-1)
    )


def maxSumReciprocals(g, G):
    splits = getSplits(g, G)
    return 1 / sum(1 / t for t in splits.values())


def information(g, G):
    splits = getSplits(g, G)
    return sum(t * np.log(t) for t in splits.values()) - (g in G) * (2 * np.log(2))
