import random
from collections import deque

from enemy import ENEMY_TYPES, Enemy
from item import ITEM_POOL
from settings import FLOOR, HEIGHT, STAIRS, WALL, WIDTH


class Dungeon:
    def __init__(self, floor_no: int) -> None:
        self.floor_no = floor_no
        self.grid = [[WALL for _ in range(WIDTH)] for _ in range(HEIGHT)]
        self.enemies = []
        self.items = {}
        self.stairs = (WIDTH - 2, HEIGHT - 2)
        self.generate()

    def generate(self) -> None:
        rooms = []
        for _ in range(9):
            w, h = random.randint(5, 9), random.randint(4, 7)
            x = random.randint(1, WIDTH - w - 2)
            y = random.randint(1, HEIGHT - h - 2)
            room = (x, y, w, h)
            rooms.append(room)
            for yy in range(y, y + h):
                for xx in range(x, x + w):
                    self.grid[yy][xx] = FLOOR

        centers = [(x + w // 2, y + h // 2) for x, y, w, h in rooms]
        for (x1, y1), (x2, y2) in zip(centers, centers[1:]):
            for x in range(min(x1, x2), max(x1, x2) + 1):
                self.grid[y1][x] = FLOOR
            for y in range(min(y1, y2), max(y1, y2) + 1):
                self.grid[y][x2] = FLOOR

        self.stairs = centers[-1]
        sx, sy = self.stairs
        self.grid[sy][sx] = STAIRS
        self._place_entities(centers[0])

    def _open_cells(self):
        cells = []
        for y, row in enumerate(self.grid):
            for x, tile in enumerate(row):
                if tile in (FLOOR, STAIRS):
                    cells.append((x, y))
        return cells

    def _place_entities(self, start) -> None:
        cells = [cell for cell in self._open_cells() if self.distance(cell, start) > 6]
        random.shuffle(cells)
        enemy_count = 5 + self.floor_no * 2
        for i in range(enemy_count):
            if self.floor_no == 1:
                choices = ENEMY_TYPES[:3]
            elif self.floor_no == 2:
                choices = ENEMY_TYPES[:4]
            else:
                choices = ENEMY_TYPES
            name, hp, atk, defense, xp, icon, ai, difficulty = random.choice(choices)
            if self.floor_no < 3 and name == "Dragon":
                name, hp, atk, defense, xp, icon, ai, difficulty = random.choice(ENEMY_TYPES[:4])
            x, y = cells.pop()
            scale = 1 + (self.floor_no - 1) * 0.25
            max_hp = int(hp * scale)
            self.enemies.append(Enemy(name, x, y, max_hp, max_hp, int(atk * scale), defense, xp, icon, ai, difficulty))

        for _ in range(6):
            x, y = cells.pop()
            self.items[(x, y)] = random.choice(ITEM_POOL)

    def is_walkable(self, x: int, y: int) -> bool:
        return 0 <= x < WIDTH and 0 <= y < HEIGHT and self.grid[y][x] in (FLOOR, STAIRS)

    def enemy_at(self, x: int, y: int):
        for enemy in self.enemies:
            if enemy.alive and enemy.x == x and enemy.y == y:
                return enemy
        return None

    def remove_dead(self) -> None:
        self.enemies = [enemy for enemy in self.enemies if enemy.alive]

    @staticmethod
    def distance(a, b) -> int:
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def next_step_toward(self, start, goal, blocked):
        queue = deque([(start, [])])
        seen = {start}
        while queue:
            (x, y), path = queue.popleft()
            if (x, y) == goal:
                return path[0] if path else start
            for dx, dy in ((0, -1), (0, 1), (-1, 0), (1, 0)):
                nx, ny = x + dx, y + dy
                if (nx, ny) in seen or (nx, ny) in blocked:
                    continue
                if self.is_walkable(nx, ny):
                    seen.add((nx, ny))
                    queue.append(((nx, ny), path + [(nx, ny)]))
        return start
