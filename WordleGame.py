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
    def __init__(self, manual = False) -> None:
        self.nLetters = 5
        self.validGuesses = guesses
        self.validAnswers = answers
        self.debug = False
        self.manual = manual

        self.previousResults = []

        self.readableMap = {
            'g': Color.GREY,
            'G': Color.GREEN,
            'Y': Color.YELLOW
        }

    def check(self, guess, answer, debug = False):
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

    def manualCheck(self):
        res = list(input("Result from guess: "))
        res = [self.readableMap[k] for k in res]
        return res

    def play(self, answer = None):
        self.resetPlayer()
        self.previousResults = []

        if answer is None and not self.manual:
            answer = random.choice(self.validAnswers)

        nTurns = 0
        while True:
            guess = self.getNextGuess()
            if self.debug: print("Guess: ", guess)
            nTurns += 1

            if self.manual:
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

    def runAllPossibleAnswers(self):
        # return np.array([self.play(answer) for answer in self.validAnswers])
        scores = []
        for answer in tqdm(self.validAnswers): scores.append(self.play(answer))
        return scores

    