from dataclasses import dataclass, field

from inventory import Inventory


@dataclass
class Player:
    name: str = "Player"
    x: int = 1
    y: int = 1
    hp: int = 150
    max_hp: int = 150
    base_atk: int = 20
    atk: int = 20
    base_defense: int = 5
    defense: int = 5
    weapon_name: str = "Training Sword"
    weapon_power: int = 0
    armor_name: str = "Cloth Armor"
    armor_power: int = 0
    xp: int = 0
    level: int = 1
    kills: int = 0
    undo_used: int = 0
    inventory: Inventory = field(default_factory=Inventory)

    def gain_xp(self, amount: int) -> str:
        self.xp += amount
        needed = self.level * 30
        if self.xp >= needed:
            self.xp -= needed
            self.level += 1
            self.max_hp += 25
            self.hp = self.max_hp
            self.base_atk += 5
            self.atk = self.base_atk + self.weapon_power
            return f"Level up! You are now Lv.{self.level}."
        return f"Gained {amount} XP."

    def equip_weapon(self, item) -> str:
        self.weapon_name = item.name
        self.weapon_power = item.power
        self.atk = self.base_atk + self.weapon_power
        return f"Equipped {item.name}. ATK is now {self.atk}."

    def equip_armor(self, item) -> str:
        self.armor_name = item.name
        self.defense = self.base_defense + item.power
        self.armor_power = item.power
        return f"Equipped {item.name}. DEF is now {self.defense}."
