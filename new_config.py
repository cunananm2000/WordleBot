from dataclasses import dataclass
from typing import Dict, List, Optional, Union

from tqdm import tqdm

from new_definitions import INFINITY
from new_utils import get_splits_with_count, read_from_file


@dataclass
class Game:
    game_name: str
    guesses: List[str]
    secrets: List[str]
    r_star: str
    max_splits: Optional[int] = None
    upper_bound: Optional[int] = None

    @staticmethod
    def from_game_name(game_name: str) -> "Game":
        """Generate config object from a game name

        Args:
            game_name (str):
        """

        configs: Dict[str, Dict[str, Union[str, int]]] = {
            "newWordle": {
                "guess_file": "wordLists/newWordleGuesses.txt",
                "secret_file": "wordLists/newWordleAnswers.txt",
                "r_star": "22222",
            },
            "newerWordle": {
                "guess_file": "wordLists/newerWordleGuesses.txt",
                "secret_file": "wordLists/newerWordleAnswers.txt",
                "r_star": "22222",
                "max_splits": 150,
                "upper_bound": 7883,
            },
            "oldWordle": {
                "guess_file": "wordLists/oldWordleGuesses.txt",
                "secret_file": "wordLists/oldWordleAnswers.txt",
                "r_star": "22222",
                "max_splits": 150,
            },
            "primel": {
                "guess_file": "wordLists/primelWords.txt",
                "secret_file": "wordLists/primelWords.txt",
                "r_star": "22222",
            },
            "mininerdle": {
                "guess_file": "wordLists/mininerdleWords.txt",
                "secret_file": "wordLists/mininerdleWords.txt",
                "r_star": "222222",
            },
            "bardle": {
                "guess_file": "wordLists/bardleGuesses.txt",
                "secret_file": "wordLists/bardleAnswers.txt",
                "r_star": "22222",
            },
            "mathler": {
                "guess_file": "wordLists/mathlerWords.txt",
                "secret_file": "wordLists/mathlerWords.txt",
                "r_star": "222222",
            },
            "nerdle": {
                "guess_file": "wordLists/nerdleWords.txt",
                "secret_file": "wordLists/nerdleWords.txt",
                "r_star": "22222222",
            },
            "ffxivrdle": {
                "guess_file": "wordLists/ffxivrdleGuesses.txt",
                "secret_file": "wordLists/ffxivrdleAnswers.txt",
                "r_star": "22222",
            },
        }

        config_dict = configs[game_name]

        game = Game(
            game_name=game_name,
            guesses=read_from_file(config_dict["guess_file"]),
            secrets=read_from_file(config_dict["secret_file"]),
            r_star=config_dict["r_star"],
            upper_bound=config_dict.get("upper_bound", INFINITY),
        )

        max_splits = config_dict.get("max_splits", -1)
        if max_splits == -1:
            max_splits = max(
                len(get_splits_with_count(g, game.secrets))
                for g in tqdm(game.guesses, desc="TEMPORARY max_splits")
            )

        game.max_splits = max_splits

        return game
