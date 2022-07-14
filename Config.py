class Config(object):
    def __init__(self, game):

        configs = {
            'newWordle' : {
                'guessFile' : 'wordLists/newWordleGuesses.txt',
                'answerFile' : 'wordLists/newWordleAnswers.txt',
                'rStar' : '22222'
            },
            'oldWordle': {
                'guessFile' : 'wordLists/oldWordleGuesses.txt',
                'answerFile' : 'wordLists/oldWordleAnswers.txt',
                'rStar' : '22222'
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

    def readFromFile(self, fname):
        with open(fname,'r') as f:
            return [s.strip() for s in f]