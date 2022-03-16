import math
from wordfreq import zipf_frequency
import requests


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
    # response = requests.get(f"https://api.datamuse.com/words?sp={word}&md=f&max=1")
    # return response.json()[0]['score']

    return zipf_frequency(word, "en")


def getSplits(g, G, useWords=False):
    splits = {}
    for g0 in G:
        res = check(g, g0)
        if useWords:
            if res not in splits:
                splits[res] = []
            splits[res].append(g0)
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


def filterPossible(possibleGuess, possibleRes, candidates):
    return [x for x in candidates if check(possibleGuess, x) == possibleRes]
