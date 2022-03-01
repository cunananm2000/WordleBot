from SmallestAverageStrategy import SmallestAverageStrategy
from tqdm.auto import tqdm
import math

class SmallestAverageStrategyEnglish(SmallestAverageStrategy):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        # Since first guess is gonna be the same no matter what, cache which result leads to which next guess
        self.wordFreqs = {}

        with open('wordFreqs.txt', encoding="utf8") as f:
            for line in f:
                v,k = line.split()
                self.wordFreqs[k] = float(v)
        hi = max(self.wordFreqs.values())
        for k in self.wordFreqs.keys():
            self.wordFreqs[k] = 1/(1 + math.exp(-(self.wordFreqs[k]/hi - 0.5)))

    
    def averageIfGuessed(self, possibleGuess):
        results = {}
        for x in self.allPossible:
            res = self.fromEnum(self.check(possibleGuess,x))
            # print(x,'-->')
            # self.pprint(self.toEnum(res))
            # if x in self.wordFreqs: print("got a discount", self.wordFreqs[x])
            results[res] = results.get(res,0) + 1/(1 + self.wordFreqs.get(x, 0))
        # print(results)

        score = sum(results.values())/len(results)
        # score /= (1 + self.wordFreqs.get(possibleGuess,0))
        # score /= (1 + (possibleGuess in self.allPossible)/len(self.allPossible))
        del results
        return score