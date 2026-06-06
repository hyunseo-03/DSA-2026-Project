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

- `main.py`: Entry point of the project. It creates a `Game` object and starts
  the game loop.
- `game.py`: Manages the main game state, including player setup, floor changes,
  game reset, win/loss handling, final score calculation, and leaderboard
  updates.
- `pygame_ui.py`: Handles the graphical interface using Pygame. It draws the
  dungeon map, player, enemies, items, inventory screen, start screen, end
  screen, status panel, and game log messages.
- `dungeon.py`: Generates the dungeon layout using a 2D grid. It creates rooms,
  connects them with corridors, places the player start point, enemies, items,
  and stairs, and includes BFS-based pathfinding support for enemy movement.
- `turn.py`: Handles turn-based gameplay logic. It processes player commands,
  movement, attacks, item usage, undo actions, enemy turns, combat results, and
  interactions with stairs or dungeon objects.
- `player.py`: Defines the player character. It stores player stats such as HP,
  attack, defense, level, XP, position, inventory, equipped weapon and armor,
  kill count, and undo usage count.
- `enemy.py`: Defines enemy data and enemy types. Each enemy has stats such as
  HP, attack, defense, XP reward, icon, name, and position in the dungeon.
- `item.py`: Defines collectible items such as healing potions, weapons, and
  armor. Items affect the player's HP, attack power, or defense when used or
  equipped.
- `inventory.py`: Manages the player's inventory as a list of items. It supports
  adding items, removing used items, checking inventory size, and displaying
  item labels in the UI.
- `undo.py`: Implements the undo system using a stack. Previous game states are
  saved so the player can restore an earlier turn.
- `leaderboard.py`: Calculates the final score and manages saved rankings. It
  reads and writes leaderboard data using the `leaderboard.json` file.
- `settings.py`: Stores shared game constants, including map width, map height,
  tile symbols, number of floors, undo limit, and leaderboard file name.
- `ui.py`: Contains an older terminal-based rendering system. The current game
  uses `pygame_ui.py`, but this file shows the original text-based display
  approach.
- `requirements.txt`: Lists external Python packages required to run the
  project. Currently, the main dependency is Pygame.
- `leaderboard.json`: Stores saved leaderboard records, including player names,
  scores, clear times, and undo counts.
