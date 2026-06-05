# Dungeon Crawler RPG - DSA Project

Python/Pygame dungeon crawler that demonstrates core data structure and
algorithm topics through gameplay.

## Install and Run

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python main.py
```

Or run the included setup script:

```bash
chmod +x setup_venv.sh
./setup_venv.sh
source .venv/bin/activate
python main.py
```

### Windows

```bat
py -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python main.py
```

Or run the included setup script:

```bat
setup_venv.bat
.venv\Scripts\activate
python main.py
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
