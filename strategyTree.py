import json
from itertools import permutations
from os.path import exists

from tqdm.auto import tqdm

from utils import getSplits
from valuations import *
from Config import Config


c = Config('oldWordle')
G = c.guesses
S = c.answers


class TreeGenerator(object):
    def __init__(self, vs=[inSet], aggFn=max):
        self.vs = vs
        self.aggFn = aggFn

        self.stratName = ','.join([val.__name__ for val in self.vs])
        self.tree = None

    def v(self, g, C):

        # return (maxSizeSplit(g, C), firstValid(g, C), mostParts(g, C))
        return tuple(val(g, C) for val in self.vs)

    def agg(self, a):
        return self.aggFn([x[0] for x in a])

    def sigma(self, L, C):
        print(f"{'   ' * L} Called with {len(C)} candidates")
        if len(C) == 1:
            print(f"Only one candidate {C[0]}")
            return C[0]

        if len(C) == 2:
            print(f"Got two candidates, guessing {C[0]}")
            return C[0]

        sortedG = sorted([(self.v(g, C), g) for g in tqdm(G)])
        print(sortedG[:5])
        if L == 1:
            guess = sortedG[0][-1]
            if len(C) < 30:
                print(C)
                print(getSplits(guess, C))
                print(self.v(guess, C))
            print(f"Submitting {guess}")
            return guess

        assert False

        futures = []
        for _, g in tqdm(sortedG[:5]):
            print(f"Investigating {g} further")
            splits = getSplits(g, C, useWords=True)
            scores = []
            for res, cands in tqdm(splits.items()):
                # Can use a bound here since we can keep track of the largest future split here
                followUpGuess = self.sigma(L - 1, cands)
                score = self.v(followUpGuess, cands)
                print(
                    f" After getting g={g}, res=({res},{len(cands)}), follow with {followUpGuess} -> {score}"
                )

                scores.append(score)

            futures.append(((self.agg(scores), 1 - (g in C)), g))

            print(f"{'  ' * L} --> {g}: {self.agg(scores)}")

        futures.sort()
        for s, g in futures:
            print(f"{'   ' * L} Future {g} --> {s}")
        guess = futures[0][-1]
        print(f"{'   ' * L} Submitting {guess}")
        return guess

    def genStrategyTree(self, L, C):
        tree = {}
        g = self.sigma(L, C)
        tree["guess"] = g
        tree["nRemaining"] = len(C)
        if len(C) != 1:
            splits = getSplits(g, C, useWords=True)
            tree["splits"] = {}

            for k, v in splits.items():
                if k == "22222":
                    continue
                tree["splits"][k] = self.genStrategyTree(L, v)

        self.tree = tree
        return tree

    def scoreTree(self, words):
        if self.tree is None: assert(False)
        #     r = [1]
        #     if 'splits' in T:
        #         for k in T['splits']:
        #             r += [1 + x for x in g(T['splits'][k])]
        #     return r
        r = []
        for w in words:
            s = 1
            curr = self.tree
            res = check(curr['guess'],w)
            while res != '22222':
                s += 1
                curr = curr['splits'][res]
                res = check(curr['guess'],w)
                
            r.append(s)
        return r


    def writeStrategyTree(self, L):
        # tree = {}

        # forcing a guess
        # g = 'raise' # L = 1
        # g = 'reais' # L = 2
        # g = 'aesir' # L = 3
        # tree['guess'] = g

        # splits = getSplits(g, S, useWords=True)
        # tree['splits'] = {}

        # for k, v in splits.items():
        #     tree['splits'][k] = genStrategyTree(L, v)

        fname = f"standardTrees/{self.stratName}{L}.json"
        
        
        if exists(fname): 
            print(f"Already see {fname}")
            return

        tree = self.genStrategyTree(L, S)

        with open(fname, "w") as f:
            json.dump(tree, f, sort_keys=True, indent=4)


if __name__ == "__main__":
    # allVals = [firstValid, maxSizeSplit, mostParts, information]

    # fns = sum([
    #     list(permutations(allVals, i)) for i in range(1,len(allVals)+1)
    # ], [])

    fns = [
        # maxSizeSplit,
        # mostParts,
        # information,
        # probsGreen,
        # minRange,
        # expSizeSplit,
        # harmonicMean,
        # minStdDev,
        charFreqs,
        minStdDev,
    ]

    # for f in fns:
    #     print(f)
    # print(len(fns))
    # assert(False)
    for f in fns:
        treeGen = TreeGenerator(vs=[f, inSet], aggFn=None)
        treeGen.writeStrategyTree(1)
