from typing import List, Optional, Tuple

from tqdm import tqdm

from new_base_optimizer import BaseOptimizer
from new_definitions import (DEBUG_COLOURS, DEBUG_LEVEL, INFINITY,
                             N_DEBUG_COLOURS, Valuation)
from new_utils import encode, get_splits_with_words, sort_words, useful_guesses

WorstScoreType = Tuple[int, int]


class WorstOptimizer(BaseOptimizer[WorstScoreType]):
    def __init__(
        self,
        game_name: str,
        max_depth: int = 10,
        max_breadth: int = 20,
        hard_mode: bool = False,
        vals: Optional[List[Valuation]] = None,
    ):
        file_name = f"{game_name}_{max_breadth}_worst{'_hard' if hard_mode else ''}"
        super(WorstOptimizer, self).__init__(
            file_name=file_name,
            game_name=game_name,
            max_depth=max_depth,
            max_breadth=max_breadth,
            hard_mode=hard_mode,
            vals=vals,
        )

    def explore(
        self, possible_guesses: List[str], possible_secrets: List[str], depth: int = 1
    ) -> WorstScoreType:
        self.calls += 1
        code = (
            encode(possible_guesses, self.G),
            encode(possible_secrets, self.S),
        )

        disable_debug = depth > DEBUG_LEVEL
        debug_colour = DEBUG_COLOURS[depth % N_DEBUG_COLOURS]

        if code in self.best_score:
            self.hits += 1
            return self.best_score[code]

        # Special cases first
        if len(possible_secrets) == 1:
            self.best_guess[code] = possible_secrets[0]
            self.best_score[code] = (1, 1)
            return self.best_score[code]

        if len(possible_secrets) == 2:
            self.best_guess[code] = possible_secrets[0]
            self.best_score[code] = (2, 1)
            return self.best_score[code]

        if depth >= self.max_depth:
            self.best_guess[code] = possible_secrets[0]
            self.best_score[code] = (INFINITY, 1)
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

            max_depth = 1
            at_max_depth = 1

            for res, split in tqdm(
                splits.items(), disable=disable_debug, colour="yellow", desc=g
            ):
                if res == self.r_star:
                    continue

                sub_depth, at_sub_depth = self.explore(
                    possible_guesses=self.guess_filter(g, res, possible_guesses),
                    possible_secrets=split,
                    depth=depth + 1,
                )
                sub_depth += 1

                if sub_depth > max_depth:
                    max_depth, at_max_depth = sub_depth, 0

                if sub_depth == max_depth:
                    at_max_depth += at_sub_depth

            score = (max_depth, at_max_depth)

            if self.best_score.get(code, (INFINITY, 1)) > score:
                self.best_score[code] = score
                self.best_guess[code] = g

        return self.best_score[code]


def main():
    breadths = [1]
    game_names = [
        # "old_wordle",
        "mininerdle",
        "ffxivrdle",
        # "bardle",
        # "primel",
        # "nerdle",
        # "newer_wordle",
    ]

    for breadth in breadths:
        for game_name in game_names:
            optimizer = WorstOptimizer(
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
