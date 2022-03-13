from WordleGame import WordleGame


class BruteForceStrategy(WordleGame):
    def __init__(self, debug=False) -> None:
        super().__init__()
        self.guessIndex = 0
        self.debug = debug
        self.allPossible = self.validAnswers + self.validGuesses
        self.allPossible.sort()

    def resetPlayer(self):
        self.guessIndex = 0

    def getNextGuess(self):
        guess = self.allPossible[self.guessIndex]
        self.guessIndex += 1
        return guess
