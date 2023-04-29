import math
import os
import re
from typing import Dict, List

from tqdm import tqdm

from new_config import Game
from new_definitions import BORDER, MAX_BOUND_DEPTH
from new_utils import get_splits_with_words, max_splits, useful_guesses

game = Game.from_game_name("newer_wordle")


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


def file_finished(file_name: str) -> bool:
    with open(file_name, "r") as f:
        lines = (l.strip() for l in f)
        for line in lines:
            if line == BORDER:
                return True
    return False


def extract_guess_scores(file_name: str) -> Dict[str, int]:
    out = {}
    pattern = re.compile("(\\w+) --> (\\d+)")
    with open(file_name, "r") as f:
        lines = (l.strip() for l in f)
        for line in lines:
            res = pattern.search(line)
            if res is None:
                continue

            guess = res.group(1)
            score = int(res.group(2))

            out[guess] = score
    return out


def main():
    global game
    game = Game.from_game_name("newer_wordle")
    todo = game.guesses

    result_folder = "new_bound_results/"
    if not os.path.isdir(result_folder):
        print(f"Creating folder {result_folder}")
        os.mkdir(result_folder)
    else:
        print(f"Folder {result_folder} already exists")

    game_result_folder = f"{result_folder}/{game.game_name}/"
    if not os.path.isdir(game_result_folder):
        print(f"Creating folder {game_result_folder}")
        os.mkdir(game_result_folder)
    else:
        print(f"Folder {game_result_folder} already exists")

    last_depth = MAX_BOUND_DEPTH + 1
    last_path = ""
    for depth in range(MAX_BOUND_DEPTH, -1, -1):
        last_depth = depth
        last_path = f"{game_result_folder}/V{last_depth}.txt"
        if os.path.exists(last_path):
            break

    print("Last processed depth", last_depth)

    start_depth = 1
    if last_depth != 0:
        if file_finished(last_path):
            start_depth = last_depth + 1
            guess_scores = extract_guess_scores(last_path)
            todo = [
                g for (g, score) in guess_scores.items() if score <= game.upper_bound
            ]
        elif last_depth > 1:
            start_depth = last_depth
            last_finished_path = f"{game_result_folder}/V{last_depth-1}.txt"

            guess_scores = extract_guess_scores(last_finished_path)
            todo = [
                g for (g, score) in guess_scores.items() if score <= game.upper_bound
            ]

            done_guess_scores = extract_guess_scores(last_path)

            todo = [g for g in todo if g not in done_guess_scores]

    for depth in range(start_depth, MAX_BOUND_DEPTH + 1):
        processed = 0
        below = 0

        game_result_file = f"V{depth}.txt"

        todo_next = []
        for g in tqdm(todo):
            with open(f"{game_result_folder}/{game_result_file}", "a+") as f:
                score = V(depth, g, game.secrets)
                f.write(f"{g} --> {score}\n")
                if score <= game.upper_bound:
                    todo_next.append(g)
                below += score < game.upper_bound
                processed += 1
                # print(f"{len(todo_next)}/{processed}: {g} --> {score}")

        with open(f"{game_result_folder}/{game_result_file}", "a+") as f:
            f.write(f"{BORDER}\n")
            f.write(
                f"Below/Todo/Processed/Total: {below}/{len(todo_next)}/{processed}/{len(todo)}\n"
            )

        todo = todo_next

        if (len(todo) == 0) or (below == 0):
            print(f"Stopped early at depth {depth}. Options: {todo}")
            with open(f"{game_result_folder}/{game_result_file}", "a+") as f:
                f.write(f"Options: {todo}\n")
            break


if __name__ == "__main__":
    main()
