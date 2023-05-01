from typing import List, Optional

from tqdm import tqdm

from new_base_optimizer import BaseOptimizer
from new_definitions import (DEBUG_COLOURS, DEBUG_LEVEL, INFINITY,
                             N_DEBUG_COLOURS, Guess, Secret, Valuation)
from new_utils import encode, get_splits_with_words, sort_words, useful_guesses

TotalScoreType = int


class TotalOptimizer(BaseOptimizer[TotalScoreType]):
    def __init__(
        self,
        game_name: str,
        folder_name="new_optimized_trees",
        max_depth: int = 10,
        max_breadth: int = 20,
        hard_mode: bool = False,
        vals: Optional[List[Valuation]] = None,
    ):
        file_name = f"{game_name}_{max_breadth}{'_hard' if hard_mode else ''}"
        super(TotalOptimizer, self).__init__(
            folder_name=folder_name,
            file_name=file_name,
            game_name=game_name,
            max_depth=max_depth,
            max_breadth=max_breadth,
            hard_mode=hard_mode,
            vals=vals,
        )

    def explore(
        self,
        possible_guesses: List[Guess],
        possible_secrets: List[Secret],
        depth: int = 1,
    ) -> TotalScoreType:
        self.calls += 1

        disable_debug = depth > DEBUG_LEVEL
        debug_colour = DEBUG_COLOURS[depth % N_DEBUG_COLOURS]

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

        if n_remaining == 2:
            self.best_guess[code] = possible_secrets[0]
            self.best_score[code] = 3
            return self.best_score[code]

        if depth >= self.max_depth:
            self.best_guess[code] = possible_secrets[0]
            self.best_score[code] = INFINITY
            self.breaches += 1
            return self.best_score[code]

        options = useful_guesses(possible_guesses, possible_secrets)

        options = sort_words(
            G=options,
            S=possible_secrets,
            vals=self.vals,
            n=self.max_breadth,
            show_progress=not disable_debug,
        )

        for g in tqdm(
            options,
            disable=disable_debug,
            colour=debug_colour,
            desc=f"Depth {depth}",
        ):
            splits = get_splits_with_words(g, possible_secrets)

            if len(splits) == 1:
                continue

            score = len(possible_secrets)
            for res, split in tqdm(
                splits.items(), disable=disable_debug, colour="yellow", desc=g
            ):
                if res == self.r_star:
                    continue

                score += self.explore(
                    possible_guesses=self.guess_filter(g, res, possible_guesses),
                    possible_secrets=split,
                    depth=depth + 1,
                )

            if self.best_score.get(code, INFINITY) > score:
                self.best_score[code] = score
                self.best_guess[code] = g

        return self.best_score[code]


def main():
    breadths = [30]
    game_names = [
        # "old_wordle",
        # "mininerdle",
        # "ffxivrdle",
        # "bardle",
        # "primel",
        # "nerdle",
        "newer_wordle",
    ]

    for breadth in breadths:
        for game_name in game_names:
            optimizer = TotalOptimizer(
                game_name=game_name,
                max_depth=10,
                max_breadth=breadth,
                hard_mode=False,
            )

            optimizer.to_json()
            optimizer.show_stats()
            optimizer.to_word_list()


if __name__ == "__main__":
    main()
