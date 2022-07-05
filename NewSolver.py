import json
from utils import filterPossible, getSplits, saveAsWordList, sortWords, filterMultiple, softFilterPossible, softFilterMultiple
from originalWordLists import guesses, answers
from tqdm.auto import tqdm
from valuations import *

MAX_DEPTH = 10
BREACHES = 0
HITS = 0

class Solver(object):
    def __init__(self, possibleGuesses, possibleAnswers):
        self.G = possibleGuesses
        self.S = possibleAnswers
        
        self.bestGuess = {}
        self.bestScore = {}

    def encode(self, subset, superset):
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
            global HITS
            HITS += 1
            return self.bestScore[code]

        # isSet = 0
        # Special cases first 
        if len(possibleAnswers) == 1:
            self.bestGuess[code] = possibleAnswers[0]
            self.bestScore[code] = 1
            # isSet = 1
        elif len(possibleAnswers) == 2:
            self.bestGuess[code] = possibleAnswers[0]
            self.bestScore[code] = 1.5
            # isSet = 2
        elif depth >= MAX_DEPTH:
            # print("Went too far")
            self.bestGuess[code] = possibleAnswers[0]
            self.bestScore[code] = 1000000
            # isSet = 3
            global BREACHES
            BREACHES += 1
        else:
            if (depth == 1): 
                options = ['salet']
            else:
                options = sortWords(
                    C = possibleGuesses,
                    S = possibleAnswers,
                    vals = [mostParts, firstValid, maxSizeSplit],
                    n = 20
                )

            # if (depth <= 2): 
            #     print('   '*(depth-1), options)

            for g in tqdm(options, disable = not(depth <= 2)):
                splits = getSplits(g, possibleAnswers, useWords=True)
                if len(splits) == 1: continue 
                
                t = 1
                for res, split in splits.items():
                    if res == '22222': continue 
                    # if (depth <= 2):
                    #     print('    '*(depth-1),g,'-->',res)
                    t += len(split)/len(possibleAnswers) * self.explore(
                        possibleAnswers = split, 
                        possibleGuesses = softFilterPossible(g, res, possibleGuesses),
                        depth = depth + 1,
                    )

                # if (depth <= 2):
                #     print('    '*(depth-1),g,'-->',t)
                
                if self.bestScore.get(code, 9999999) > t:
                    self.bestScore[code] = t
                    self.bestGuess[code] = g
                    # isSet = 4

                

            # assert(isSet != 0)
        
        if code not in self.bestScore:
            print(possibleAnswers, possibleGuesses)
            assert(False)


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
        avg = self.bestScore[code]
    
        # if guess == 'howff':
        #     print('OI HOW', possibleGuesses)


        tree = {'guess': guess, 'avg': avg}
        if len(possibleAnswers) != 1:
            tree['splits'] = {}
            splits = getSplits(guess, possibleAnswers, useWords=True)
            for res, split in splits.items():
                if res == '22222': continue 
                tree['splits'][res] = self.genTree(
                    possibleGuesses=softFilterPossible(guess, res, possibleGuesses),
                    possibleAnswers=split,
                    depth = depth + 1
                )
        
        return tree


if __name__ == "__main__":
    G = sorted(guesses + answers)
    S = sorted(answers)

    # # Temporrary
    # history = [('salet','00000')]
    # G = softFilterMultiple(
    #     history = history,
    #     candidates = G
    # )

    # S = filterMultiple(
    #     history = history,
    #     candidates = S
    # )

    print(len(G), len(S))
    # print(G, S)


    s = Solver(
        possibleGuesses=G,
        possibleAnswers=S
    )

    tree = s.genTree(
        possibleGuesses=G,
        possibleAnswers=S
    )

    with open("originalBestTree.json", "w") as f:
        json.dump(tree, f, sort_keys=True, indent=4)

    saveAsWordList(
        tree = tree,
        fname = "originalBestTree.txt",
        answers = S
    )
    
    print(s.bestScore[(s.encode(s.S,s.S), s.encode(s.G,s.G))])
    print("HITS:", HITS)
    print("BREACHES:", BREACHES)