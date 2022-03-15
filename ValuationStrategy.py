from WordleGame import WordleGame
from tqdm.auto import tqdm
from utils import getWordFreq
import pandas as pd

class ValuationStrategy(WordleGame):
    def __init__(
        self, debug=False, forcedGuesses=[], valuation=lambda g: 1, **kwargs
    ) -> None:
        super().__init__(**kwargs)
        self.debug = debug

        self.allPossible = (self.validAnswers + self.validGuesses).copy()
        self.consistentGuesses = (self.validAnswers + self.validGuesses).copy()

        self.forcedGuessIdx = 0
        self.forcedGuesses = forcedGuesses

        self.strategy = {
            # 'guess': 'tares',
            # 'responses': {
            #     'YYYYY': {
            #         'guess': 'sepia',
            #         'responses': {
            #         }
            #     },
            #     'YYYYg': {
            #         'guess': 'sepia',
            #         'responses': {
            #         }
            #     }
            # }
        }
        # nextGuess
        # splits

        self.valuation = valuation

        self.wordFreqs = {}
        for word in tqdm(self.allPossible):
            self.wordFreqs[word] = getWordFreq(word)

    def resetPlayer(self):
        self.forcedGuessIdx = 0
        self.consistentGuesses = self.allPossible.copy()

    def filterPossible(self, possibleGuess, possibleRes):
        return [
            x
            for x in self.consistentGuesses
            if self.check(possibleGuess, x) == possibleRes
        ]

    def getNextGuess(self):
        if len(self.previousResults) > 0:
            self.consistentGuesses = self.filterPossible(
                self.previousGuesses[-1], self.previousResults[-1]
            )

        assert len(self.consistentGuesses) != 0

        if self.debug:
            print(f"# Remaining: {len(self.consistentGuesses)}")

        guess = self.allPossible[0]
        if self.forcedGuessIdx < len(self.forcedGuesses):
            guess = self.forcedGuesses[self.forcedGuessIdx]
            self.forcedGuessIdx += 1
        elif len(self.allPossible) == 1:
            guess = self.allPossible[0]
        else:
            # bestScore = self.valuation(guess, self.consistentGuesses, self.check)
            # # print(guess, bestScore)
            # for g in tqdm(self.allPossible[1:]):
            #     score = self.valuation(g, self.consistentGuesses, self.check)
            #     # print(g, score)
            #     if score < bestScore:
            #         bestScore = score
            #         guess = g

            scores = [
                (
                    self.valuation(g, self.consistentGuesses, self.check),
                    -self.wordFreqs.get(g, 0),
                    g
                )
                for g in tqdm(self.allPossible)
            ]
            scores.sort()
            guess = scores[0][-1]

            if self.debug:
                print("*** Top possible ***")
                df = pd.DataFrame(columns = ['val','freq','guess'], data = scores[:5])
                df = df[['guess','val','freq']]
                print(df)

                # for *info, g in scores[:5]:
                #     print(*info,'-->',g)

                print("*** Top valid ***")
                # for *info, g in [x for x in scores if x[-1] in self.consistentGuesses][:5]:
                #     print(*info,'-->',g)

                df = pd.DataFrame(columns = ['val','freq','guess'], data = [x for x in scores if x[-1] in self.consistentGuesses][:5])
                df = df[['guess','val','freq']]
                print(df)


        return guess

    # def valuation(self, guess):
    #     return 1
