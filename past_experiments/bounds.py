from utils import getSplits
import math
from Config import Config
from tqdm.auto import tqdm
import json

c = Config('oldWordle')

# n nodes, r branches
def best_total(n, r):
    if n == 1: return 1
    if r == 1: return (n*(n+1)) // 2
    l = int(math.log(n*(r-1) + 1) / math.log(r))
    so_far = (r**l - 1) // (r-1)
    left = n - so_far
    return sum((r**i) * (i+1) for i in range(l)) + left *(l+1)

def bestSplits(C):
    if len(C) == 1: return 1
    return max(len(getSplits(g,C)) for g in c.guesses)

def rough_bound(g):
    t = len(c.answers)
    for res, split in getSplits(g, c.answers).items():
        if res == '22222':  continue 
        if split == 1: t += 1
        else: t += best_total(split, 150)
    return t

def tight_bound(g):
    t = len(c.answers)
    for res,split in tqdm(sorted(list(getSplits(g, c.answers, useWords=True).items())), desc=g, colour='yellow'):
        if res == '22222': continue
        if len(split) == 1: t += 1
        else: t += best_total(len(split), bestSplits(split)) 
    return t

if __name__ == '__main__':
    
    with open("lower_bounds.txt","r") as g:
        done = [line.strip().split()[0] for line in g]
    
    todo = [g for g in c.guesses if g not in done]

    for g in tqdm(todo):
        rough = rough_bound(g)
        tight = 99999
        if rough <= 7920:
            tight = tight_bound(g)
        print(g,'-->', rough, tight)
        # scores[g] = (rough, tight)
    
        with open("lower_bounds.txt", "a+") as f:
            f.write(f"{g} --> {rough} {tight}\n")
            # json.dump(scores, f, sort_keys=True, indent=4)