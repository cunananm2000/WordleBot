from WordleGame import WordleGame
from tqdm.auto import tqdm
from utils import getWordFreq, filterPossible
from strategyTree import writeStrategyTree
import pandas as pd
import json


class ValuationStrategyCached(WordleGame):
    def __init__(
        self, debug=False, onlyCommon = False, forcedGuesses=[], valuation=lambda g: 1, **kwargs
    ) -> None:
        super().__init__(**kwargs)
        self.debug = debug

        folder = 'commonTrees' if onlyCommon else 'trees'

        self.strategy = {}

        try:
            f = open(f"{folder}/{valuation.__name__}.json")
        except FileNotFoundError:
            print("Need to write file")
            writeStrategyTree(valuation, onlyCommon)

        with open(f"{folder}/{valuation.__name__}2.json") as f:
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

        if self.debug and "nRemaining" in curr:
            print(f"Remaining:", curr["nRemaining"])

        return curr["guess"]
