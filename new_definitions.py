from dataclasses import dataclass, field
from typing import Callable, Dict, Generic, List, Tuple, TypeVar, Union

INFINITY = 99999999
CACHE_LIMIT = 10_000
DEBUG_LEVEL = 2
BOUND_DEBUG_LEVEL = 2
MAX_BOUND_DEPTH = 7


Val = Union[int, float, Tuple["Val", ...]]
Valuation = Callable[[str, List[str]], Val]
Score = TypeVar("Score")
Guess = str
Secret = str
Response = str
Encoding = Tuple[int, int]

DEBUG_COLOURS = ["blue", "green", "red"]
N_DEBUG_COLOURS = len(DEBUG_COLOURS)

BORDER = "--------------"


@dataclass
class Tree(Generic[Score]):
    guess: str
    score: Score
    splits: Dict[str, "Tree"] = field(default_factory=dict)
    n_remaining: int = 0
