import time

from settings import MAX_UNDO
from undo import UndoStack


class TurnManager:
    def __init__(self, game) -> None:
        self.game = game
        self.undo = UndoStack(MAX_UNDO)
        self.started_at = time.time()
        self.logs = ["[1] Escape the dungeon!"]

    def snapshot(self):
        return {
            "player": self.game.player,
            "dungeon": self.game.dungeon,
            "floor": self.game.floor_no,
            "logs": list(self.logs),
        }

    def restore(self, state) -> None:
        self.game.player = state["player"]
        self.game.dungeon = state["dungeon"]
        self.game.floor_no = state["floor"]
        self.logs = state["logs"]

    def add_log(self, message: str) -> None:
        self.logs.append(message)
        self.logs = self.logs[-7:]

    def player_action(self, command: str) -> bool:
        player = self.game.player
        dungeon = self.game.dungeon
        moves = {"w": (0, -1), "s": (0, 1), "a": (-1, 0), "d": (1, 0)}

        if command == "attack":
            self.undo.push(self.snapshot())
            if self.attack_adjacent_enemy():
                self.enemy_turn()
            return True

        if command in moves:
            self.undo.push(self.snapshot())
            dx, dy = moves[command]
            nx, ny = player.x + dx, player.y + dy
            enemy = dungeon.enemy_at(nx, ny)
            if enemy:
                damage = max(1, player.atk - enemy.defense)
                enemy.hp -= damage
                self.add_log(f"You hit {enemy.name} for {damage}.")
                if not enemy.alive:
                    player.kills += 1
                    self.add_log(f"{enemy.name} defeated. {player.gain_xp(enemy.xp)}")
                    dungeon.remove_dead()
            elif dungeon.is_walkable(nx, ny):
                player.x, player.y = nx, ny
                if (nx, ny) in dungeon.items:
                    item = dungeon.items.pop((nx, ny))
                    player.inventory.add(item)
                    self.add_log(f"Picked up {item.name}.")
                if (nx, ny) == dungeon.stairs:
                    self.game.next_floor()
                    if self.game.finished:
                        return True
            else:
                self.add_log("A wall blocks the way.")
            self.enemy_turn()
            return True

        if command == "u":
            state = self.undo.pop()
            if state:
                self.restore(state)
                self.game.player.undo_used += 1
                self.add_log("Undo restored the previous turn.")
            else:
                self.add_log("No undo state available.")
            return True

        if command.startswith("i"):
            parts = command.split()
            if len(parts) == 2 and parts[1].isdigit():
                self.undo.push(self.snapshot())
                self.add_log(player.inventory.use(int(parts[1]) - 1, player))
                self.enemy_turn()
            else:
                labels = player.inventory.labels() or ["Inventory is empty."]
                for label in labels:
                    self.add_log(label)
            return True

        if command == "r":
            self.add_log("Restarting run.")
            self.game.reset()
            return True

        return False

    def attack_adjacent_enemy(self) -> bool:
        player = self.game.player
        dungeon = self.game.dungeon
        targets = []
        for enemy in dungeon.enemies:
            if enemy.alive and dungeon.distance((player.x, player.y), (enemy.x, enemy.y)) == 1:
                targets.append(enemy)
        if not targets:
            self.add_log("No enemy in melee range.")
            return False
        enemy = min(targets, key=lambda target: target.hp)
        damage = max(1, player.atk - enemy.defense)
        enemy.hp -= damage
        self.add_log(f"{player.name} attacks {enemy.name} for {damage}.")
        if not enemy.alive:
            player.kills += 1
            self.add_log(f"{enemy.name} defeated. {player.gain_xp(enemy.xp)}")
            dungeon.remove_dead()
        return True

    def enemy_turn(self) -> None:
        player = self.game.player
        dungeon = self.game.dungeon
        occupied = {(enemy.x, enemy.y) for enemy in dungeon.enemies if enemy.alive}
        for enemy in list(dungeon.enemies):
            if not enemy.alive:
                continue
            dist = dungeon.distance((enemy.x, enemy.y), (player.x, player.y))
            if dist == 1 or (enemy.ai in ("ranged", "boss") and dist <= 3):
                damage = max(1, enemy.atk - player.defense)
                player.hp -= damage
                self.add_log(f"{enemy.name} attacks for {damage}.")
                continue
            if dist <= 8 or enemy.ai == "boss":
                occupied.discard((enemy.x, enemy.y))
                step = dungeon.next_step_toward((enemy.x, enemy.y), (player.x, player.y), occupied)
                if step != (player.x, player.y):
                    enemy.x, enemy.y = step
                occupied.add((enemy.x, enemy.y))
