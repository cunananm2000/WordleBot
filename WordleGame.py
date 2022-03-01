from enum import Enum
import random
from wordLists import answers, guesses
from tqdm.auto import tqdm
import numpy as np

class Color(Enum):
    GREY = 0
    YELLOW = 1
    GREEN = 2

class WordleGame(object):
    def __init__(self, forcedGuesses = []) -> None:
        self.nLetters = 5
        self.validGuesses = guesses
        self.validAnswers = answers
        self.debug = False

        self.previousResults = []

        self.readableMap = {
            'g': Color.GREY,
            'G': Color.GREEN,
            'Y': Color.YELLOW
        }
        
        self.forcedGuesses = forcedGuesses

        self.computerMap = {}
        for k,v in self.readableMap.items(): self.computerMap[v] = k

        self.checkCache = {}

    def check(self, guess, answer, debug = False):
        # key = guess + answer
        # if key not in self.checkCache: key = answer + guess
        # if key not in self.checkCache:
        res = [Color.GREY] * self.nLetters
        hit = [False] * self.nLetters
        for i in range(self.nLetters):
            if guess[i] == answer[i]: 
                res[i] = Color.GREEN
                hit[i] = True
        for i in range(self.nLetters):
            if res[i] == Color.GREY:
                for j in range(self.nLetters):
                    if guess[i] == answer[j] and not hit[j]:
                        res[i] = Color.YELLOW
                        hit[j] = True
                        break
        if debug: self.pprint(res)
        return res
        #     self.checkCache[key] = res
        # return self.checkCache[key]

    def manualCheck(self):
        res = input("Result from guess: ")
        return self.toEnum(res)

    def toEnum(self, res):
        return [self.readableMap[k] for k in list(res)]

    def fromEnum(self, res):
        res = [self.computerMap[k] for k in res]
        return ''.join(res)


    def play(self, answer = None, manual = False, forcedGuesses = []):
        self.resetPlayer()
        self.previousResults = []
        self.forcedGuesses = forcedGuesses

        if answer is None and not manual:
            answer = random.choice(self.validAnswers)

        nTurns = 0
        while True:
            guess = self.getNextGuess()
            if self.debug: print("Guess: ", guess)
            nTurns += 1

            if manual:
                res = self.manualCheck()
            else:
                res = self.check(guess, answer, self.debug)
            
            self.previousResults.append(res)
            if all(x == Color.GREEN for x in res):
                break
            elif nTurns == 100:
                if self.debug: print("aight wtf, reached 100 guesses")
                break
        return nTurns

    def resetPlayer(self):
        raise NotImplementedError("Please Implement this method")

    def getNextGuess(self):
        raise NotImplementedError("Please Implement this method")
        
    def pprint(self, res):
        for x in res:
            if x == Color.YELLOW:
                print("\U0001f7e8", end='')
            elif x == Color.GREEN:
                print("\U0001f7e9", end='')
            else:
                print("\u2B1B", end='')
        print('')

    def runAllPossibleAnswers(self, forcedGuesses = []):
        tempDebug = self.debug
        self.debug = False
        scores = []
        for answer in tqdm(self.validAnswers): scores.append(self.play(answer, forcedGuesses = forcedGuesses))
        self.debug = True
        return scores

    