# Dungeon Crawler RPG - DSA Project

Python standard-library dungeon crawler that demonstrates core data structure
and algorithm topics through gameplay.

## Install and Run

```bash
pip install -r requirements.txt
python3 main.py
```

## Controls

- Type your player name on the start screen, then press `Enter`
- `W`, `A`, `S`, `D` or arrow keys: move
- `Space` or `F`: attack an adjacent enemy
- `i`: open or close the inventory
- `1`-`9`: use or equip an inventory item
- `u`: undo previous turn
- `r`: restart
- `q`: quit

## DSA Features

- Dungeon map: 2D grid with random rooms and corridors
- Undo system: bounded stack of deep-copied game states
- Turn management: queue-based enemy turn processing after each player action
- Item inventory: list-backed inventory with consumable/equipment effects
- Weapons and armor: equipment changes attack and defense stats
- Enemy difficulty: easy, normal, hard, and boss enemies
- Enemy AI: BFS pathfinding and ranged/boss attack behavior
- Leaderboard: JSON-backed sorted ranking by calculated score

## Modules

- `main.py`: entry point
- `game.py`: game loop and floor progression
- `dungeon.py`: map generation, entity placement, BFS movement helper
- `turn.py`: command handling, undo, combat, enemy turns
- `player.py`, `enemy.py`, `item.py`, `inventory.py`: core game entities
- `leaderboard.py`: score calculation and persistence
- `ui.py`: terminal rendering
- `settings.py`: constants
