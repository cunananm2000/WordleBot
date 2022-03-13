import math


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
