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

    return zipf_frequency(word, 'en')