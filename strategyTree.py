from utils import getWordFreq, check, getSplits
from wordLists import guesses, answers
from tqdm.auto import tqdm
from valuations import *
import json

def genStrategyTree(candidates, valuation , depth = 0):
    if len(candidates) == 1:
        print(f'{"  "*depth}Leaf: {candidates[0]}, depth = {depth}')
        return {
            'guess': candidates[0]
        }
    
    scores = [
        (
            valuation(g, candidates),
            -getWordFreq(g),
            g
        )
        for g in tqdm(guesses + answers, desc=f'{"  "*depth}Depth: {depth}')
    ]
    scores.sort()
    guess = scores[0][-1]

    res = {
        'guess': guess,
        'nRemaining': len(candidates),
        'splits': {}
    }

    print(f'{"  "*depth}Guess: {guess}, Remaining: {len(candidates)}')

    for response, split in getSplits(guess, candidates, useWords=True).items():
        if response == '22222': continue
        res['splits'][response] = genStrategyTree(split, valuation, depth = depth + 1)

    return res

if __name__ == "__main__":
    tree = genStrategyTree(guesses + answers, information)

    with open('trees/information.json','w') as f:
        json.dump(tree, f, sort_keys = True, indent = 4)