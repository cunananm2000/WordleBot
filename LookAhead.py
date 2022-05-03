from sys import maxsize
from wordLists import guesses, answers
from utils import *
from valuations import *
from tqdm.auto import tqdm

G = sorted(guesses + answers)
S = sorted(answers)

def v(g, C):
    return (maxSizeSplit(g, C), 1-(g in C))

def agg(a):
    return max([x[0] for x in a])


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
        
if __name__ == '__main__':
    C = S
    # C = filterPossible('reais', '01110', C)
    # C = filterPossible('aizle', '21012', C)
    # play = [ 
    #     # ('reais','00100'),
    #     # ('canty','02002'),
    #     # ('algid','10000'),
    #     # ('abamp','10001')
    # ]

    play = [
        ('aesir','00001'),
        ('choon','00110')
    ]

    for g,r in play:
        C = filterPossible(g, r, C)
        print(f"# Remaining: {len(C)}, e.g. {C[:10]}...")
    g = sigma(3, C)
    print(f"Best guess {g}")
# print(f"Overall best first guess is {overallBestGuess} -> {overallBestScore}")