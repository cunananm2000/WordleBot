import math
from itertools import product
from tqdm.auto import tqdm
# from valuations import inSet

from wordfreq import zipf_frequency

check_cache = {}


def getWordFreqDict():
    wordFreqs = {}

    with open("wordFreqs.txt", encoding="utf8") as f:
        for line in f:
            v, k = line.split()
            wordFreqs[k] = float(v)
    hi = max(wordFreqs.values())
    for k in wordFreqs.keys():
        wordFreqs[k] = 1 / (1 + math.exp(-(wordFreqs[k] / hi - 0.5)))

    return wordFreqs


def getWordFreq(word):
    return zipf_frequency(word, "en")


def getSplits(g, C, useWords=False):
    splits = {}
    for c in C:
        res = check(g, c)
        if useWords:
            if res not in splits:
                splits[res] = []
            splits[res].append(c)
        else:
            splits[res] = splits.get(res, 0) + 1

    return splits

def getSplitsMultiple(G, C, useWords=False):
    splits = {}
    for c in C:
        key = tuple(check(g,c) for g in G)
        if useWords:
            if key not in splits:
                splits[key] = []
            splits[key].append(c)
        else:
            splits[key] = splits.get(key, 0) + 1
    return splits

def getSimulSplits(g, D, useWords=False):
    game_splits = [getSplits(g, C, useWords = True) for C in D]
    keys = list(product(*[list(splits.keys()) for splits in game_splits]))
    out = {}
    for key in keys:
        wordSet = [game_split[res] for game_split,res in zip(game_splits, key)]
        # print(g,key, wordSet)
        count = countWithNonrepeats(wordSet)
        if count == 0: continue
        if useWords:
            out[key] = wordSet
        else:
            out[key] = count
    return out


def pprint(res):
    for x in res:
        if x == "1":
            print("\U0001f7e8", end="")
        elif x == "2":
            print("\U0001f7e9", end="")
        else:
            print("\u2B1B", end="")
    print("")

def countWithNonrepeats(D):
    if len(D) == 1:
        return len(D[0])
    
    if len(D) == 2:
        A, B = D
        t = len(A) * len(B) - len(set(A).intersection(set(B)))
        # if t == 0:
        #     print(D)
        #     assert False
        return t
    
    t = 0
    for tup in product(*D):
        t += len(set(tup)) == len(tup)
    
    return t


def old_check(guess, answer, debug=False):
    code = guess+answer

    global check_cache

    if code in check_cache: return check_cache[code]

    if len(check_cache) >= 100_000:
        check_cache = {}

    nLetters = len(guess)
    # print(guess, answer)
    res = ["0"] * nLetters
    hit = [False] * nLetters

    for i in range(nLetters):
        if guess[i] == answer[i]:
            res[i] = "2"
            hit[i] = True
    for i in range(nLetters):
        if res[i] == "0":
            for j in range(nLetters):
                if guess[i] == answer[j] and not hit[j]:
                    res[i] = "1"
                    hit[j] = True
                    break
    if debug:
        pprint(res)

    check_cache[code] = "".join(res)
    
    return check_cache[code]

def check(g, s, debug=False):
    code = g+s

    global check_cache


    if code in check_cache: return check_cache[code]

    if len(check_cache) >= 1_000_00:
        # print("clearing cache")
        check_cache = {}


    res = ['0'] * len(g)

    freq = {}
    for l in s:
        freq[l] = freq.get(l,0) + 1

    for i,(a,b) in enumerate(zip(g,s)):
        if a == b:
            freq[a] -= 1
            res[i] = '2'
            continue


    for i, a in enumerate(g):
        if freq.get(a,0) == 0: continue
        if res[i] != '0': continue
        res[i] = '1'
        freq[a] -= 1

    out = "".join(res)

    check_cache[code] = out

    return out


def filterPossible(guess, res, candidates):
    return [x for x in candidates if check(guess, x) == res]

def filterMultiple(history, candidates):
    for g,r in history:
        candidates = filterPossible(g, r, candidates)
    return candidates

def filterSimul(guess, rs, D):
    return list(filterPossible(guess, r, cands) for r,cands in zip(rs, D))

def isUseful(guess, C):
    if len(C) <= 1: return guess in C
    res = check(guess, C[0])
    for c in C[1:]:
        if check(guess, c) != res: return True

    return False



def usefulGuesses(G, C):
    if len(C) <= 1: return C.copy()
    return [g for g in G if isUseful(g, C)]


def saveAsWordList(tree, fname, answers):
    with open(fname,'w') as g:
        for s in answers:
            ans = []
            curr = tree
            while 1:
                ans.append(curr['guess'])
                if curr['guess'] == s: break
                res = check(curr['guess'], s)
                curr = curr['splits'][res]
            g.write(','.join(ans) + '\n')

    
def sortWords(G, S, vals, n, showProg = False):
    # C.sort(key=lambda c: tuple((v(c, S) for v in vals)))
    # print('sorting words')
    if n >= len(G): return G 
    scores = [(tuple((v(g, S) for v in vals)), g) for g in tqdm(G, disable = not(showProg), colour='red')]
    scores.sort()
    return [g for _,g in scores[:n]]

def softMatch(guess, res, cand):
    used = [False]*len(guess)
    for i,(g,r,c) in enumerate(zip(guess, res, cand)):
        if r == '2':
            if g != c: return False 
            used[i] = True 
    
    for i,(g,r) in enumerate(zip(guess, res)):
        # print(i,g,r)
        if r == '1':
            # print('wo')
            for j,c in enumerate(cand):
                if used[j]: continue 
                if c == g:
                    used[j] = True 
                    break 
            else:
                return False
        # print(used)

    return True 

def noFilterPossible(guess, res, candidates):
    return candidates
        

def softFilterPossible(guess, res, candidates):
    return [c for c in candidates if softMatch(guess, res, c)]

def softFilterMultiple(history, candidates):
    for g,r in history:
        candidates = softFilterPossible(g, r, candidates)
    return candidates