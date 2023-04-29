from Config import Config
from utils import filterSimul, getSimulSplits, check, countWithNonrepeats
from tqdm.auto import tqdm
from random import sample
import numpy as np

n = 2
game = Config('oldWordle')


    

def firstValid(D, turn):
    return min(C[0] for C in D)

def mostParts(D, turn):
    if turn == 0:
        return 'trace'

    scores = ((len(getSimulSplits(g, D, useWords=True)),g) for g in tqdm(game.guesses))
    # scores.sort(reverse=True)
    return max(scores)[1]

def maxSizeSplit(D, turn):
    if turn == 0:
        return 'aesir'

    scores = ((max(getSimulSplits(g, D).values()),g) for g in tqdm(game.guesses))
    # scores.sort()
    return min(scores)[1]


def expSizeSplit(D, turn):
    if turn == 0:
        return 'roate'

    scores = ((sum(t* t for t in getSimulSplits(g, D).values()),g) for g in tqdm(game.guesses))
    # scores.sort()
    return min(scores)[1] 

def information(D, turn):
    if turn == 0:
        return 'soare'


    # for g in tqdm(game.guesses):
    #     values = list(getSimulSplits(g, D).values())
    #     print(values)
    #     score = (sum(t*np.log(t) for t in values),g)
    #     print(score)
    #     scores.append(score)
    #     assert False

    scores = ((sum(t* np.log(t) for t in getSimulSplits(g, D).values()),g) for g in tqdm(game.guesses))
    # scores.sort()
    # print(scores[:20])
    return min(scores)[1] 

def getNextGuess(D, turn, func):
    assert len(D) != 0
    # print("Lengths:", list(len(cands) for cands in D))
    goodIdxs = [idx for idx,cands in enumerate(D) if len(cands) == 1]
    if len(goodIdxs) != 0:
        return D[goodIdxs[0]][0]

    if len(D) == 1 and len(D[0]) == 2:
        return D[0][0]
    
    return func(D, turn)


def play(secrets, fn):
    # secrets = sample(game.answers, n)
    ss = secrets.copy()

    D = [game.answers for _ in range(n)]

    guesses = []

    for turn in range(20):
        # print('------ Turn',turn+1,'------')
        # if turn == 0:
        #     # print("Lengths:", list(len(cands) for cands in D))
        #     g = 'salet'
        # else:
        g = getNextGuess(D, turn, fn)
        # print("Guessing",g)
        guesses.append(g)


        # rs = input('Responses: ').split(' ')
        rs = [check(g, s) for s in ss]



        assert len(rs) == len(D) and all(len(r) == len(game.rStar) for r in rs)
        if game.rStar in rs:
            idx = rs.index(game.rStar)
            D.pop(idx)
            rs.pop(idx)
            ss.pop(idx)
            if len(D) == 0: 
                # print(turn +1)
                break
        D = filterSimul(g, rs, D)

    # print(f"{'.'.join(secrets)} -> {turn+1} = {'.'.join(guesses)}")

    filename = f"simulSamples_{fn.__name__}_{n}_2.txt" 
    
    with open(filename,"a+") as f:
        f.write(f"{'.'.join(secrets)} -> {turn+1} = {'.'.join(guesses)}\n")
        
if __name__ == '__main__':



    for val in [
        # firstValid, 
        # mostParts, 
        # expSizeSplit, 
        # maxSizeSplit, 
        information,
    ]:

    # play(sample(game.answers, n), val)
    # assert False

    # print(val([game.answers for _ in range(n)],0))
    # assert False
        done = []
        # with open(f"simulSamples_{val.__name__}_{n}.txt","r") as f:
        #     done = [line.split(' ')[0] for line in f]


        with open(f"simulTests_{n}.txt","r") as f:
            todo = [line.strip() for line in f]

        todo = [x for x in todo if x not in done]

        for line in tqdm(todo, colour='blue'):

            answers = line.split('.')


            play(answers, val)

    #     # i = 0
    #     for line in tqdm(f, total=10000):
    #         a = line.split(' ')[0]
    #         answers = a.split('.')
            
            # print(answers)
            # i += 1
            # if i > 20: break
        

# rs = ['20001','00002']
# D = list(filterPossible(g, r, cands) for r,cands in zip(rs, D))

# g = 'courd'
# rs = ['11000','02101']
# D = list(filterPossible(g, r, cands) for r,cands in zip(rs, D))

# g = 'donut'
# rs = ['01001','22222']
# D = list(filterPossible(g, r, cands) for r,cands in zip(rs, D))

