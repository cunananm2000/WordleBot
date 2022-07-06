import json
from utils import filterPossible, getSplits, saveAsWordList, sortWords, filterMultiple, softFilterPossible, softFilterMultiple, noFilterPossible
from mathlerLists import guesses, answers, rStar
from tqdm.auto import tqdm
from valuations import *


class AverageOptimizer(object):
    def __init__(
        self, 
        possibleGuesses, 
        possibleAnswers,
        MAX_DEPTH = 10,
        MAX_BREADTH = 20,
        hardMode = False,
        game = 'temp',
        DEBUG_LEVEL = 2,
    ):
        self.G = possibleGuesses
        self.S = possibleAnswers
        self.MAX_DEPTH = MAX_DEPTH
        self.vals = [mostParts, firstValid, maxSizeSplit]
        self.MAX_BREADTH = MAX_BREADTH
        self.hardMode = hardMode
        self.game = game
        self.DEBUG_LEVEL = DEBUG_LEVEL

        self.guessFilter = softFilterPossible if hardMode else noFilterPossible

        self.BREACHES = 0
        self.HITS = 0
        
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
        code = (
            self.encode(possibleAnswers, self.S), 
            self.encode(possibleGuesses, self.G)
        )

        if code in self.bestScore:
            self.HITS += 1
            return self.bestScore[code]

        # Special cases first 
        if len(possibleAnswers) == 1:
            self.bestGuess[code] = possibleAnswers[0]
            self.bestScore[code] = 1
        elif len(possibleAnswers) == 2:
            self.bestGuess[code] = possibleAnswers[0]
            self.bestScore[code] = 1.5
        elif depth >= self.MAX_DEPTH:
            self.bestGuess[code] = possibleAnswers[0]
            self.bestScore[code] = 1000000
            self.BREACHES += 1
        else:
            # Shortcut since this always the best choice
            # if (depth == 1): 
            #     options = ['salet']
            # else:

            # print('here again',len(possibleAnswers))

            options = sortWords(
                C = possibleGuesses,
                S = possibleAnswers,
                vals = self.vals,
                n = self.MAX_BREADTH,
                showProg = (depth <= self.DEBUG_LEVEL),
            )

            # print(options)

            # print('also here', len(possibleAnswers))


            for g in tqdm(options, disable = not(depth <= self.DEBUG_LEVEL), colour = ['green','blue'][depth%2]):
                splits = getSplits(g, possibleAnswers, useWords=True)
                if len(splits) == 1: continue 
                # if (depth == 1): print(splits)
                t = 1
                for res, split in tqdm(splits.items(), disable = not(depth <= self.DEBUG_LEVEL), colour='yellow'):
                    if res == rStar: continue 
                    # if (depth <= 2):
                    #     print('    '*(depth-1),g,'-->',res)
                    t += len(split)/len(possibleAnswers) * self.explore(
                        possibleAnswers = split, 
                        possibleGuesses = self.guessFilter(g, res, possibleGuesses),
                        depth = depth + 1,
                    )

                if self.bestScore.get(code, 9999999) > t:
                    self.bestScore[code] = t
                    self.bestGuess[code] = g

        return self.bestScore[code]

    def genTree(self, possibleGuesses, possibleAnswers, depth = 1):
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
                if res == rStar: continue 
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
        with open(f"{self.fname}.json", "w") as f:
            json.dump(tree, f, sort_keys=True, indent=4)
        print("Wrote JSON!")
        
    def writeWordList(self):
        print("Writing word list...")
        saveAsWordList(
            tree = self.getTree(),
            fname = f"{self.fname}.txt",
            answers = self.S
        )
        print("Wrote word list!")

    def showStats(self):
        avg = self.bestScore[(self.encode(self.S,self.S), self.encode(self.G,self.G))]
        print("AVERAGE:", avg)
        print("TOTAL:",avg * len(self.S))
        print("HITS:", self.HITS)
        print("BREACHES:", self.BREACHES)