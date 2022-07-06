class Config(object):
    def __init__(self, game):

        configs = {
            'wordle' : {
                'guessFile' : 'wordLists/wordleGuesses.txt',
                'answerFile' : 'wordLists/wordleAnswers.txt',
                'rStar' : '22222'
            },
            'originalWordle': {
                'guessFile' : 'wordLists/originalWordleGuesses.txt',
                'answerFile' : 'wordLists/originalWordleAnswers.txt',
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
            }
        }

        config = configs[game]

        self.game = game
        self.guesses = self.readFromFile(config['guessFile'])
        self.answers = self.readFromFile(config['answerFile'])
        self.rStar = config['rStar']

    def readFromFile(fname):
        with open(fname,'r') as f:
            return [s.strip() for s in f]