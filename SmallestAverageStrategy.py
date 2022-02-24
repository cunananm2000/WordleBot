from WordleGame import WordleGame
from tqdm.auto import tqdm
import gc

class SmallestAverageStrategy(WordleGame):
    def __init__(self, debug = False, **kwargs) -> None:
        super().__init__(**kwargs)
        self.debug = debug
        self.allPossible = (self.validAnswers + self.validGuesses).copy()
        self.originalAllPossible = self.allPossible.copy()
        self.forcedGuessIdx = 0
        self.lastGuess = None

    def resetPlayer(self):
        self.allPossible = self.originalAllPossible.copy()
        self.lastGuess = None

    def filterPossible(self, possibleGuess, possibleRes):
        return [x for x in self.allPossible if self.check(possibleGuess, x) == possibleRes]

    def averageIfGuessed(self, possibleGuess):
        results = {}
        for x in self.allPossible:
            res = self.fromEnum(self.check(possibleGuess,x))
            # print(x,'-->')
            # self.pprint(self.toEnum(res))
            results[res] = results.get(res,0) + 1
        # print(results)
        score = sum(results.values())/len(results)
        del results
        return score

    def getNextGuess(self):
        if self.lastGuess is not None:
            lastRes = self.previousResults[-1]
            self.allPossible = self.filterPossible(self.lastGuess, lastRes)

        if self.debug: print("Possible set:", len(self.allPossible))

        bestGuess = None
        if self.forcedGuessIdx < len(self.forcedGuesses):
            guess = self.forcedGuesses[self.forcedGuessIdx]
            self.forcedGuessIdx += 1
            self.lastGuess = guess
            return guess
        
        if len(self.allPossible) == 1:
            self.lastGuess = self.allPossible[0]
            return self.allPossible[0]

        bestGuess = None
        lowestScore = 0
        i = 0
        for x in tqdm(self.originalAllPossible, colour = 'blue'):
            score = self.averageIfGuessed(x)
            # print(x,'-->',score)
            if bestGuess is None or score < lowestScore:
                bestGuess = x
                lowestScore = score
            i += 1
            # if i % 100 == 0: gc.collect()

        if self.debug: print("Best score:", lowestScore)
        
        self.lastGuess = bestGuess
        return bestGuess
