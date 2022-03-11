from WordleGame import WordleGame

class HumanStrategy(WordleGame):
    def __init__(self) -> None:
        super().__init__()
        self.debug = True

    def resetPlayer(self):
        pass

    def getNextGuess(self):
        guess = input("Enter guess: ").lower()
        while guess not in self.validGuesses and guess not in self.validAnswers:
            guess = input("Not a valid guess, enter guess: ").lower()
        return guess
