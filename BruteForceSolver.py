import json
from utils import getSplits
from originalWordLists import guesses, answers
from tqdm.auto import tqdm
from valuations import *

G = sorted(guesses + answers)
S = sorted(answers)

class Solver(object):
    def __init__(self, words):
        self.words = words
        self.memo = {}
        self.best = {}
    
    def encode(self, sub):
        t = 0
        for w in sub:
            t |= 1 << (len(self.words) - self.words.index(w) - 1)
        return t
    
    def solve(self):
        self.h(self.words)
        return self.memo[self.encode(self.words)]
        
    def h(self, sub, depth = 1):


        c = self.encode(sub)
        if c in self.memo: 
            return self.memo[c]

        # print(f"Depth = {depth}")
        
        ans = 1
        if len(sub) == 1:
            self.best[c] = sub[0]
            ans = 1
        elif len(sub) == 2:
            self.best[c] = sub[0]
            ans = 1.5
        elif depth >= 7:
            self.best[c] = sub[0]
            ans = 1000
            # print("Gone too far")
        else:
            bestScore = -1
            bestGuess = ""
            for g in tqdm(sorted(sub, key=lambda x: (mostParts(x, sub),1 - (x in sub)) )[:50], disable = not (depth < 3)):
                t = 1
                splits = getSplits(g, sub, useWords = True)
                if len(splits) == 1: continue
                for res, split in splits.items():
                    if res == '22222': continue
                    t += len(split)/len(sub) * (self.h(split, depth + 1))
#                     if first:
#                         print(split, t, self.h(split))
                
                if bestScore == -1 or t < bestScore:
                    bestScore = t
                    bestGuess = g
                    
#                 print(g,'final ',t, bestScore, getSplits(g, sub, useWords = True))
                
            ans = bestScore
            self.best[c] = bestGuess
        self.memo[c] = ans 
        return ans
    
    def genTree(self, sub = None):
        if sub is None:
            sub = self.words
#         print(self.memo[self.encode(sub)])
        guess = self.best[(self.encode(sub))]
        tree = {
            'guess': guess
        }
        if len(sub) != 1:
            tree['splits'] = {}
            splits = getSplits(guess, sub, useWords = True)
            for res, split in splits.items():
                if res == '22222': continue
                tree['splits'][res] = self.genTree(split)
        
        return tree
        

if __name__ == "__main__":
    s = Solver(words = S)
    # s = Solver(words = ['spasm', 'swami','soapy','swamp'])
    # s = Solver(words = ['boxer', 'homer', 'hover', 'joker', 'mover', 'roger', 'rover'])
    # bin(s.encode(s.words))
    s.solve()
    # pprint(s.genTree())
    tree = s.genTree()
    with open("originalBestTreeHardMode.json", "w") as f:
        json.dump(tree, f, sort_keys=True, indent=4)
    # print(json.dumps(tree, indent=4, sort_keys=True))
    print(s.memo[s.encode(s.words)])

    # print(json.dumps(s.memo, indent=4, sort_keys=True))