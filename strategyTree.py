from utils import getWordFreq, check, getSplits
from wordLists import guesses, answers
from tqdm.auto import tqdm

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
        'splits': {}
    }

    print(f'{"  "*depth}Guess: {guess}, Remaining: {len(candidates)}')

    for response, split in getSplits(guess, candidates, useWords=True).items():
        res['splits'][response] = genStrategyTree(split, valuation, depth = depth + 1)

    return res