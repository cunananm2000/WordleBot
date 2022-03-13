from WordleGame import WordleGame
from tqdm.auto import tqdm
import math
from utils import *


class SmallestEntropyStrategy(WordleGame):
    def __init__(self, debug=False, hardMode=False, **kwargs) -> None:
        super().__init__(**kwargs)
        self.debug = debug
        self.allPossible = (self.validAnswers + self.validGuesses).copy()
        self.originalAllPossible = self.allPossible.copy()
        self.forcedGuessIdx = 0
        self.lastGuess = None
        self.forcedGuesses = []
        self.nGuesses = 0
        self.hardMode = hardMode

        # Since first guess is gonna be the same no matter what, cache which result leads to which next guess
        self.secondTurnGuesses = {}

        self.wordFreqs = getWordFreqDict()

    def resetPlayer(self):
        self.allPossible = self.originalAllPossible.copy()
        self.forcedGuesses = []
        self.forcedGuessIdx = 0
        self.lastGuess = None
        self.nGuesses = 0

    def filterPossible(self, possibleGuess, possibleRes):
        return [
            x for x in self.allPossible if self.check(possibleGuess, x) == possibleRes
        ]

    def entropyIfGuessed(self, possibleGuess):
        results = {}
        nPossible = len(self.allPossible)
        for x in self.allPossible:
            res = self.fromEnum(self.check(possibleGuess, x))
            # print(x,'-->')
            # self.pprint(self.toEnum(res))
            results[res] = results.get(res, 0) + 1 - self.wordFreqs.get(x, 0)
        # print(results)

        # should really be negative score, but we're trying to minimize entropy
        score = sum(
            (r / nPossible) * math.log2(r / nPossible) for r in results.values()
        )

        if possibleGuess in self.allPossible:
            score *= 1 + 1 / nPossible
            score *= 1 + self.wordFreqs.get(possibleGuess, 0)
        return score

    def getNextGuess(self):
        self.nGuesses += 1
        resKey = None
        if self.lastGuess is not None:
            lastRes = self.previousResults[-1]
            resKey = self.fromEnum(lastRes)

            self.allPossible = self.filterPossible(self.lastGuess, lastRes)

        if self.debug:
            print("Possible set:", len(self.allPossible))
        #     if len(self.allPossible) < 10:
        #         print(self.allPossible)

        bestGuess = None
        if self.forcedGuessIdx < len(self.forcedGuesses):
            bestGuess = self.forcedGuesses[self.forcedGuessIdx]
            self.forcedGuessIdx += 1
        elif self.nGuesses == 2 and resKey in self.secondTurnGuesses:
            print("Used cache!")
            bestGuess = self.secondTurnGuesses[resKey]
        elif len(self.allPossible) == 1:
            bestGuess = self.allPossible[0]
        elif len(self.allPossible) == 0:
            print("Uhhh somehow nothing possible left?????")
            assert False
        else:
            lowestScore = 0
            # i = 0
            wordSet = self.allPossible if self.hardMode else self.originalAllPossible
            for x in tqdm(wordSet, colour="blue"):
                score = self.entropyIfGuessed(x)
                if self.debug:
                    if len(self.allPossible) < 10 and x in self.allPossible:
                        print(x, "-->", score, ",", self.wordFreqs.get(x, 0))
                if bestGuess is None or score <= lowestScore:
                    bestGuess = x
                    lowestScore = score
                # i += 1
                # if i % 100 == 0: gc.collect()

            if self.nGuesses == 2:
                self.secondTurnGuesses[resKey] = bestGuess

            if self.debug:
                print("Best score:", lowestScore)

        print(self.nGuesses, ":", resKey, "--->", bestGuess)
        self.lastGuess = bestGuess
        return bestGuess