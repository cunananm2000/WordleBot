from dataclasses import dataclass
from typing import Callable, Dict, Generic, List, TypeVar, Union

INFINITY = 99999999
CACHE_LIMIT = 10_000
DEBUG_LEVEL = 0
BOUND_DEBUG_LEVEL = 2
MAX_BOUND_DEPTH = 7


Numeric = Union[int, float]
Valuation = Callable[[str, List[str]], Numeric]
ScoreType = TypeVar("ScoreType")
# Tree = Dict[str, Union[str, int, Dict]]

DEBUG_COLOURS = ["blue", "green", "red"]
N_DEBUG_COLOURS = len(DEBUG_COLOURS)

BORDER = "--------------"


@dataclass
class Tree(Generic[ScoreType]):
    guess: str
    score: ScoreType
    splits: Dict[str, "Tree"]
