from ctypes.wintypes import tagMSG
from fileinput import filename
from Config import Config
from utils import filterSimul, getSimulSplits, check, countWithNonrepeats
from tqdm.auto import tqdm
from random import sample
import numpy as np
from valuations import multiVal

n = 2
game = Config('oldWordle')

def getNextGuess(D, turn):
    assert len(D) != 0
    # print("Lengths:", list(len(cands) for cands in D))
    goodIdxs = [idx for idx,cands in enumerate(D) if len(cands) == 1]
    if len(goodIdxs) != 0:
        return D[goodIdxs[0]][0]

    if len(D) == 1 and len(D[0]) == 2:
        return D[0][0]

    if turn == 0:
        return 'trace'

    
    return min(game.guesses, key=lambda g: multiVal(g, D[0]))
    

def play_in_order(secrets):

    filename = f"meta_results_inorder_{n}.txt"

    with open(filename, 'r') as f:
        for line in f:
            if '.'.join(secrets) in line:
                return
                
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
        g = getNextGuess(D, turn)
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

    
    with open(filename,"a+") as f:
        f.write(f"{'.'.join(secrets)} -> {turn+1} = {'.'.join(guesses)}\n")

def play_with_swap(secrets, method):
    filename = f"meta_results_{method}_with_swap_{n}.txt"

    with open(filename, 'r') as f:
        for line in f:
            if '.'.join(secrets) in line:
                return

    ss = secrets.copy()

    D = [game.answers for _ in range(n)]
    guesses = []
    target = -1
    for turn in range(20):

        g = None
        goodIdxs = [idx for idx,cands in enumerate(D) if len(cands) == 1]
        if len(goodIdxs) != 0:
            g= D[goodIdxs[0]][0]

        if len(D) == 1 and len(D[0]) == 2:
            g= D[0][0]

        if g is None:
            if turn == 0:
                g = 'trace'
            else:
                assert target != -1
                g = min(game.guesses, key=lambda x: multiVal(x, D[target]))

        guesses.append(g)

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

        if method =='min':
            target = min((len(C), idx) for idx, C in enumerate(D))[-1]
        elif method == 'max':
            target = max((len(C), idx) for idx, C in enumerate(D))[-1]
        else:
            assert False

    with open(filename,"a+") as f:
        f.write(f"{'.'.join(secrets)} -> {turn+1} = {'.'.join(guesses)}\n")


def play_no_swap(secrets, method):
    filename =f"meta_results_{method}_no_swap_{n}.txt"

    with open(filename, 'r') as f:
        for line in f:
            if '.'.join(secrets) in line:
                return

    ss = secrets.copy()

    D = [game.answers for _ in range(n)]
    guesses = []
    target = -1
    for turn in range(20):

        g = None
        goodIdxs = [idx for idx,cands in enumerate(D) if len(cands) == 1]
        if len(goodIdxs) != 0:
            g= D[goodIdxs[0]][0]

        if len(D) == 1 and len(D[0]) == 2:
            g= D[0][0]

        if g is None:
            if turn == 0:
                g = 'trace'
            else:
                assert target != -1
                # print(target, D)
                g = min(game.guesses, key=lambda x: multiVal(x, D[target]))

        guesses.append(g)

        rs = [check(g, s) for s in ss]



        assert len(rs) == len(D) and all(len(r) == len(game.rStar) for r in rs)
        if game.rStar in rs:
            idx = rs.index(game.rStar)
            D.pop(idx)
            rs.pop(idx)
            ss.pop(idx)
            if idx == target:
                target = -1
            elif idx < target:
                target -= 1
            if len(D) == 0: 
                # print(turn +1)
                break
        D = filterSimul(g, rs, D)

        if target == -1:
            if method =='min':
                target = min((len(C), idx) for idx, C in enumerate(D))[-1]
            elif method == 'max':
                target = max((len(C), idx) for idx, C in enumerate(D))[-1]
            else:
                assert False

    with open(filename,"a+") as f:
        f.write(f"{'.'.join(secrets)} -> {turn+1} = {'.'.join(guesses)}\n")
        
if __name__ == '__main__':

    with open(f"simulTests_{n}.txt","r") as f:
        for line in tqdm(f, total=10000, colour='blue', desc='in order'):
            line = line.strip()
            answers = line.split('.')


            play_in_order(answers)

    with open(f"simulTests_{n}.txt","r") as f:
        for line in tqdm(f, total=10000, colour='blue', desc='with, min'):
            line = line.strip()
            answers = line.split('.')


            play_with_swap(answers, method='min')

    with open(f"simulTests_{n}.txt","r") as f:
        for line in tqdm(f, total=10000, colour='blue', desc='with, max'):
            line = line.strip()
            answers = line.split('.')


            play_with_swap(answers, method='max')

    with open(f"simulTests_{n}.txt","r") as f:
        for line in tqdm(f, total=10000, colour='blue', desc='no, min'):
            line = line.strip()
            answers = line.split('.')


            play_no_swap(answers, method='min')

    with open(f"simulTests_{n}.txt","r") as f:
        for line in tqdm(f, total=10000, colour='blue', desc='no, max'):
            line = line.strip()
            answers = line.split('.')


            play_no_swap(answers, method='max')