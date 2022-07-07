import json
from utils import filterPossible, getSplits, saveAsWordList, sortWords, filterMultiple, softFilterPossible, softFilterMultiple, noFilterPossible
# from mathlerLists import guesses, answers, rStar
from tqdm.auto import tqdm
from valuations import *
from Config import Config


class BaseOptimizer(object):
    def __init__(
        self,
        MAX_DEPTH = 10,
        MAX_BREADTH = 20,
        hardMode = False,
        game = 'temp',
        DEBUG_LEVEL = 2,
    ):
        c = Config(game)

        self.G = c.guesses
        self.S = c.answers
        self.rStar = c.rStar

        self.MAX_DEPTH = MAX_DEPTH
        self.vals = [mostParts, firstValid, maxSizeSplit]
        self.MAX_BREADTH = MAX_BREADTH
        self.hardMode = hardMode
        self.game = game
        self.DEBUG_LEVEL = DEBUG_LEVEL

        self.guessFilter = softFilterPossible if hardMode else noFilterPossible

        self.BREACHES = 0
        self.HITS = 0
        self.CALLS = 0
        
        self.bestGuess = {}
        self.bestScore = {}

        self.fname = f"{self.game}_{self.MAX_BREADTH}{'_hard' if self.hardMode else ''}"

        self.tree = None

    def encode(self, subset, superset):
        if len(subset) == len(superset):
            return 0
        t = 0
        for c in subset:
            t |= 1 << (len(superset) - superset.index(c) - 1)
        return t

    def explore(self, possibleGuesses, possibleAnswers, depth = 1):
        raise NotImplementedError("Look ahead function")

    def genTree(self, possibleGuesses, possibleAnswers, depth = 1):
        # print(len(possibleGuesses), len(possibleAnswers), possibleAnswers)
        code = (
            self.encode(possibleAnswers, self.S), 
            self.encode(possibleGuesses, self.G)
        )

        if code not in self.bestGuess:
            self.explore(
                possibleGuesses = possibleGuesses, 
                possibleAnswers = possibleAnswers,
                depth = depth
            )
        
        guess = self.bestGuess[code]
        score = self.bestScore[code]

        tree = {'guess': guess, 'score': score, 'nRemaining': len(possibleAnswers)}
        if len(possibleAnswers) != 1:
            tree['splits'] = {}
            splits = getSplits(guess, possibleAnswers, useWords=True)
            for res, split in splits.items():
                if res == self.rStar: continue 
                tree['splits'][res] = self.genTree(
                    possibleGuesses = self.guessFilter(guess, res, possibleGuesses),
                    possibleAnswers = split,
                    depth = depth + 1
                )
        
        return tree

    def getTree(self):
        if self.tree is None:
            self.tree = self.genTree(
                possibleGuesses=self.G,
                possibleAnswers=self.S
            )
        return self.tree

    def writeJson(self):
        print("Writing JSON...")
        tree = self.getTree()
        with open(f"optimizedTrees/{self.fname}.json", "w") as f:
            json.dump(tree, f, sort_keys=True, indent=4)
        print("Wrote JSON!")
        
    def writeWordList(self):
        print("Writing word list...")
        saveAsWordList(
            tree = self.getTree(),
            fname = f"optimizedTrees/{self.fname}.txt",
            answers = self.S
        )
        print("Wrote word list!")

    def showStats(self):
        print("----- GAME:",self.game.capitalize(),"-----")
        print("HARD MODE ON?:", self.hardMode)
        print("# POSSIBLE SECRETS:", len(self.S))
        print("# POSSIBLE GUESSES:", len(self.G))
        print("MAX BREADTH:", self.MAX_BREADTH)
        print("MAX_DEPTH:",self.MAX_DEPTH)
        score = self.bestScore[(self.encode(self.S,self.S), self.encode(self.G,self.G))]
        print("BEST SCORE:", score)
        print("HITS:", self.HITS)
        print("BREACHES:", self.BREACHES)
        print("CALLS: ", self.CALLS)