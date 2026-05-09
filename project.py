import random

WIDTH = 30
HEIGHT = 15

WALL = "#"
FLOOR = "."
PLAYER = "P"
EXIT = "E"
ENEMY = "M"
ITEM = "*"

def create_empty_map(width, height):
    return [[WALL for _ in range(width)] for _ in range(height)]

def create_room(dungeon, x, y, w, h):
    for row in range(y, y + h):
        for col in range(x, x + w):
            dungeon[row][col] = FLOOR

def create_h_tunnel(dungeon, x1, x2, y):
    for x in range(min(x1, x2), max(x1, x2) + 1):
        dungeon[y][x] = FLOOR

def create_v_tunnel(dungeon, y1, y2, x):
    for y in range(min(y1, y2), max(y1, y2) + 1):
        dungeon[y][x] = FLOOR

def generate_dungeon(width, height, room_count=6):
    dungeon = create_empty_map(width, height)
    rooms = []

    for _ in range(room_count):
        w = random.randint(4, 8)
        h = random.randint(3, 5)

        x = random.randint(1, width - w - 2)
        y = random.randint(1, height - h - 2)

        create_room(dungeon, x, y, w, h)

        center_x = x + w // 2
        center_y = y + h // 2

        if rooms:
            prev_x, prev_y = rooms[-1]

            if random.choice([True, False]):
                create_h_tunnel(dungeon, prev_x, center_x, prev_y)
                create_v_tunnel(dungeon, prev_y, center_y, center_x)
            else:
                create_v_tunnel(dungeon, prev_y, center_y, prev_x)
                create_h_tunnel(dungeon, prev_x, center_x, center_y)

        rooms.append((center_x, center_y))

    return dungeon, rooms

def place_object(dungeon, symbol):
    while True:
        y = random.randint(1, HEIGHT - 2)
        x = random.randint(1, WIDTH - 2)

        if dungeon[y][x] == FLOOR:
            dungeon[y][x] = symbol
            return x, y

def print_map(dungeon):
    for row in dungeon:
        print("".join(row))

def main():
    dungeon, rooms = generate_dungeon(WIDTH, HEIGHT)

    start_x, start_y = rooms[0]
    exit_x, exit_y = rooms[-1]

    dungeon[start_y][start_x] = PLAYER
    dungeon[exit_y][exit_x] = EXIT

    for _ in range(5):
        place_object(dungeon, ENEMY)

    for _ in range(4):
        place_object(dungeon, ITEM)

    print_map(dungeon)

if __name__ == "__main__":
    main()