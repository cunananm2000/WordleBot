from itertools import combinations

from IPython.lib.pretty import pprint
from tqdm.auto import tqdm

from utils import check, getWordFreq
from wordLists import *


class StaticWordle(object):
    def __init__(
        self,
        candidates=commonWords,
        gameAnswers=answers,
        gameGuesses=guesses,
        debug=True,
    ):
        self.candidates = commonWords
        self.answers = gameAnswers
        self.guesses = gameGuesses
        self.debug = debug

    def evaluateSet(self, querySet, hideDebug=False, cheat=False):
        classes = {}
        wordSet = self.answers if cheat else self.candidates
        for c in tqdm(wordSet, disable=hideDebug):
            vec = ""
            for q in querySet:
                vec += check(q, c)
            if vec not in classes:
                classes[vec] = []
            classes[vec].append(c)

        if self.debug and not hideDebug:
            its = list(classes.items())
            its.sort(key=lambda x: -len(x[1]))
            for k, v in its[:5]:
                print(*[k[i:i+5] for i in range(0, len(k), 5)], "-->", len(v))
                # from IPython.lib.pretty import pprint
                print("    ", end="")
                v.sort(key=lambda x: -getWordFreq(x))
                pprint(v, max_seq_length=5)

        return max(map(len, classes.values()))

    def findBestN(self, n, hideDebug=False, cheat=False):
        combs = list(combinations(self.guesses, n))
        # wordSet = self.answers if cheat else self.candidates
        # bestScore = len(wordSet)
        # bestComb = None

        pairs = []
        for comb in tqdm(combs):
            s = self.evaluateSet(list(comb), hideDebug=True, cheat=cheat)

            # if self.debug and not hideDebug:
            #     print(list(comb),'-->',s)

            # if s < bestScore:
            #     bestScore = s
            #     bestComb = list(comb)

            pairs.append((comb, s))

        pairs.sort(key=lambda x: (x[1], -sum(map(getWordFreq, x[0]))))

        if self.debug and not hideDebug:
            print("***BEST 5***")
            for i in range(5):
                print(pairs[i][0], "-->", pairs[i][1])

        return pairs[0]
