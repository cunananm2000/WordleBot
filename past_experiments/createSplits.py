from wordLists import guesses, answers 
import json
from utils import getSplits

G = sorted(guesses + answers)
S = sorted(answers)

for g in G:
    splits = getSplits(g, S, useWords=True)
    with open(f"initialSplits/{g}.json", "w") as f:
        json.dump(splits, f, sort_keys=True)
    print(g,end=' ')
print('')