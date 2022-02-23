from WordleGame import WordleGame
import random

class RandomStrategy(WordleGame):
    def __init__(self, debug = False) -> None:
        super().__init__()
        self.guessIndex = 0
        self.debug = debug
        self.allPossible = self.validAnswers + self.validGuesses

        random.seed(10)

    def resetPlayer(self):
        self.guessIndex = 0
        random.shuffle(self.allPossible)

    def getNextGuess(self):
        guess = self.allPossible[self.guessIndex]
        self.guessIndex += 1
        return guess
