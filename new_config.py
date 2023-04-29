from dataclasses import dataclass
from typing import Dict, List

from tqdm import tqdm

from new_definitions import INFINITY, Guess, Secret
from new_utils import get_splits_with_count, read_from_file


@dataclass
class GameConfig:
    guess_file: str
    secret_file: str
    r_star: str
    max_splits: int = -1
    upper_bound: int = INFINITY


OldWordleConfig = GameConfig(
    guess_file="wordLists/oldWordleGuesses.txt",
    secret_file="wordLists/oldWordleAnswers.txt",
    r_star="22222",
    max_splits=150,
)

NewWordleConfig = GameConfig(
    guess_file="wordLists/newWordleGuesses.txt",
    secret_file="wordLists/newWordleAnswers.txt",
    r_star="22222",
)

NewerWordleConfig = GameConfig(
    guess_file="wordLists/newerWordleGuesses.txt",
    secret_file="wordLists/newerWordleAnswers.txt",
    r_star="22222",
    max_splits=150,
    upper_bound=7883,
)

PrimelConfig = GameConfig(
    guess_file="wordLists/primelWords.txt",
    secret_file="wordLists/primelWords.txt",
    r_star="22222",
)

FFXIVrdle = GameConfig(
    guess_file="wordLists/ffxivrdleGuesses.txt",
    secret_file="wordLists/ffxivrdleAnswers.txt",
    r_star="22222",
    max_splits=75,
    upper_bound=432,
)

NerdleConfig = GameConfig(
    guess_file="wordLists/nerdleWords.txt",
    secret_file="wordLists/nerdleWords.txt",
    r_star="22222222",
)

MiniNerdleConfig = GameConfig(
    guess_file="wordLists/mininerdleWords.txt",
    secret_file="wordLists/mininerdleWords.txt",
    r_star="222222",
    max_splits=72,
    upper_bound=544,
)

BardleConfig = GameConfig(
    guess_file="wordLists/bardleGuesses.txt",
    secret_file="wordLists/bardleAnswers.txt",
    r_star="22222",
    max_splits=72,
    upper_bound=455,
)


@dataclass
class Game:
    game_name: str
    guesses: List[Guess]
    secrets: List[Secret]
    r_star: str
    max_splits: int = -1
    upper_bound: int = INFINITY

    @staticmethod
    def from_game_name(game_name: str) -> "Game":
        """Generate config object from a game name

        Args:
            game_name (str):
        """

        configs: Dict[str, GameConfig] = {
            "old_wordle": OldWordleConfig,
            "new_wordle": NewWordleConfig,
            "newer_wordle": NewerWordleConfig,
            "primel": PrimelConfig,
            "ffxivrdle": FFXIVrdle,
            "nerdle": NerdleConfig,
            "mininerdle": MiniNerdleConfig,
            "bardle": BardleConfig,
        }

        game_config = configs[game_name]

        game = Game(
            game_name=game_name,
            guesses=read_from_file(game_config.guess_file),
            secrets=read_from_file(game_config.secret_file),
            r_star=game_config.r_star,
            upper_bound=game_config.upper_bound,
        )

        max_splits = game_config.max_splits
        if max_splits == -1:
            max_splits = max(
                len(get_splits_with_count(g, game.secrets))
                for g in tqdm(game.guesses, desc="TEMPORARY max_splits")
            )
            assert ValueError(f"Hard code this in future: {max_splits}")

        game.max_splits = max_splits

        return game
