from new_base_optimizer import BaseOptimizer
from new_utils import encode, useful_guesses
from new_definitions import INFINITY


class ExpectedOptimizer(BaseOptimizer):
    def __init__(self, *args, **kwargs):
        super(ExpectedOptimizer, self).__init__(
            *args,
            **kwargs,
            file_name=f"{self.game}_{self.MAX_BREADTH}{'_hard' if self.hardMode else ''}",
        )

    def explore(
        self, possible_guesses: List[str], possible_secrets: List[str], depth: int = 1
    ) -> float:
        self.calls += 1

        code = (
            encode(possible_guesses, self.G),
            encode(possible_secrets, self.S),
        )

        if code in self.best_score:
            self.hits += 1
            return self.best_score[code]

        # Special cases first
        n_remaining = len(possible_secrets)
        if n_remaining == 1:
            self.best_guess[code] = possible_secrets[0]
            self.best_score[code] = 1
            return self.best_score[code]
        elif n_remaining == 2:
            self.best_score[code] = possible_secrets[0]
            self.best_score[code] = 1.5
            return self.best_score[code]
        elif depth >= self.max_depth:
            self.best_guess[code] = possible_secrets[0]
            self.best_score[code] = INFINITY
            self.breaches += 1
            return self.best_score[code]

        options = useful_guesses(possible_guesses, possible_secrets)

        options = sort_words(
            G=options,
            S=possible_secrets,
            vals=self.vals,
            n=self.MAX_BREADTH,
            showProg=(depth <= self.DEBUG_LEVEL),
        )
