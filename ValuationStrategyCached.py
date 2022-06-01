from WordleGame import WordleGame
from tqdm.auto import tqdm
from utils import getWordFreq, filterPossible
from strategyTree import writeStrategyTree
import pandas as pd
import json


class ValuationStrategyCached(WordleGame):
    def __init__(
        self,
        strategyFile,
        debug=False,
        # onlyCommon=False,
        # forcedGuesses=[],
        # valuation=lambda g: 1,
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)
        self.debug = debug

        # folder = "commonTrees" if onlyCommon else "trees"
        # self.strategy = {}
        # with open(f"{folder}/{valuation.__name__}.json") as f:
        #     self.strategy = json.load(f)

        self.fileName = strategyFile

        # self.valuation = valuation
        with open(strategyFile) as f:
            self.strategy = json.load(f)

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

    def getPlayerName(self):
        return self.strategy.get("name", self.fileName)
