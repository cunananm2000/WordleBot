from BaseOptimizer import BaseOptimizer
from utils import getSplits, sortWords
from tqdm.auto import tqdm



class AverageOptimizer(BaseOptimizer):
    def __init__(
        self, 
        *args,
        **kwargs,
    ):
        super(AverageOptimizer, self).__init__(*args, **kwargs)
        self.fname = f"{self.game}_{self.MAX_BREADTH}{'_hard' if self.hardMode else ''}"

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
            if (depth == 1): 
                options = ['salet']
            else:

            # print('here again',len(possibleAnswers))

                options = sortWords(
                    C = possibleGuesses,
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
                t = 1
                for res, split in tqdm(splits.items(), disable = not(depth <= self.DEBUG_LEVEL), colour='yellow'):
                    if res == self.rStar: continue 
                    # if (depth <= 2):
                    #     print('    '*(depth-1),g,'-->',res)
                    t += len(split)/len(possibleAnswers) * self.explore(
                        possibleAnswers = split, 
                        possibleGuesses = self.guessFilter(g, res, possibleGuesses),
                        depth = depth + 1,
                    )

                # if (depth <= 3):
                #     print('    '*(depth-1),g,'-->',t)
                
                if self.bestScore.get(code, 9999999) > t:
                    self.bestScore[code] = t
                    self.bestGuess[code] = g

                n = len(possibleAnswers)
                if g in possibleAnswers:
                    if abs(t - (1 + 2*(n-1))/n) < 0.001:
                        # print("Exit early! Reason 1")
                        break
                else:
                    if abs(t - 2) < 0.001:
                        # print("Exit early! Reason 2")
                        break

        
        # if code not in self.bestScore:
        #     print(possibleAnswers, possibleGuesses)
        #     assert(False)

        return self.bestScore[code]


if __name__ == "__main__":
    s = AverageOptimizer(
        hardMode = True,
        MAX_BREADTH = 30,
        game = 'oldWordle',
        DEBUG_LEVEL = 1
    )

    s.writeJson()
    s.showStats()
    s.writeWordList()