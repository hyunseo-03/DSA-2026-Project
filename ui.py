import os

from settings import FLOOR, HEIGHT, ITEM_ICON, PLAYER_ICON, STAIRS, WALL, WIDTH


def clear() -> None:
    os.system("cls" if os.name == "nt" else "clear")


def hp_bar(current: int, maximum: int, width: int = 20) -> str:
    filled = int(width * max(0, current) / maximum)
    return "[" + "#" * filled + "-" * (width - filled) + "]"


def render(game) -> None:
    clear()
    player = game.player
    dungeon = game.dungeon
    enemies = {(enemy.x, enemy.y): enemy for enemy in dungeon.enemies if enemy.alive}

    print("== DUNGEON CRAWLER RPG ==")
    print(f"Floor {game.floor_no}/{game.max_floors}  HP {player.hp}/{player.max_hp} {hp_bar(player.hp, player.max_hp)}")
    print(f"Lv.{player.level} XP:{player.xp}/{player.level * 30}  ATK:{player.atk} DEF:{player.defense}  Kills:{player.kills}")
    print(f"Undo used:{player.undo_used}  Undo left:{len(game.turn.undo)}")
    print()

    for y in range(HEIGHT):
        line = []
        for x in range(WIDTH):
            if player.x == x and player.y == y:
                line.append(PLAYER_ICON)
            elif (x, y) in enemies:
                line.append(enemies[(x, y)].icon)
            elif (x, y) in dungeon.items:
                line.append(ITEM_ICON)
            else:
                tile = dungeon.grid[y][x]
                if tile == WALL:
                    line.append("#")
                elif tile == STAIRS:
                    line.append(">")
                elif tile == FLOOR:
                    line.append(".")
                else:
                    line.append(tile)
        print("".join(line))

    print()
    print("[Inventory]")
    labels = player.inventory.labels()
    print("  " + (" | ".join(labels) if labels else "empty"))
    print()
    for log in game.turn.logs:
        print(log)
    print()
    print("WASD: move/attack  i: inventory  i N: use item  u: undo  r: restart  q: quit")


def render_leaderboard(rows) -> None:
    clear()
    print("== LEADERBOARD ==")
    print(f"{'Rank':<6}{'Name':<14}{'Score':<10}{'Time':<8}{'Undo'}")
    for i, row in enumerate(rows, 1):
        minute, second = divmod(row["time"], 60)
        print(f"{i:<6}{row['name']:<14}{row['score']:<10}{minute:02d}:{second:02d}   {row['undo']}")
