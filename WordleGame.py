from enum import Enum
import random
from wordLists import answers, guesses
from tqdm.auto import tqdm
import numpy as np


class WordleGame(object):
    def __init__(self, debug=False, forcedGuesses=[]) -> None:
        self.nLetters = 5
        self.validGuesses = guesses
        self.validAnswers = answers
        self.debug = debug

        self.previousResults = []

        self.forcedGuesses = forcedGuesses

        self.checkCache = {}

    def check(self, guess, answer, debug=False):
        # key = guess + answer
        # if key not in self.checkCache: key = answer + guess
        # if key not in self.checkCache:
        res = ["0"] * self.nLetters
        hit = [False] * self.nLetters
        for i in range(self.nLetters):
            if guess[i] == answer[i]:
                res[i] = "2"
                hit[i] = True
        for i in range(self.nLetters):
            if res[i] == "0":
                for j in range(self.nLetters):
                    if guess[i] == answer[j] and not hit[j]:
                        res[i] = "1"
                        hit[j] = True
                        break
        if debug:
            self.pprint(res)

        return "".join(res)

    def manualCheck(self):
        return input("Result from guess: ")

    def play(self, answer=None, manual=False, forcedGuesses=[]):
        self.resetPlayer()
        self.previousResults = []
        self.forcedGuesses = forcedGuesses

        if answer is None and not manual:
            answer = random.choice(self.validAnswers)

        nTurns = 0
        while True:
            guess = self.getNextGuess()
            if self.debug:
                print("Guess: ", guess)
            nTurns += 1

            if manual:
                res = self.manualCheck()
                self.pprint(res)
            else:
                res = self.check(guess, answer, self.debug)

            self.previousResults.append(res)
            if all(x == "2" for x in res):
                break
            elif nTurns == 100:
                if self.debug:
                    print("aight wtf, reached 100 guesses")
                break
        return nTurns

    def resetPlayer(self):
        raise NotImplementedError("Please Implement this method")

    def getNextGuess(self):
        raise NotImplementedError("Please Implement this method")

    def pprint(self, res):
        for x in res:
            if x == "1":
                print("\U0001f7e8", end="")
            elif x == "2":
                print("\U0001f7e9", end="")
            else:
                print("\u2B1B", end="")
        print("")

    def runAllPossibleAnswers(self, forcedGuesses=[], overrideDebug=False):
        tempDebug = self.debug
        self.debug = False or overrideDebug
        scores = []
        for answer in tqdm(self.validAnswers):
            scores.append(self.play(answer, forcedGuesses=forcedGuesses))
        self.debug = tempDebug
        return scores
