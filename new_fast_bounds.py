import math
import os
import re
from typing import Dict, List

from tqdm import tqdm

from new_config import Game
from new_definitions import BORDER, BOUND_DEBUG_LEVEL, INFINITY, MAX_BOUND_DEPTH
from new_total_optimizer import TotalOptimizer
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


def V_1(g: str, C: List[str], upper_bound: int = INFINITY) -> int:
    splits = get_splits_with_words(g, C)
    out = len(C)

    disable_debug = not (1 >= BOUND_DEBUG_LEVEL)

    for res, split in tqdm(splits.items(), desc=f"v1 {g}", disable=disable_debug):
        if res == game.r_star:
            continue
        out += LB_1(split)
        if out > upper_bound:
            return out
    return out


def V_2(g: str, C: List[str], upper_bound: int = INFINITY) -> int:
    splits = get_splits_with_words(g, C)

    split_scores = [(LB_1(split), res) for res, split in splits.items()]
    split_scores.sort(reverse=True)

    disable_debug = not (2 >= BOUND_DEBUG_LEVEL)

    total = sum(x[0] for x in split_scores) + len(C)

    if total > upper_bound:
        return total

    for _ in tqdm(range(len(split_scores)), desc=f"v2 {g}", disable=disable_debug):
        score, res = split_scores.pop(0)

        updated_score = LB_2(splits[res])

        total -= score
        total += updated_score

        if total > upper_bound:
            return total

    return total


def LB(i: int, C: List[str], req_diff: int = INFINITY) -> int:
    if i == 1:
        return LB_1(C)

    if i == 2:
        return LB_2(C)

    ug = useful_guesses(game.guesses, C)

    upper_bound = INFINITY
    if len(C) > 500:
        print("Making optimizer")
        total_optimizer = TotalOptimizer(game_name=game.game_name, max_breadth=5)
        total_optimizer.S = C.copy()
        upper_bound = total_optimizer.get_best_score()
        print("Solved optimizer, best upper bound is", upper_bound)

    if i <= 4:
        return min(V(i - 2, g, C, upper_bound) for g in ug)

    disable_debug = not (i > BOUND_DEBUG_LEVEL)

    # If LB_i - LB_{i-2} > req_diff can exit early
    guess_scores = sorted([(min(V(i - 4, g, C) for g in ug), False, g) for g in ug])

    old_base = guess_scores[0][0]

    for _ in tqdm(ug, disable=disable_debug, desc=f"LB_{i}"):
        _, recomputed, g = guess_scores.pop(0)
        if recomputed:
            break

        updated_score = V(i - 2, g, C, upper_bound)

        guess_scores.append((updated_score, True, g))
        guess_scores.sort()

        if guess_scores[0][0] - old_base > req_diff:
            return guess_scores[0][0]

    return guess_scores[0][0]


def V(i: int, g: str, C: List[str], upper_bound: int = INFINITY) -> int:
    if i == 1:
        return V_1(g, C, upper_bound)

    if i == 2:
        return V_2(g, C, upper_bound)

    splits = get_splits_with_words(g, C)

    split_scores = [(LB(i - 2, split), res) for res, split in splits.items()]
    split_scores.sort(reverse=True)

    out = len(C) + sum(x[0] for x in split_scores)
    if out > upper_bound:
        return out

    disable_debug = not (i > BOUND_DEBUG_LEVEL)

    for _ in tqdm(range(len(split_scores)), disable=disable_debug, desc=f"V_{i} {g}"):
        score, res = split_scores.pop(0)
        updated_score = LB(i, splits[res], req_diff=upper_bound - out)

        out -= score
        out += updated_score

        if out > upper_bound:
            return out

    return out


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


if __name__ == "__main__":
    game = Game.from_game_name("newer_wordle")

    todo = game.guesses

    result_folder = "new_fast_bound_results/"
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
        for f in tqdm(todo):
            with open(f"{game_result_folder}/{game_result_file}", "a+") as f:
                score = V(depth, f, game.secrets, upper_bound=game.upper_bound)
                f.write(f"{f} --> {score}\n")
                if score <= game.upper_bound:
                    todo_next.append(f)
                below += score < game.upper_bound
                processed += 1
                print(f"{len(todo_next)}/{processed}: {f} --> {score}")

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
