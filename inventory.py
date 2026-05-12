class Inventory:
    def __init__(self) -> None:
        self.items = []

    def add(self, item) -> None:
        self.items.append(item)

    def use(self, index, player):
        if index < 0 or index >= len(self.items):
            return "Invalid inventory slot."

        item = self.items.pop(index)
        if item.kind == "heal":
            before = player.hp
            player.hp = min(player.max_hp, player.hp + item.power)
            return f"Used {item.name}: HP {before}->{player.hp}."
        if item.kind == "weapon":
            return player.equip_weapon(item)
        if item.kind == "armor":
            return player.equip_armor(item)
        return f"Used {item.name}."

    def labels(self):
        return [f"{i + 1}. {item.label()}" for i, item in enumerate(self.items)]
