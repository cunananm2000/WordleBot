from WordleGame import WordleGame
from tqdm.auto import tqdm
import gc

class SmallestMaximumStrategy(WordleGame):
    def __init__(self, debug = False, **kwargs) -> None:
        super().__init__(**kwargs)
        self.debug = debug
        self.allPossible = (self.validAnswers + self.validGuesses).copy()
        self.originalAllPossible = self.allPossible.copy()
        self.forcedGuessIdx = 0
        self.lastGuess = None
        self.forcedGuesses = ['serai']
        self.nGuesses = 0

        # Since first guess is gonna be the same no matter what, cache which result leads to which next guess
        self.secondTurnGuesses = {}

    def resetPlayer(self):
        self.allPossible = self.originalAllPossible.copy()
        self.forcedGuessIdx = 0
        self.lastGuess = None
        self.nGuesses = 0

    def filterPossible(self, possibleGuess, possibleRes):
        return [x for x in self.allPossible if self.check(possibleGuess, x) == possibleRes]

    def maximumIfGuessed(self, possibleGuess):
        results = {}
        for x in self.allPossible:
            res = self.fromEnum(self.check(possibleGuess,x))
            # print(x,'-->')
            # self.pprint(self.toEnum(res))
            results[res] = results.get(res,0) + 1
        # print(results)
        score = max(results.values())
        del results
        return score

    def getNextGuess(self):
        self.nGuesses += 1
        resKey = None
        if self.lastGuess is not None:
            lastRes = self.previousResults[-1]
            resKey = self.fromEnum(lastRes)

            self.allPossible = self.filterPossible(self.lastGuess, lastRes)

        if self.debug: print("Possible set:", len(self.allPossible))

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
            assert(False)
        else:
            lowestScore = 0
            # i = 0
            for x in tqdm(self.originalAllPossible, colour = 'blue'):
                score = self.maximumIfGuessed(x)
                # print(x,'-->',score)
                if bestGuess is None or score <= lowestScore:
                    bestGuess = x
                    lowestScore = score
                # i += 1
                # if i % 100 == 0: gc.collect()

            if self.nGuesses == 2:
                self.secondTurnGuesses[resKey] = bestGuess

            if self.debug: print("Best score:", lowestScore)
        
        print(self.nGuesses,':',resKey,'--->',bestGuess)
        self.lastGuess = bestGuess
        return bestGuess
