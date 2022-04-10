from enum import Enum
import random
from wordLists import answers, guesses
from tqdm.auto import tqdm
import numpy as np
from utils import check, pprint


class WordleGame(object):
    def __init__(
        self, debug=False, forcedGuesses=[], validGuesses=None, validAnswers=None
    ) -> None:
        self.nLetters = 5
        self.validGuesses = guesses if validGuesses is None else validGuesses
        self.validAnswers = answers if validAnswers is None else validAnswers
        self.debug = debug

        self.previousGuesses = []
        self.previousResults = []

        self.forcedGuesses = forcedGuesses

    def manualCheck(self):
        return input("Result from guess: ")

    def play(self, answer=None, forcedGuesses=[], overrideSuggestion=False):
        self.resetPlayer()
        self.previousGuesses = []
        self.previousResults = []
        self.forcedGuesses = forcedGuesses

        # if answer is None and not manual:
        #     answer = random.choice(self.validAnswers)

        nTurns = 0
        while True:
            guess = self.getNextGuess()
            if overrideSuggestion:
                print("Suggested guess:", guess)
                manualGuess = input("Actual guess: ")
                if len(manualGuess) == self.nLetters and manualGuess.isalpha():
                    guess = manualGuess
            if self.debug:
                print("Guessing: ", guess)
            nTurns += 1

            if answer is None:
                res = self.manualCheck()
                pprint(res)
            else:
                res = check(guess, answer, debug=self.debug, nLetters=self.nLetters)

            self.previousGuesses.append(guess)
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

    def runAllPossibleAnswers(
        self, answers=None, forcedGuesses=[], overrideDebug=False
    ):
        tempDebug = self.debug
        self.debug = False or overrideDebug
        if answers is None:
            answers = self.validAnswers
        scores = []
        for answer in tqdm(answers):
            scores.append(self.play(answer, forcedGuesses=forcedGuesses))
        self.debug = tempDebug
        return scores
