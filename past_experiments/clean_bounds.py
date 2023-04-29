from pprint import pprint
from utils import filterPossible, getSplits, usefulGuesses
import math 
from Config import Config 
from tqdm.auto import tqdm 
import json
import pandas as pd
from os.path import exists
from random import shuffle

game = Config('newerWordle')

def bound(n, r):
    if n == 0: return 0
    if n == 1: return 1
    if r == 1: return (n*(n+1))//2
    l = int(math.log(n*(r-1) + 1) / math.log(r))
    so_far = (r**l - 1) // (r - 1)
    left = n - so_far 
    return sum((r**i) * (i+1) for i in range(l)) + left*(l+1)

def bestSplits(C):
    return max(len(getSplits(g, C)) for g in game.guesses)

def LB1(C):
    if len(C) == 1: return 1
    if len(C) == 2: return 3
    return bound(len(C), game.maxsplits)

def LB2(C):
    if len(C) == 1: return 1
    if len(C) == 2: return 3
    return bound(len(C), bestSplits(C))

def V1(g, C, show=False):
    t = len(C)
    for res, split in tqdm(getSplits(g, C, useWords=True).items(), disable=not show, desc=g):
        if res == game.rStar: continue
        t += LB1(split)
    return t

def V2(g, C, show=False, upper_bound = game.upper_bound):
    t = len(C)
    splits = list(getSplits(g, C, useWords=True).items())
    splits.sort(key = lambda x: -len(x[1]))
    for res, split in tqdm(splits, disable=not show, desc=g):
        if res == game.rStar: continue

        add = LB1(split)
        t += add
        if t > upper_bound:
            break
        t -= add

        t += LB2(split)
        if t > upper_bound:
            break
    return t

def V1to2(g, C, show=False, upper_bound = 99999):
    df = pd.DataFrame(columns = ['res','bound'])
    for res,split in tqdm(getSplits(g, C, useWords=True).items(), disable= not show, desc=f'{g}: Initial'):
        if res == game.rStar: continue
        df = df.append({
            'res': res,
            'bound': LB1(split)
        }, ignore_index = True)
    
    df = df.set_index('res', drop = True).sort_values(by='bound', ascending=True)
    # This is V3
    t = df['bound'].sum() + len(C)
    # if show: print(f"New total bound = {t}")
    if t > upper_bound:
        return t

    for res in tqdm(list(df.index), disable= not show, desc=f'{g}: Updating'):
        new_bound = LB2(filterPossible(g, res, C))
        # if show:
        #     print(f"{df.loc[res,'bound'] } -> {new_bound}")
        df.loc[res,'bound'] = new_bound
        t = df['bound'].sum() + len(C)
        # if show: print(f"{g}: New total bound = {t}")
        if t > upper_bound:
            return t

    return t


def LB3(C, show=False):
    if len(C) == 1: return 1
    if len(C) == 2: return 3
    return min(V1(g, C) for g in tqdm(usefulGuesses(game.guesses, C), disable = not show))

def LB4(C, show=False):
    if len(C) == 1: return 1
    if len(C) == 2: return 3
    return min(V2(g, C) for g in tqdm(game.guesses, disable = not show))

def LB3to4(C, show=False, req_diff = 99999):
    if len(C) == 1: return 1
    if len(C) == 2: return 3
    df = pd.DataFrame(columns=['guess','v','recomputed'])

    ugc = usefulGuesses(game.guesses, C)

    for g in tqdm(ugc, disable = not show, desc='Initial V1'):
        df = df.append({
            'guess': g,
            'v': V1(g, C),
            'recomputed': False
        }, ignore_index = True)
    
    df = df.sort_values(by=["v","recomputed","guess"], ascending=[True, True, True]).set_index("guess")

    old = df.iloc[0]['v']

    for _ in tqdm(ugc, disable= not show, desc='Updating'):
        g = df.index[0]
        if df.loc[g,'recomputed']: break
            
        v = V2(g, C)
        df.loc[g, 'v'] = v
        df.loc[g, 'recomputed'] = True
        df = df.sort_values(by=['v','recomputed','guess'], ascending=[True, True, True])

        if show: print(df.head(1))

        if df.iloc[0]['v'] - old > req_diff:
            if show: print("Skipped updating everything")
            return df.iloc[0]['v']

    if show:
        print(f"{old} -> {df.iloc[0]['v']}")

    return df.iloc[0]['v']

def V3(g, C, show=False, upper_bound = 99999):
    t = len(C)
    for res, split in tqdm(getSplits(g, C, useWords=True).items(), disable=not show, desc=g):
        if res == game.rStar: continue
        t += LB3(split)
    return t

def V1to3(g, C, show=False, upper_bound = 99999):
    t = len(C)
    for res, split in tqdm(getSplits(g, C, useWords=True).items(), disable=not show, desc=g):
        if res == game.rStar: continue
        add = LB1(split)
        t += add
        if t > upper_bound:
            return t
        t -= add
        
        t += LB3(split)
        if t > upper_bound:
            return t
    return t

def V3to4(g, C, show=False, upper_bound = 99999):
    df = pd.DataFrame(columns = ['res','bound'])
    for res,split in tqdm(getSplits(g, C, useWords=True).items(), disable= not show, desc=f'{g}: Initial'):
        if res == game.rStar: continue
        df = df.append({
            'res': res,
            'bound': LB3(split)
        }, ignore_index = True)
    
    df = df.set_index('res', drop = True).sort_values(by='bound', ascending=False)
    t = df['bound'].sum() + len(C)
    if show: print(f"New total bound = {t}")
    if t > upper_bound:
        return 99999

    for res in tqdm(list(df.index), disable=not show,  desc=f'{g}: Updating'):
        new_bound = LB3to4(filterPossible(g, res, C), req_diff=upper_bound - t)
        if show:
            print(f"{df.loc[res,'bound'] } -> {new_bound}")
        df.loc[res,'bound'] = new_bound
        t = df['bound'].sum() + len(C)
        if show: print(f"New total bound = {t}")
        if t > upper_bound:
            return t

    # for res, split in tqdm(getSplits(g, C, useWords=True).items(), disable=not show, desc=g):
    #     if res == game.rStar: continue
    #     t += LB3to4(split, show=True)
    # return t

    return df['bound'].sum() + len(C)


def V4(g, C, show=False):
    t = len(C)
    for res, split in tqdm(getSplits(g, C, useWords=True).items(), disable=not show, desc=g):
        if res == game.rStar: continue
        t += LB4(split)
    return t

def LB3to5(C, show=False, req_diff = 99999):
    if len(C) == 1: return 1
    if len(C) == 2: return 3
    df = pd.DataFrame(columns=['guess','v','recomputed'])

    ugc = usefulGuesses(game.guesses, C)

    for g in tqdm(ugc, disable = not show, desc='Initial V1'):
        if len(getSplits(g, C)) == 1: continue
        df = df.append({
            'guess': g,
            'v': V1(g, C),
            'recomputed': False
        }, ignore_index = True)
    
    df = df.sort_values(by=["v","recomputed","guess"], ascending=[True, True, True]).set_index("guess")

    # This value is LB3
    old = df.iloc[0]['v']

    for _ in tqdm(ugc, disable= not show, desc='Updating LB3->5'):
        g = df.index[0]
        if df.loc[g,'recomputed']: break
            
        v = V3(g, C)
        df.loc[g, 'v'] = v
        df.loc[g, 'recomputed'] = True
        df = df.sort_values(by=['v','recomputed','guess'], ascending=[True, True, True])

        if show: print(df.head(1))

        if df.iloc[0]['v'] - old > req_diff:
            if show: print("Skipped updating everything")
            return df.iloc[0]['v']

    if show:
        print(f"{old} -> {df.iloc[0]['v']}")

    return df.iloc[0]['v']

def V3to5(g, C, show=False, upper_bound = 99999):
    df = pd.DataFrame(columns = ['res','bound'])
    for res,split in tqdm(getSplits(g, C, useWords=True).items(), disable= not show, desc=f'{g}: Initial'):
        if res == game.rStar: continue
        df = df.append({
            'res': res,
            'bound': LB3(split)
        }, ignore_index = True)
    
    df = df.set_index('res', drop = True).sort_values(by='bound', ascending=False)
    # This is V3
    t = df['bound'].sum() + len(C)
    if show: print(f"New total bound = {t}")
    if t > upper_bound:
        return t

    for res in tqdm(list(df.index), disable= not show, desc=f'{g}: Updating'):
        new_bound = LB3to5(filterPossible(g, res, C), req_diff=upper_bound - t, show=True)
        if show:
            print(f"{df.loc[res,'bound'] } -> {new_bound}")
        df.loc[res,'bound'] = new_bound
        t = df['bound'].sum() + len(C)
        if show: print(f"New total bound = {t}")
        if t > upper_bound:
            return t

    return t

def LB6(C, show = False):
    if len(C) == 1: return 1
    if len(C) == 2: return 3
    return min(V4(g, C) for g in tqdm(game.guesses, disable = not show))


def V6(g, C, show=False):
    t = len(C)
    for res, split in tqdm(getSplits(g, C, useWords=True).items(), disable=not show, desc=g):
        if res == game.rStar: continue
        t += LB6(split)
    return t

def LB5to6(C, show = False, req_diff = 99999):
    if len(C) == 1: return 1
    if len(C) == 2: return 3
    df = pd.DataFrame(columns=['guess','v','recomputed'])
    for g in tqdm(game.guesses, disable = not show, desc='Initial V3'):
        df = df.append({
            'guess': g,
            'v': V3(g, C),
            'recomputed': False
        }, ignore_index = True)
    
    df = df.sort_values(by=["v","recomputed","guess"], ascending=[True, True, True]).set_index("guess")

    # This value is LB5
    old = df.iloc[0]['v']

    for _ in tqdm(game.guesses, disable= not show, desc='Updating LB5->6'):
        g = df.index[0]
        if df.loc[g,'recomputed']: break
            
        v = V4(g, C)
        df.loc[g, 'v'] = v
        df.loc[g, 'recomputed'] = True
        df = df.sort_values(by=['v','recomputed','guess'], ascending=[True, True, True])

        if show: print(df.head(1))

        if df.iloc[0]['v'] - old > req_diff:
            if show: print("Skipped updating everything")
            return df.iloc[0]['v']

    if show:
        print(f"{old} -> {df.iloc[0]['v']}")

    return df.iloc[0]['v']

def V5to6(g, C, show=False, upper_bound = 99999):
    # if len(C) == 1 and g in C:
    #     return 1
    # if len(C) == 1 and g not in C:
    #     return 2
    # if len(C) == 2 and g in C:
    #     return 3
    # if len(C) == 2 and g not in C:
    #     return 4

    df = pd.DataFrame(columns = ['res','bound'])
    for res,split in tqdm(getSplits(g, C, useWords=True).items(), disable= not show, desc=f'{g}: Initial'):
        if res == game.rStar: continue
        df = df.append({
            'res': res,
            'bound': LB3to5(split)
        }, ignore_index = True)
    
    df = df.set_index('res', drop = True).sort_values(by='bound', ascending=False)
    # This is V5
    t = df['bound'].sum() + len(C)
    if show: print(f"New total bound = {t}")
    if t > upper_bound:
        return t

    for res in tqdm(list(df.index), disable= not show,  desc=f'{g}: Updating'):
        new_bound = LB5to6(filterPossible(g, res, C), req_diff=upper_bound - t)
        if show:
            print(f"{df.loc[res,'bound'] } -> {new_bound}")
        df.loc[res,'bound'] = new_bound
        t = df['bound'].sum() + len(C)
        if show: print(f"New total bound = {t}")
        if t > upper_bound:
            return t

    return t


if __name__ == "__main__":
    # print(V1('farle', game.answers))
    # print(V2('farle', game.answers))
    # print(V3('salet', game.answers, show=True))
    # print(V4('farle', game.answers, show=True))

    # print(LB1(game.answers))
    # print(LB2(game.answers))
    # print(LB3(game.answers, show=True))
    # print(LB3to4(game.answers, show=True))
    # print(LB3to5(game.answers, show=True))
    # print('lb3',LB3(game.answers, show=True))
    # print('v3',V3('4*7=28', game.answers, show=True))
    # print('v4',V4('4*7=28', game.answers, show=True))
    # print('v3to4',V3to4('4*7=28', game.answers, show=True))
    # print('v3to5',V3to5('4*7=28', game.answers, show=True))

    # with open("v3to4_vals.txt","r") as f:
    #     todo = [(a,c) for a,b,c in map(lambda x: x.strip().split(), f) if int(c) <= 7920]
    # todo.sort(key= lambda x: -int(x[1]))
    # todo = [a for a,c in todo]

    with open('newerWordleResults/V4.txt', 'r') as f:
        lines = [line.strip() for line in f]
        todo = [line.split(' ') for line in lines]
        todo = [(a,int(c)) for a,b,c in todo]
        todo.sort(key = lambda x: -x[1])
        todo = [a for a,c in todo if int(c) <= 7883]
    
    # with open('newerWordleResults/V4.txt', 'r') as f:
    #     lines = [line.strip() for line in f]
    #     done = [line.split(' ')[0] for line in lines]
    # todo = [g for g in todo if g not in done]


    # shuffle(todo)
    
    total = 0
    passed = 0
    for g in tqdm(todo):
        with open('newerWordleResults/V5.txt', 'a+') as f:
            score = V3to5(g, game.answers, show=True, upper_bound=game.upper_bound)
            f.write(f"{g} --> {score}\n")
            passed += score <= game.upper_bound
            total += 1
            print(f"{passed}/{total}: {g} --> {score}")

    # with open("v3to5_vals.txt","r+") as f:
    #     done = [line.strip().split()[0] for line in f]
    # todo = [g for g in todo if g not in done]

    # for g in tqdm(['salet'],colour='blue',desc='todo'):
    #     v = V5to6(g, game.answers, show = True, upper_bound=7920)
    #     with open("v5to6_vals.txt", "a+") as f:
    #         f.write(f"{g} ---> {v}\n")
    #     print(f"{g} ---> {v}")

    # with open('optimizedTrees2/newerWordle_30.json','r') as f:
    #     strategy = json.load(f)
    # for r, split in tqdm(sorted(list(strategy['splits'].items()), key=lambda x: x[1]['score'] * x[1]['nRemaining']), colour='blue'):
    #     # print(r)
    #     # print(split['nRemaining'])
    #     # print(split['score'])
    #     up = round(split['score'] * split['nRemaining'])
    #     print(r,'upper bound', up)

    #     C = filterPossible('tarse', r, game.answers)

    #     vals = [V1, V2, V3, V3to4]
    #     todo = game.guesses.copy()
    #     for val in vals:
    #         down = 1000000
    #         todo_next = []
    #         for g in tqdm(todo, colour='yellow', desc=f"{r} {val.__name__}"):
    #             score = val(g, C)
    #             if score <= up:
    #                 todo_next.append(g)
    #             down = min(score, down)
    #         if down == up:
    #             print(f"Proved {r} {val.__name__} hit {down} = {up}")
    #             with open("tarse_proof.txt", "a+") as f:
    #                 f.write(f"Proved {r} {val.__name__} hit {down} = {up}\n")
    #             break
                
    #         print(f"Progress {r} {val.__name__} at {down} < {up} remaining {len(todo_next)}")
    #         with open("tarse_proof.txt", "a+") as f:
    #             f.write(f"Progress {r} {val.__name__} at {down} < {up} remaining {len(todo_next)}\n")
    #         todo = todo_next
    #     else:
    #         print(f"UNPROVED {r} {val.__name__} got {down} < {up}")
    #         with open("tarse_proof.txt", "a+") as f:
    #             f.write(f"UNPROVED {r} {val.__name__} got {down} < {up}\n")


        # out_file = f"salet_vals/salet{r}_vals.txt"
        # if exists(out_file):
        #     continue

        # found = False
        # all_eq = True

        # # r = '00000'
        # # up = 609
        # C = filterPossible('salet', r, game.answers)
        # out_file = f"salet_vals/salet{r}_vals.txt"
        # todo = game.guesses
        # todo_next = []

        # for g in tqdm(todo,colour='blue',desc='todo v1'):
        #     v = V1(g, C, show = True)
        #     with open(out_file, "a+") as f:
        #         f.write(f"v1 {g} -> {v}\n")
        #     if v <= up:
        #         todo_next.append(g)
        #         if v != up:
        #             all_eq = False
        #     print(f"v1 {g} ---> {v} - cap {up}")
        # todo = todo_next
        # todo_next = []

        # if len(todo) == 1:
        #     with open(out_file, "a+") as f:
        #         f.write(f"ONLY {todo[0]}\n")
        #     continue

        # if all_eq:
        #     for g in todo:
        #         with open(out_file, "a+") as f:
        #             f.write(f"EQUAL {g}\n")
        #     continue  


        # all_eq = True
        # for g in tqdm(todo,colour='blue',desc='todo v2'):
        #     v = V2(g, C, show = True)
        #     with open(out_file, "a+") as f:
        #         f.write(f"v2 {g} -> {v}\n")
        #     if v <= up:
        #         todo_next.append(g)
        #         if v != up:
        #             all_eq = False
        #     print(f"v2 {g} ---> {v} - cap {up}")
        # todo = todo_next
        # todo_next = []

        # if len(todo) == 1:
        #     with open(out_file, "a+") as f:
        #         f.write(f"ONLY {todo[0]}\n")
        #     continue

        # if all_eq:
        #     for g in todo:
        #         with open(out_file, "a+") as f:
        #             f.write(f"EQUAL {g}\n")
        #     continue  
        
        # all_eq = True
        # for g in tqdm(todo,colour='blue',desc='todo v3'):
        #     v = V3(g, C, show = True)
        #     with open(out_file, "a+") as f:
        #         f.write(f"v3 {g} -> {v}\n")
        #     if v <= up:
        #         todo_next.append(g)
        #         if v != up:
        #             all_eq = False
        #     print(f"v3 {g} ---> {v} - cap {up}")
        # todo = todo_next
        # todo_next = []

        # if len(todo) == 1:
        #     with open(out_file, "a+") as f:
        #         f.write(f"ONLY {todo[0]}\n")
        #     continue

        # if all_eq:
        #     for g in todo:
        #         with open(out_file, "a+") as f:
        #             f.write(f"EQUAL {g}\n")
        #     continue  

        # all_eq = True
        # for g in tqdm(todo,colour='blue',desc='todo v3to4'):
        #     v = V3to4(g, C, show = True)
        #     with open(out_file, "a+") as f:
        #         f.write(f"v3to4 {g} -> {v}\n")
        #     if v <= up:
        #         todo_next.append(g)
        #         if v != up:
        #             all_eq = False
        #     print(f"v3to4 {g} ---> {v} - cap {up}")
        # todo = todo_next
        # todo_next = []

        # if len(todo) == 1:
        #     with open(out_file, "a+") as f:
        #         f.write(f"ONLY {todo[0]}\n")
        #     continue

        # if all_eq:
        #     for g in todo:
        #         with open(out_file, "a+") as f:
        #             f.write(f"EQUAL {g}\n")
        #     continue  

        # all_eq = True
        # for g in tqdm(todo,colour='blue',desc='todo v3to5'):
        #     v = V3to5(g, C, show = True)
        #     with open(out_file, "a+") as f:
        #         f.write(f"v3to5 {g} -> {v}\n")
        #     if v <= up:
        #         todo_next.append(g)
        #         if v != up:
        #             all_eq = False
        #     print(f"v3to5 {g} ---> {v} - cap {up}")
        # todo = todo_next
        # todo_next = []

        # if len(todo) == 1:
        #     with open(out_file, "a+") as f:
        #         f.write(f"ONLY {todo[0]}\n")
        #     continue

        # if all_eq:
        #     for g in todo:
        #         with open(out_file, "a+") as f:
        #             f.write(f"EQUAL {g}\n")
        #     continue  

        # all_eq = True
        # for g in tqdm(todo,colour='blue',desc='todo v5to6'):
        #     v = V5to6(g, C, show = True)
        #     with open(out_file, "a+") as f:
        #         f.write(f"v5to6 {g} -> {v}\n")
        #     if v <= up:
        #         todo_next.append(g)
        #         if v != up:
        #             all_eq = False
        #     print(f"v5to6 {g} ---> {v} - cap {up}")
        # todo = todo_next
        # todo_next = []

        # if len(todo) == 1:
        #     with open(out_file, "a+") as f:
        #         f.write(f"ONLY {todo[0]}\n")
        #     continue

        # if all_eq:
        #     for g in todo:
        #         with open(out_file, "a+") as f:
        #             f.write(f"EQUAL {g}\n")
        #     continue  

        #     v = V2(g, C, show = True)
        #     with open(out_file, "a+") as f:
        #         f.write(f"v2 {g} -> {v}\n")
        #     if v > up:
        #         continue

        #     v = V3(g, C, show = True)
        #     with open(out_file, "a+") as f:
        #         f.write(f"v3 {g} -> {v}\n")
        #     if v > up:
        #         continue

        #     v = V3to4(g, C, show = True)
        #     with open(out_file, "a+") as f:
        #         f.write(f"v3to4 {g} -> {v}\n")
        #     if v > up:
        #         continue

        #     v = V3to5(g, C, show = True)
        #     with open(out_file, "a+") as f:
        #         f.write(f"v3to5 {g} -> {v}\n")
        #     if v > up:
        #         continue


            

            # v = V3to5(g, C, show = True, upper_bound=609)
            # with open("salet00000_v3to5_vals.txt", "a+") as f:
            #     f.write(f"{g} ---> {v}\n")
            # print(f"{g} ---> {v}")
            