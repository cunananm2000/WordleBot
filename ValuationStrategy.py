from WordleGame import WordleGame
from tqdm.auto import tqdm
from utils import getWordFreq, filterPossible
import pandas as pd


class ValuationStrategy(WordleGame):
    def __init__(
        self,
        debug=False,
        forcedGuesses=[],
        valuations=[lambda g: 1],
        hardMode=False,
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)
        self.debug = debug

        self.allPossible = (self.validAnswers + self.validGuesses).copy()
        self.candidates = (self.validAnswers).copy()

        self.forcedGuessIdx = 0
        self.forcedGuesses = forcedGuesses

        self.valuations = valuations

        self.wordFreqs = {}
        for word in tqdm(self.allPossible):
            self.wordFreqs[word] = getWordFreq(word)

        self.hardMode = hardMode

    def resetPlayer(self):
        self.forcedGuessIdx = 0
        self.candidates = self.validAnswers.copy()

    def getNextGuess(self):
        if len(self.previousResults) > 0:
            self.candidates = filterPossible(
                self.previousGuesses[-1], self.previousResults[-1], self.candidates
            )

        assert len(self.candidates) != 0

        if self.debug:
            print(f"# Remaining: {len(self.candidates)}")

        guess = self.allPossible[0]
        if self.forcedGuessIdx < len(self.forcedGuesses):
            guess = self.forcedGuesses[self.forcedGuessIdx]
            self.forcedGuessIdx += 1
        elif len(self.candidates) <= 2:
            guess = self.candidates[0]
        else:

            validGuesses = self.candidates if self.hardMode else self.allPossible

            scores = [
                ([v(g, self.candidates) for v in self.valuations], -self.wordFreqs.get(g, 0), g)
                for g in tqdm(validGuesses)
            ]
            scores.sort()
            guess = scores[0][-1]

            # if self.hardMode:
            #     guess = [x for x in scores if x[-1] in self.candidates][0][-1]

            if self.debug:
                if not self.hardMode:
                    print("*** Top possible ***")
                    df = pd.DataFrame(columns=["val", "freq", "guess"], data=scores[:5])
                    df = df[["guess", "val", "freq"]]
                    print(df)

                    # for *info, g in scores[:5]:
                    #     print(*info,'-->',g)

                print("*** Top valid ***")
                # for *info, g in [x for x in scores if x[-1] in self.consistentGuesses][:5]:
                #     print(*info,'-->',g)

                df = pd.DataFrame(
                    columns=["val", "freq", "guess"],
                    data=[x for x in scores if x[-1] in self.candidates][:5],
                )
                df = df[["guess", "val", "freq"]]
                print(df)

        return guess

    def getPlayerName(self):
        return ','.join([v.__name__ for v in self.valuations])
