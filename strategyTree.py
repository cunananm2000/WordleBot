from audioop import avg
from cmath import exp
from utils import getWordFreq, check, getSplits, filterPossible
from wordLists import guesses, answers, commonWords
from tqdm.auto import tqdm
from valuations import *
import json


G = sorted(guesses + answers)
S = sorted(answers)

def v(g, C):
    return (information(g, C), 1-(g in C))

def agg(a):
    return sum([x[0] for x in a])


def sigma(L, C):
    print(f"{'   ' * L} Called with {len(C)} candidates")
    if len(C) == 1:
        print(f"Only one candidate {C[0]}")
        return C[0]

    sortedG = sorted([(v(g, C), g) for g in tqdm(G)])
    print(sortedG[:5])
    if L == 1:
        guess = sortedG[0][-1]
        print(f"Submitting {guess}")
        return guess
    
    futures = []
    for _,g in tqdm(sortedG[:5]):
        print(f"Investigating {g} further")
        splits = getSplits(g, C, useWords = True)
        scores = []
        for res,cands in tqdm(splits.items()):
            # Can use a bound here since we can keep track of the largest future split here
            followUpGuess = sigma(L-1, cands)
            score = v(followUpGuess, cands)
            print(f" After getting g={g}, res=({res},{len(cands)}), follow with {followUpGuess} -> {score}")

            scores.append(score)

        futures.append(((agg(scores), 1 - (g in C)), g))

        print(f"{'  ' * L} --> {g}: {agg(scores)}")

    futures.sort()
    for s,g in futures:
        print(f"{'   ' * L} Future {g} --> {s}")
    guess = futures[0][-1]
    print(f"{'   ' * L} Submitting {guess}")
    return guess

def genStrategyTree(L, C):
    tree = {}
    g = sigma(L, C)
    tree['guess'] = g 
    if len(C) != 1:
        splits = getSplits(g, C, useWords=True)
        tree['splits'] = {}

        for k, v in splits.items():
            if k == '22222': continue
            tree['splits'][k] = genStrategyTree(L, v)
        
    return tree

def writeStrategyTree(L):
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

    tree = genStrategyTree(L, S)

    with open(f'lookAheadTrees/information{L}.json', 'w') as f:
        json.dump(tree, f, sort_keys=True, indent = 4)

if __name__ == "__main__":
    writeStrategyTree(3)
