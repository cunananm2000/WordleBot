import math
from typing import List

from tqdm import tqdm

from new_config import Game
from new_definitions import MAX_BOUND_DEPTH
from new_utils import get_splits_with_words, max_splits, useful_guesses

game = Game.from_game_name("bardle")


def bound(n: int, b: int) -> int:
    if n == 0:
        return 0
    if n == 1:
        return 1
    if b == 1:
        return (n * (n + 1)) // 2

    k = int(math.log(n * (b - 1) + 1) / math.log(b))
    return sum(i * (b ** (i - 1)) for i in range(1, k + 1)) + (k + 1) * (
        n - (b**k - 1) // (b - 1)
    )


def LB_1(C: List[str]) -> int:
    return bound(len(C), game.max_splits)


def LB_2(C: List[str]) -> int:
    return bound(len(C), max_splits(game.guesses, C))


def V(i: int, g: str, C: List[str]) -> int:
    splits = get_splits_with_words(g, C)
    out = len(C)
    for res, split in splits.items():
        if res == game.r_star:
            continue
        out += LB(i, split)

    return out


def LB(i: int, C: List[str]) -> int:
    if i == 1:
        return LB_1(C)

    if i == 2:
        return LB_2(C)

    return min(V(i - 2, g, C) for g in useful_guesses(game.guesses, C))


if __name__ == "__main__":
    game = Game.from_game_name("ffxivrdle")
    todo = game.guesses

    for depth in range(1, MAX_BOUND_DEPTH + 1):
        processed = 0
        below = 0

        todo_next = []
        for g in tqdm(todo):
            with open(f"new_bound_results/{game.game_name}/V{depth}.txt", "a+") as f:
                score = V(depth, g, game.secrets)
                f.write(f"{g} --> {score}\n")
                if score <= game.upper_bound:
                    todo_next.append(g)
                below += score < game.upper_bound
                processed += 1
                print(f"{below}/{processed}: {g} --> {score}")

        with open(f"new_bound_results/{game.game_name}/V{depth}.txt", "a+") as f:
            f.write("--------------\n")

        todo = todo_next

        if (len(todo) == 0) or (below == 0):
            print(f"Stopped early at depth {depth}. Options: {todo}")
            with open(f"new_bound_results/{game.game_name}/V{depth}.txt", "a+") as f:
                f.write(f"Options: {todo}\n")
            break
