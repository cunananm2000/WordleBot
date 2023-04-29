from tqdm.auto import tqdm
from utils import getSplits

class Config(object):
    def __init__(self, game):

        configs = {
            'newWordle' : {
                'guessFile' : 'wordLists/newWordleGuesses.txt',
                'answerFile' : 'wordLists/newWordleAnswers.txt',
                'rStar' : '22222'
            },
            'newerWordle' : {
                'guessFile' : 'wordLists/newerWordleGuesses.txt',
                'answerFile' : 'wordLists/newerWordleAnswers.txt',
                'rStar' : '22222',
                'maxsplits': 150,
                'upper_bound': 7883
            },
            'oldWordle': {
                'guessFile' : 'wordLists/oldWordleGuesses.txt',
                'answerFile' : 'wordLists/oldWordleAnswers.txt',
                'rStar' : '22222',
                'maxsplits': 150,
            },
            'primel': {
                'guessFile' : 'wordLists/primelWords.txt',
                'answerFile' : 'wordLists/primelWords.txt',
                'rStar' : '22222'
            },
            'mininerdle': {
                'guessFile': 'wordLists/mininerdleWords.txt',
                'answerFile': 'wordLists/mininerdleWords.txt',
                'rStar': '222222'
            },
            'bardle': {
                'guessFile': 'wordLists/bardleGuesses.txt',
                'answerFile': 'wordLists/bardleAnswers.txt',
                'rStar': '22222'
            },
            'mathler': {
                'guessFile': 'wordLists/mathlerWords.txt',
                'answerFile': 'wordLists/mathlerWords.txt',
                'rStar': '222222'
            },
            'nerdle': {
                'guessFile': 'wordLists/nerdleWords.txt',
                'answerFile': 'wordLists/nerdleWords.txt',
                'rStar': '22222222'
            },
            'ffxivrdle': {
                'guessFile': 'wordLists/ffxivrdleGuesses.txt',
                'answerFile': 'wordLists/ffxivrdleAnswers.txt',
                'rStar': '22222' 
            }
        }

        config = configs[game]

        self.game = game
        self.guesses = self.readFromFile(config['guessFile'])
        self.answers = self.readFromFile(config['answerFile'])
        self.rStar = config['rStar']
        if 'maxsplits' in config:
            self.maxsplits = config['maxsplits']
        else:
            self.maxsplits = max(len(getSplits(g, self.answers)) for g in tqdm(self.guesses, desc="TEMPORARY MAXSPLITS"))
            print("SAVE THIS VALUE:", self.maxsplits)

        self.upper_bound = config.get('upper_bound', 99999)

    def readFromFile(self, fname):
        with open(fname,'r') as f:
            return [s.strip() for s in f]