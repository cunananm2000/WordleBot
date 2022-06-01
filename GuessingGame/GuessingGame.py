class GuessingGame(object):
    def __init__(self, guesses, secrets, check) -> None:
        self.G = guesses
        self.S = secrets
        self.a = check
        self.rStar = "22222"

    def play(self, s):
        r = None
        C = self.S.copy()
        for i in range(1, 11):
            g = self.strategy(C)
            print(f"Guess {i}: {g}")
            r = self.a(g, s)
            print(f"    Response: {r}")
            if r == self.rStar:
                return i
            C = self.filterCandidates(g, r, C)
        return -1

    def strategy(self, C):
        # assert(False)
        return C[0]

    def filterCandidates(self, g, r, C):
        return [c for c in C if self.a(g, c) == r]
