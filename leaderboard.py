import json
from pathlib import Path

from settings import LEADERBOARD_FILE


def calculate_score(player, floor_no: int, elapsed: int) -> int:
    time_penalty = max(0, elapsed - 180) * 10
    return player.xp * 10 + player.kills * 500 + floor_no * 3000 - player.undo_used * 50 - time_penalty


class Leaderboard:
    def __init__(self, path: str = LEADERBOARD_FILE) -> None:
        self.path = Path(path)

    def load(self):
        if not self.path.exists():
            return []
        try:
            return json.loads(self.path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return []

    def add(self, name: str, score: int, elapsed: int, undo_used: int):
        rows = self.load()
        rows.append({"name": name, "score": score, "time": elapsed, "undo": undo_used})
        rows.sort(key=lambda row: row["score"], reverse=True)
        rows = rows[:10]
        self.path.write_text(json.dumps(rows, indent=2), encoding="utf-8")
        return rows
