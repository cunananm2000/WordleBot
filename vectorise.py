import random

import numpy as np
from numba import jit

from utils import check
from wordLists import answers

N_LETTERS = 5


@jit(nopython=True)
def monte_carlo_pi_numba(nsamples):
    acc = 0
    for i in range(nsamples):
        x = random.random()
        y = random.random()
        if (x**2 + y**2) < 1.0:
            acc += 1
    return 4.0 * acc / nsamples

    # res = ["0"] * nLetters
    # hit = [False] * nLetters
    # for i in range(nLetters):
    #     if guess[i] == answer[i]:
    #         res[i] = "2"
    #         hit[i] = True
    # for i in range(nLetters):
    #     if res[i] == "0":
    #         for j in range(nLetters):
    #             if guess[i] == answer[j] and not hit[j]:
    #                 res[i] = "1"
    #                 hit[j] = True
    #                 break
    # if debug:
    #     pprint(res)

    # return "".join(res)


def check_numpy(g, s):
    # hit = np.zeros(N_LETTERS, dtype=bool)
    # res = np.zeros(N_LETTERS, dtype=int)

    # for i in range(N_LETTERS):
    #     if g[i] == s[i]:
    #         hit[i] = True
    #         res[i] = 2

    hit = g == s
    res = np.where(hit, 2, 0)

    for i in range(N_LETTERS):
        if res[i] == 0:
            for j in range(N_LETTERS):
                if g[i] == s[j] and not hit[j]:
                    res[i] = 1
                    hit[j] = True
                    break
    return res


@jit(nopython=True)
def check_numba(g, s):
    hit = np.zeros(N_LETTERS, np.bool_)
    res = np.zeros(N_LETTERS, np.int_)
    # res = np.zeros(N_LETTERS, dtype=jit.types.int8)
    for i in range(N_LETTERS):
        if g[i] == s[i]:
            hit[i] = True
            res[i] = 2

    for i in range(N_LETTERS):
        if res[i] == 0:
            for j in range(N_LETTERS):
                if g[i] == s[j] and not hit[j]:
                    res[i] = 1
                    hit[j] = True
                    break
    return res


def test_check_normal():
    for a in answers:
        check(a, "other")


def test_check_numpy():
    for a in answers:
        check_numpy(a, "other")


@jit(nopython=True)
def test_check_numba(words):
    for a in words:
        check_numba(a, "other")


def monte_carlo_pi_normal(nsamples):
    acc = 0
    for i in range(nsamples):
        x = random.random()
        y = random.random()
        if (x**2 + y**2) < 1.0:
            acc += 1
    return 4.0 * acc / nsamples
