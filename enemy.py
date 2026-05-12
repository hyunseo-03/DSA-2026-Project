from dataclasses import dataclass


@dataclass
class Enemy:
    name: str
    x: int
    y: int
    hp: int
    max_hp: int
    atk: int
    defense: int
    xp: int
    icon: str
    ai: str
    difficulty: str

    @property
    def alive(self) -> bool:
        return self.hp > 0


ENEMY_TYPES = [
    ("Slime", 30, 7, 1, 10, "s", "chase", "Easy"),
    ("Goblin", 38, 10, 2, 12, "g", "chase", "Easy"),
    ("Orc", 62, 14, 4, 18, "o", "chase", "Normal"),
    ("Wraith", 50, 17, 2, 24, "w", "ranged", "Hard"),
    ("Dragon", 115, 25, 6, 55, "D", "boss", "Boss"),
]
