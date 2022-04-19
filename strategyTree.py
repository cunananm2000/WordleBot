from utils import getWordFreq, check, getSplits, filterPossible
from wordLists import guesses, answers, commonWords
from tqdm.auto import tqdm
from valuations import *
import json


def getBestGuess(candidates, validGuesses, valuation, depth, searchDepth=0, hardMode = False):

    # nextGuesses = validGuesses
    # if hardMode:
    #     nextGuesses = filterPossible()
    
    scores = [
        (valuation(g, candidates), -getWordFreq(g), g)
        for g in tqdm(
            validGuesses, desc=f'{"  "*depth}Depth: {depth}', disable=(searchDepth != 0)
        )
    ]
    scores.sort()

    if searchDepth == 0:
        score, _, guess = scores[0]
        return score, guess

    topGuesses = [guess for _, _, guess in scores][:5]
    data = []
    for g in tqdm(topGuesses, desc=f"Going deeper, searchDepth = {searchDepth}"):
        scores = []
        for _, split in getSplits(g, candidates, useWords=True).items():
            score, _ = getBestGuess(
                split, validGuesses, valuation, depth, searchDepth - 1
            )
            scores.append(score)
        data.append((max(scores), -getWordFreq(g), g))

    data.sort()
    score, _, guess = data[0]

    return score, guess


def genStrategyTree(candidates, validGuesses, valuation, depth=0, searchDepth=0, hardMode = False):
    if len(candidates) == 1:
        print(f'{"  "*depth}Leaf: {candidates[0]}, depth = {depth}')
        return {"guess": candidates[0]}

    _, guess = getBestGuess(
        candidates, validGuesses, valuation, depth, searchDepth=searchDepth, hardMode=hardMode
    )

    res = {"guess": guess, "nRemaining": len(candidates), "splits": {}}

    print(f'{"  "*depth}Guess: {guess}, Remaining: {len(candidates)}')


    for response, split in getSplits(guess, candidates, useWords=True).items():
        if response == "22222":
            continue

        nextGuesses = validGuesses
        if hardMode:
            nextGuesses = filterPossible(guess, response, validGuesses)

        res["splits"][response] = genStrategyTree(
            split, nextGuesses, valuation, depth=depth + 1, searchDepth=searchDepth, hardMode=hardMode
        )

    return res


# def writeStrategyTree(v, common, searchDepth=0, hardMode = False):
#     if common:
#         tree = genStrategyTree(
#             commonWords, guesses + answers, v, searchDepth=searchDepth, hardMode=hardMode
#         )
#     else:
#         tree = genStrategyTree(
#             guesses + answers, guesses + answers, v, searchDepth=searchDepth, hardMode=hardMode
#         )

#     tree['name'] = v.__name__

#     with open(
#         f"{'commonTrees' if common else 'trees'}/{v.__name__}{searchDepth + 1}{'hard' if hardMode else ''}.json",
#         "w",
#     ) as f:
#         json.dump(tree, f, sort_keys=True, indent=4)

def writeStrategyTree(v, candidates, validGuesses, searchDepth=0, hardMode=False):
    tree = genStrategyTree(
        candidates, validGuesses, v, searchDepth=searchDepth, hardMode=hardMode
    )

    tree['name'] = v.__name__

    with open(
        f"cheatTrees/{v.__name__}{searchDepth + 1}{'hard' if hardMode else ''}.json",
        "w",
    ) as f:
        json.dump(tree, f, sort_keys=True, indent=4)


if __name__ == "__main__":
    # writeStrategyTree(v=maxSize, common=True, searchDepth=0, hardMode=True)
    writeStrategyTree(v=maxSizeSplit, candidates = answers, validGuesses = answers + guesses)
