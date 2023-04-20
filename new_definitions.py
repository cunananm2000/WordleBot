from typing import Callable, Set, Dict, Union

INFINITY = 99999999
CACHE_LIMIT = 10_000
DEBUG_LEVEL = 2

Valuation = Callable[[str, Set[str]], float]
Tree = Dict[str, Union[str, int, Dict]]
