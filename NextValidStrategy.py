from WordleGame import WordleGame


class NextValidStrategy(WordleGame):
    def __init__(self, debug=False, **kwargs) -> None:
        super().__init__(**kwargs)
        self.debug = debug
        self.allPossible = (self.validAnswers + self.validGuesses).copy()
        self.lastGuess = None

    def resetPlayer(self):
        self.allPossible = (self.validAnswers + self.validGuesses).copy()
        self.lastGuess = None

    def filterPossible(self, possibleGuess, possibleRes):
        return [
            x for x in self.allPossible if self.check(possibleGuess, x) == possibleRes
        ]

    def getNextGuess(self):
        if self.lastGuess is not None:
            lastRes = self.previousResults[-1]
            self.allPossible = self.filterPossible(self.lastGuess, lastRes)

        guess = self.allPossible[0]

        self.lastGuess = guess
        return guess
