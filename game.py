import random
import time

from dungeon import Dungeon
from leaderboard import Leaderboard, calculate_score
from player import Player
from settings import FLOORS
from turn import TurnManager


class Game:
    def __init__(self) -> None:
        self.max_floors = FLOORS
        self.player_name = "Player"
        self.reset()

    def reset(self) -> None:
        random.seed()
        self.finished = False
        self.won = False
        self.final_score = 0
        self.leaderboard_rows = []
        self.floor_no = 1
        self.player = Player(name=self.player_name)
        self.dungeon = Dungeon(self.floor_no)
        self._place_player()
        self.turn = TurnManager(self)

    def _place_player(self) -> None:
        self.player.x, self.player.y = self.dungeon.start

    def next_floor(self) -> None:
        if self.floor_no >= self.max_floors:
            self.finish(True)
            return
        self.floor_no += 1
        self.dungeon = Dungeon(self.floor_no)
        self._place_player()
        self.turn.add_log(f"Descended to floor {self.floor_no}.")

    def finish(self, won: bool) -> None:
        if self.finished:
            return
        self.finished = True
        self.won = won
        elapsed = int(time.time() - self.turn.started_at)
        self.final_score = calculate_score(self.player, self.floor_no, elapsed)
        self.leaderboard_rows = Leaderboard().add(self.player.name, self.final_score, elapsed, self.player.undo_used)

    def set_player_name(self, name: str) -> None:
        clean_name = name.strip()[:12] or "Player"
        self.player_name = clean_name
        self.player.name = clean_name

    def run(self) -> None:
        from pygame_ui import run_pygame

        run_pygame(self)
