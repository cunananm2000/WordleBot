from utils import getSplits, sortWords
from tqdm.auto import tqdm
from BaseOptimizer import BaseOptimizer

class WorstOptimizer(BaseOptimizer):
    def __init__(
        self, 
        *args,
        **kwargs,
    ):
        super(WorstOptimizer, self).__init__(*args, **kwargs)
        self.fname = f"{self.game}_worst_{self.MAX_BREADTH}{'_hard' if self.hardMode else ''}"

    def explore(self, possibleGuesses, possibleAnswers, depth = 1):
        self.CALLS += 1
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
            self.bestScore[code] = (1,1)
        elif len(possibleAnswers) == 2:
            self.bestGuess[code] = possibleAnswers[0]
            self.bestScore[code] = (2,1)
        elif depth >= self.MAX_DEPTH:
            self.bestGuess[code] = possibleAnswers[0]
            self.bestScore[code] = (2*self.MAX_DEPTH, 1)
            self.BREACHES += 1
        else:
            

            # Shortcut since this always the best choice
            # if (depth == 1): 
            #     options = ['salet']
            # else:

                # print('here again',len(possibleAnswers))

            options = sortWords(
                G = possibleGuesses,
                S = possibleAnswers,
                vals = self.vals,
                n = self.MAX_BREADTH,
                showProg = (depth <= self.DEBUG_LEVEL),
            )

            # print(options)

            # print('also here', len(possibleAnswers))


            for g in tqdm(options, disable = not(depth <= self.DEBUG_LEVEL), colour = ['green','blue'][depth%2]):
                splits = getSplits(g, possibleAnswers, useWords=True)
                if len(splits) == 1: continue 
                # if (depth == 1): print(splits)
                t = [1,1]
                for res, split in tqdm(splits.items(), disable = not(depth <= self.DEBUG_LEVEL), colour='yellow'):
                    if res == self.rStar: continue 
                    # if (depth <= 2):
                    #     print('    '*(depth-1),g,'-->',res)
                    d,n = self.explore(
                        possibleAnswers = split, 
                        possibleGuesses = self.guessFilter(g, res, possibleGuesses),
                        depth = depth + 1,
                    )
                    d += 1
                    if d > t[0]: t = [d,0]
                    if d == t[0]: t[1] += n

                t = tuple(t)

                # if (depth <= 3):
                #     print('    '*(depth-1),g,'-->',t)
                
                if self.bestScore.get(code, (9999999,1)) > t:
                    self.bestScore[code] = t
                    self.bestGuess[code] = g

        
        # if code not in self.bestScore:
        #     print(possibleAnswers, possibleGuesses)
        #     assert(False)

        return self.bestScore[code]

if __name__ == "__main__":
    breadths = [30]
    for b in breadths:
        s = WorstOptimizer(
            hardMode = False,
            MAX_BREADTH = b,
            game = 'oldWordle',
            DEBUG_LEVEL = 1
        )

        s.writeJson()
        s.writeWordList()
        s.showStats()