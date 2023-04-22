import json
from typing import Dict, List, Optional, Tuple

from new_config import Game
from new_definitions import Tree, Valuation
from new_utils import (encode, get_splits_with_words, no_filter_possible,
                       save_as_word_list, soft_filter_possible)
from new_valuations import multiVal


class BaseOptimizer:
    def __init__(
        self,
        game_name: str,
        file_name: str,
        max_depth: int = 10,
        max_breadth: int = 20,
        hard_mode: bool = False,
        vals: Optional[List[Valuation]] = None,
    ):
        game = Game.from_game_name(game_name)
        self.game_name = game_name

        self.G = game.guesses
        self.S = game.secrets
        self.r_star = game.r_star

        self.max_depth = max_depth
        self.max_breadth = max_breadth
        self.hard_mode = hard_mode

        if vals is None:
            vals = [multiVal]
        self.vals = vals

        self.guess_filter = soft_filter_possible if hard_mode else no_filter_possible

        self.breaches = 0
        self.hits = 0
        self.calls = 0

        self.best_guess: Dict[Tuple[int, int], str] = {}
        self.best_score: Dict[Tuple[int, int], int] = {}

        self.file_name = file_name

        self.tree: Optional[Tree] = None

    def explore(
        self, possible_guesses: List[str], possible_secrets: List[str], depth: int = 1
    ) -> float:
        raise NotImplementedError("Look ahead function")

    def generate_tree(
        self, possible_guesses: List[str], possible_secrets: List[str], depth: int = 1
    ) -> Tree:
        code = (
            encode(possible_guesses, self.G),
            encode(possible_secrets, self.S),
        )

        if code not in self.best_guess:
            self.explore(
                possible_guesses=possible_guesses,
                possible_secrets=possible_secrets,
                depth=depth,
            )

        guess = self.best_guess[code]
        score = self.best_score[code]

        tree: Tree = {
            "guess": guess,
            "score": score,
            "n_remaining": len(possible_secrets),
        }

        if len(possible_secrets) != 1:
            tree_splits = {}
            splits = get_splits_with_words(guess, possible_secrets)
            for res, split in splits.items():
                if res == self.r_star:
                    continue
                tree_splits[res] = self.generate_tree(
                    possible_guesses=self.guess_filter(guess, res, possible_guesses),
                    possible_secrets=split,
                    depth=depth + 1,
                )
            tree["splits"] = tree_splits

        return tree

    def get_tree(self) -> Tree:
        if self.tree is None:
            self.tree = self.generate_tree(
                possible_guesses=self.G,
                possible_secrets=self.S,
            )
        return self.tree
    
    def get_best_score(self) -> int:
        tree = self.get_tree()
        return tree["score"]

    def to_json(self):
        print(f"Writing JSON to {self.file_name}.json")
        tree = self.get_tree()
        with open(f"optimizedTrees4/{self.file_name}.json", "w") as f:
            json.dump(tree, f, sort_keys=True, indent=4)
        print(f"Wrote JSON at {self.file_name}.json")

    def to_word_list(self):
        print(f"Writing word list to {self.file_name}.txt")
        save_as_word_list(
            tree=self.get_tree(),
            file_name=f"optimizedTrees4/{self.file_name}.txt",
            secrets=self.S,
        )
        print(f"Wrote word list at {self.file_name}.txt")

    def show_stats(self):
        print("----- GAME:", self.game_name.capitalize(), "-----")
        print("HARD MODE ON?:", self.hard_mode)
        print("# POSSIBLE GUESSES:", len(self.G))
        print("# POSSIBLE SECRETS:", len(self.S))
        print("MAX BREADTH:", self.max_breadth)
        print("MAX_DEPTH:", self.max_depth)
        score = self.best_score[(encode(self.G, self.G), encode(self.S, self.S))]
        print("BEST SCORE:", score)
        print("BEST EXPECTED:", score / len(self.S))
        print("HITS:", self.hits)
        print("BREACHES:", self.breaches)
        print("CALLS: ", self.calls)
        print("--------------------------")

    def get_depth(self, tree: Optional[Tree] = None) -> int:
        if tree is None:
            assert self.tree is not None
            tree = self.tree

        if "splits" not in tree:
            return 1

        return 1 + max(self.get_depth(tt) for tt in tree["splits"].values())
