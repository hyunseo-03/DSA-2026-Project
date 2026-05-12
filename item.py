from dataclasses import dataclass


@dataclass(frozen=True)
class Item:
    name: str
    kind: str
    power: int
    icon: str

    def label(self) -> str:
        if self.kind == "weapon":
            return f"[WEAPON] {self.name} ATK+{self.power}"
        if self.kind == "armor":
            return f"[ARMOR] {self.name} DEF+{self.power}"
        if self.kind == "heal":
            return f"[HEAL] {self.name} HP+{self.power}"
        return f"[{self.kind.upper()}] {self.name} +{self.power}"


ITEM_POOL = [
    Item("Healing Potion", "heal", 35, "!"),
    Item("Iron Shield", "armor", 3, "]"),
    Item("Steel Sword", "weapon", 7, "/"),
    Item("Flame Blade", "weapon", 13, "/"),
    Item("Power Crystal", "weapon", 5, "*"),
]
