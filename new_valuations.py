from typing import List

import numpy as np

from new_definitions import Numeric
from new_utils import get_splits_with_count, get_splits_with_words


def in_set(g: str, C: List[str]) -> Numeric:
    return 1 - (g in C)


def max_size_split(g: str, C: List[str]) -> Numeric:
    splits = get_splits_with_count(g, C)
    return max(splits.values())


def avg_size_split(g: str, C: List[str]) -> Numeric:
    splits = get_splits_with_count(g, C)
    return np.mean(list(splits.values()))


def exp_size_split(g: str, C: List[str]) -> Numeric:
    splits = get_splits_with_count(g, C)
    return sum(t / len(C) * t for t in splits.values())


def max_sum_reciprocals(g: str, C: List[str]) -> Numeric:
    splits = get_splits_with_count(g, C)
    return 1 / sum(1 / t for t in splits.values())


def harmonic_mean(g: str, C: List[str]) -> Numeric:
    splits = get_splits_with_count(g, C)
    return len(splits.values()) / sum((1 / t) for t in splits.values())


def most_parts(g: str, C: List[str]) -> Numeric:
    splits = get_splits_with_count(g, C)
    return -len(splits)


def information(g: str, C: List[str]) -> Numeric:
    splits = get_splits_with_count(g, C)
    return sum(t * np.log(t) for t in splits.values())


def prosb_green(g: str, C: List[str]) -> Numeric:
    splits = get_splits_with_words(g, C)
    t = 0
    for k, v in splits.items():
        s = k.count("1") + 2 * k.count("2")
        t += s * v / len(C)

    return -t


def min_range(g: str, C: List[str]) -> Numeric:
    splits = get_splits_with_count(g, C)
    if len(splits) == 1:
        return np.inf
    return max(splits.values()) - min(splits.values())


def min_std_dev(g: str, C: List[str]) -> Numeric:
    splits = get_splits_with_count(g, C)
    if len(splits) == 1:
        return np.inf
    return np.std(list(splits.values()))


def char_freqs(g: str, C: List[str]) -> Numeric:
    splits = get_splits_with_count(g, C)
    if len(splits) == 1:
        return np.inf
    t = 0
    for i, l in enumerate(g):
        for c in C:
            if l == c[i]:
                t += 2
            elif l in c:
                t += 1
    return -t


def multi_val(g: str, C: List[str]) -> Numeric:
    splits = get_splits_with_count(g, C)
    return -len(splits), (1 - (g in C)), sum(t * t for t in splits.values())
