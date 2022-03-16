from WordleGame import WordleGame
from tqdm.auto import tqdm
from utils import getWordFreq, filterPossible
import pandas as pd
import json


class ValuationStrategyCached(WordleGame):
    def __init__(
        self, debug=False, forcedGuesses=[], valuation=lambda g: 1, **kwargs
    ) -> None:
        super().__init__(**kwargs)
        self.debug = debug

        self.strategy = {}
        with open(f"trees/{valuation.__name__}.json") as f:
            self.strategy = json.load(f)

        self.valuation = valuation

    def resetPlayer(self):
        pass

    def getNextGuess(self):
        curr = self.strategy
        for g, r in zip(self.previousGuesses, self.previousResults):
            assert curr["guess"] == g
            if r not in curr["splits"]:
                print("Possible splits are", *curr["splits"].keys())
                assert False
            curr = curr["splits"][r]

        if "nRemaining" in curr:
            print(f"Remaining:", curr["nRemaining"])

        return curr["guess"]
