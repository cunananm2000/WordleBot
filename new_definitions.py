from typing import Callable, Dict, List, Union

INFINITY = 99999999
CACHE_LIMIT = 10_000
DEBUG_LEVEL = 0
BOUND_DEBUG_LEVEL = 2
MAX_BOUND_DEPTH = 7

Valuation = Callable[[str, List[str]], float]
Tree = Dict[str, Union[str, int, Dict]]


DEBUG_COLOURS = ["blue", "green", "red"]
N_DEBUG_COLOURS = len(DEBUG_COLOURS)

BORDER = "--------------"