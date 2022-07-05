import math
from re import L

from wordfreq import zipf_frequency


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


def pprint(res):
    for x in res:
        if x == "1":
            print("\U0001f7e8", end="")
        elif x == "2":
            print("\U0001f7e9", end="")
        else:
            print("\u2B1B", end="")
    print("")


def check(guess, answer, debug=False, nLetters=5):
    # key = guess + answer
    # if key not in self.checkCache: key = answer + guess
    # if key not in self.checkCache:
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

    return "".join(res)


def filterPossible(guess, res, candidates):
    return [x for x in candidates if check(guess, x) == res]

def filterMultiple(history, candidates):
    for g,r in history:
        candidates = filterPossible(g, r, candidates)
    return candidates


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

    
def sortWords(C, S, vals, n = 5):
    C.sort(key=lambda c: tuple((v(c, S) for v in vals)))
    return C[:n]

def softMatch(guess, res, cand, nLetters = 5):
    used = [False]*nLetters
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
        

def softFilterPossible(guess, res, candidates):
    return [c for c in candidates if softMatch(guess, res, c)]

def softFilterMultiple(history, candidates):
    for g,r in history:
        candidates = softFilterPossible(g, r, candidates)
    return candidates