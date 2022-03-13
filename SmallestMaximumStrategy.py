from xml.etree.ElementPath import xpath_tokenizer_re
from WordleGame import WordleGame
from tqdm.auto import tqdm
import gc


class SmallestMaximumStrategy(WordleGame):
    def __init__(self, debug=False, **kwargs) -> None:
        super().__init__(**kwargs)
        self.debug = debug
        self.allPossible = (self.validAnswers + self.validGuesses).copy()
        self.originalAllPossible = self.allPossible.copy()
        self.forcedGuessIdx = 0
        self.lastGuess = None
        self.forcedGuesses = ["serai"]
        self.nGuesses = 0

        # Since first guess is gonna be the same no matter what, cache which result leads to which next guess
        self.secondTurnGuesses = {}

    def resetPlayer(self):
        self.allPossible = self.originalAllPossible.copy()
        self.forcedGuessIdx = 0
        self.lastGuess = None
        self.nGuesses = 0

    def filterPossible(self, possibleGuess, possibleRes, possibleSet=None):
        if possibleSet is None:
            possibleSet = self.allPossible
        return [x for x in possibleSet if self.check(possibleGuess, x) == possibleRes]

    def maximumIfGuessed(self, possibleGuess, possibleSet=None):
        if possibleSet is None:
            possibleSet = self.allPossible
        # print(possibleGuess,len(possibleSet))
        results = {}
        for x in possibleSet:
            res = self.fromEnum(self.check(possibleGuess, x))

            # print(len(self.filterPossible(
            #                 possibleGuess=possibleGuess,
            #                 possibleRes=res,
            #                 possibleSet=possibleSet
            #             )))
            # print(x,'-->')
            # self.pprint(self.toEnum(res))
            # if res in results:
            #     results[res] = max(results[res],v)
            # else:

            results[res] = results.get(res, 0) + 1
            # if level == 0:
            #     results[res] = results.get(res,0) + 1
            # else:
            #     results[res] = max(
            #         results.get(res,0),
            #         self.maximumIfGuessed(
            #             x,
            #             possibleSet = self.filterPossible(
            #                 possibleGuess=possibleGuess,
            #                 possibleRes=self.toEnum(res),
            #                 possibleSet=possibleSet
            #             ),
            #             level = level - 1
            #         )
            #     )
        # print(results)
        score = max(results.values())
        # del results
        return score

    def getNextGuess(self):
        self.nGuesses += 1
        resKey = None
        if self.lastGuess is not None:
            lastRes = self.previousResults[-1]
            resKey = self.fromEnum(lastRes)

            self.allPossible = self.filterPossible(self.lastGuess, lastRes)

        if self.debug:
            print("Possible set:", len(self.allPossible))

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
            assert False
        else:
            lowestScore = 0
            # i = 0
            for x in tqdm(self.originalAllPossible, colour="blue"):
                score = self.maximumIfGuessed(x)
                # print(x,'-->',score)
                if bestGuess is None or score <= lowestScore:
                    bestGuess = x
                    lowestScore = score
                # i += 1
                # if i % 100 == 0: gc.collect()

            if self.nGuesses == 2:
                self.secondTurnGuesses[resKey] = bestGuess

            if self.debug:
                print("Best score:", lowestScore)

        print(self.nGuesses, ":", resKey, "--->", bestGuess)
        self.lastGuess = bestGuess
        return bestGuess
