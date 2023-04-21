from typing import Dict, List, Tuple

from tqdm import tqdm

from new_definitions import CACHE_LIMIT, Valuation


class CHECK_CACHE:
    cache: Dict[Tuple[str, str], str] = {}


def read_from_file(fname: str) -> List[str]:
    """Read lines from a file into a list of lines

    Args:
        fname (str): _description_

    Returns:
        List[str]: _description_
    """
    with open(fname, "r") as f:
        return [s.strip() for s in f]


def check(g: str, s: str, debug: bool = False) -> str:
    """Checking function comparing s to g

    Args:
        g (str): Guess
        s (str): Secret
        debug (bool, optional): _description_. Defaults to False.

    Returns:
        str: 0, 1, 2's to represent colours e.g. in Wordle.
    """
    code = (g, s)

    if code in CHECK_CACHE.cache:
        return CHECK_CACHE.cache[code]

    if len(CHECK_CACHE.cache) >= CACHE_LIMIT:
        CHECK_CACHE.cache = {}

    res = ["0"] * len(g)

    freq: Dict[str, int] = {}
    for l in s:
        freq[l] = freq.get(l, 0) + 1

    for i, (a, b) in enumerate(zip(g, s)):
        if a == b:
            freq[a] -= 1
            res[i] = "2"
            continue

    for i, a in enumerate(g):
        if freq.get(a, 0) == 0:
            continue
        if res[i] != "0":
            continue
        res[i] = "1"
        freq[a] -= 1

    out = "".join(res)

    CHECK_CACHE.cache[code] = out

    return out


def get_splits_with_words(g: str, C: List[str]) -> Dict[str, List[str]]:
    """Get the splits as a dict. Key is guess, value is the split corresponding to guess.

    Args:
        g (str): _description_
        C (List[str]): _description_

    Returns:
        Dict[str, List[str]]: _description_
    """
    splits: Dict[str, List[str]] = {}
    for c in C:
        res = check(g, c)
        if res not in splits:
            splits[res] = []
        splits[res].append(c)
    return splits


def get_splits_with_count(g: str, C: List[str]) -> Dict[str, int]:
    """Get the splits as a dict. Key is guess, value is the size of the split.

    Args:
        g (str): _description_
        C (List[str]): _description_

    Returns:
        Dict[str, List[str]]: _description_
    """
    splits: Dict[str, int] = {}
    for c in C:
        res = check(g, c)
        splits[res] = splits.get(res, 0) + 1
    return splits


def max_splits(G: List[str], C: List[str]) -> int:
    return max(len(get_splits_with_count(g, C)) for g in G)


def soft_match(guess: str, res: str, cand: str) -> bool:
    used = [False] * len(guess)
    for i, (g, r, c) in enumerate(zip(guess, res, cand)):
        if r == "2":
            if g != c:
                return False
            used[i] = True

    for i, (g, r) in enumerate(zip(guess, res)):
        if r == "1":
            for j, c in enumerate(cand):
                if used[j]:
                    continue
                if c == g:
                    used[j] = True
                    break
            else:
                return False

    return True


def soft_filter_possible(g: str, r: str, C: List[str]) -> List[str]:
    return [c for c in C if soft_match(g, r, c)]


def no_filter_possible(g: str, r: str, C: List[str]) -> List[str]:
    return C


def soft_filter_multiple(history: List[Tuple[str, str]], C: List[str]) -> List[str]:
    for g, r in history:
        C = soft_filter_possible(g, r, C)
    return C


def encode(subset: List[str], superset: List[str]) -> int:
    if len(subset) == len(superset):
        return 0
    t = 0
    for c in subset:
        t |= 1 << (len(superset) - superset.index(c) - 1)
    return t


def is_useful(guess, C):
    if len(C) <= 1:
        return guess in C
    res = check(guess, C[0])
    for c in C[1:]:
        if check(guess, c) != res:
            return True

    return False


def save_as_word_list(tree: Dict, file_name: str, secrets: List[str]):
    with open(file_name, "w") as g:
        for s in secrets:
            ans = []
            curr = tree
            while True:
                ans.append(curr["guess"])
                if curr["guess"] == s:
                    break
                res = check(curr["guess"], s)
                curr = curr["splits"][res]
            g.write(",".join(ans) + "\n")


def useful_guesses(G: List[str], C: List[str]) -> List[str]:
    if len(C) <= 1:
        return C.copy()
    return [g for g in G if is_useful(g, C)]


def sort_words(
    G: List[str],
    S: List[str],
    vals: List[Valuation],
    n: int = -1,
    show_progress: bool = False,
) -> List[str]:
    if n >= len(G) or n == -1:
        return G
    scores = sorted(
        [
            (tuple((v(g, S) for v in vals)), g)
            for g in tqdm(G, disable=not show_progress, colour="red", desc="Sorting")
        ]
    )
    return [g for _, g in scores[:n]]
