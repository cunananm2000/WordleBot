from BaseOptimizer import BaseOptimizer
from utils import filterPossible, getSplits, softFilterPossible, sortWords, usefulGuesses
from tqdm.auto import tqdm
from valuations import *



class AverageOptimizer(BaseOptimizer):
    def __init__(
        self, 
        *args,
        **kwargs,
    ):
        super(AverageOptimizer, self).__init__(*args, **kwargs)
        if self.fname is None:
            self.fname = f"{self.game}_{self.MAX_BREADTH}{'_hard' if self.hardMode else ''}"

    def explore(self, possibleGuesses, possibleAnswers, depth = 1):
        self.CALLS += 1
        # print(len(possibleGuesses), len(possibleAnswers))
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
            #     options = ['tarse']
            # else:

            # print('here again',len(possibleAnswers))

            options = usefulGuesses(possibleGuesses, possibleAnswers)
            options = sortWords(
                G = options,
                S = possibleAnswers,
                vals = self.vals,
                n = self.MAX_BREADTH,
                showProg = (depth <= self.DEBUG_LEVEL),
            )

            # print(options)
            # options.sort(key=lambda g: inSet(g, possibleAnswers))

            # print('also here', len(possibleAnswers))


            for g in tqdm(options, disable = not(depth <= self.DEBUG_LEVEL), colour = ['green','blue'][depth%2], desc=f"Depth {depth}"):
                splits = getSplits(g, possibleAnswers, useWords=True)
                if len(splits) == 1: continue 
                # if (depth == 1): print(splits)
                t = 1
                for res, split in tqdm(splits.items(), disable = not(depth <= self.DEBUG_LEVEL), colour='yellow', desc=g):
                    if res == self.rStar: continue 
                    # if (depth <= 2):
                    #     print('    '*(depth-1),g,'-->',res)
                    t += len(split)/len(possibleAnswers) * self.explore(
                        possibleAnswers = split, 
                        possibleGuesses = self.guessFilter(g, res, possibleGuesses),
                        depth = depth + 1,
                    )

                # if (depth <= 1):
                #     print('    '*(depth-1),g,'-->',t)
                
                if self.bestScore.get(code, 9999999) > t:
                    self.bestScore[code] = t
                    self.bestGuess[code] = g

                # This only works because after choosing the top N, we make sure the InSet ones take priority
                # n = len(possibleAnswers)
                # if g in possibleAnswers and abs(t - (1 + 2*(n-1))/n) < 0.00001:
                #     break
                # elif abs(t - 2) < 0.00001:
                #     break

        
        # if code not in self.bestScore:
        #     print(possibleAnswers, possibleGuesses)
        #     assert(False)

        return self.bestScore[code]


if __name__ == "__main__":

    for b in [1, 5, 10]:
        for game_name in [
            # "oldWordle",
            # "mininerdle",
            # "ffxivrdle",
            "bardle",
            # "primel",
            # "nerdle",
        ]:

            s = AverageOptimizer(
                hardMode = False,
                MAX_BREADTH = b,
                game = game_name,
                DEBUG_LEVEL = 0,
                fname = None, #'oldWordle_50',
                MAX_DEPTH = 7,
            )

            s.writeJson()
            s.showStats()
            s.writeWordList()