import json
from typing import Any, Dict, Generic, List, Optional

from new_config import Game
from new_definitions import Encoding, Guess, Score, Secret, Tree, Valuation
from new_utils import (
    encode,
    get_splits_with_words,
    no_filter_possible,
    save_as_word_list,
    soft_filter_possible,
)
from new_valuations import multi_val


class BaseOptimizer(Generic[Score]):
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
            vals = [multi_val]
        self.vals = vals

        self.guess_filter = soft_filter_possible if hard_mode else no_filter_possible

        self.breaches = 0
        self.hits = 0
        self.calls = 0

        self.best_guess: Dict[Encoding, Guess] = {}
        self.best_score: Dict[Encoding, Score] = {}

        self.file_name = file_name

        self.tree: Optional[Tree] = None

    def explore(
        self,
        possible_guesses: List[Guess],
        possible_secrets: List[Secret],
        depth: int = 1,
    ) -> Score:
        raise NotImplementedError("Look ahead function")

    def generate_tree(
        self,
        possible_guesses: List[Guess],
        possible_secrets: List[Secret],
        depth: int = 1,
    ) -> Tree[Score]:
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

        tree = Tree(
            guess=guess,
            score=score,
            n_remaining=len(possible_secrets),
        )

        if len(possible_secrets) != 1:
            splits = get_splits_with_words(guess, possible_secrets)
            for res, split in splits.items():
                if res == self.r_star:
                    continue
                tree.splits[res] = self.generate_tree(
                    possible_guesses=self.guess_filter(guess, res, possible_guesses),
                    possible_secrets=split,
                    depth=depth + 1,
                )

        return tree

    def get_tree(self) -> Tree[Score]:
        if self.tree is None:
            self.tree = self.generate_tree(
                possible_guesses=self.G,
                possible_secrets=self.S,
            )
        return self.tree

    def get_best_score(self) -> Score:
        tree = self.get_tree()
        return tree.score

    def to_dict(self, tree: Optional[Tree] = None) -> Dict[str, Any]:
        if tree is None:
            tree = self.get_tree()

        out = {
            "guess": tree.guess,
            "score": tree.score,
            "n_remaining": tree.n_remaining,
        }
        if len(tree.splits) != 0:
            subtrees = {}
            for g, tt in tree.splits.items():
                subtrees[g] = self.to_dict(tt)

            out["splits"] = subtrees
        return out

    def to_json(self):
        print(f"Writing JSON to {self.file_name}.json")
        tree = self.to_dict()
        with open(f"new_optimized_trees/{self.file_name}.json", "w") as f:
            json.dump(tree, f, sort_keys=True, indent=4)
        print(f"Wrote JSON at {self.file_name}.json")

    def to_word_list(self):
        print(f"Writing word list to {self.file_name}.txt")
        save_as_word_list(
            tree=self.get_tree(),
            file_name=f"new_optimized_trees/{self.file_name}.txt",
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
        print("HITS:", self.hits)
        print("BREACHES:", self.breaches)
        print("CALLS: ", self.calls)
        print("--------------------------")

    def get_depth(self, tree: Optional[Tree] = None) -> int:
        if tree is None:
            assert self.tree is not None
            tree = self.tree

        if len(tree.splits) == 0:
            return 1

        return 1 + max(self.get_depth(tt) for tt in tree.splits.values())
