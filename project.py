import random
import pygame

# =========================
# 기본 설정
# =========================
MAP_WIDTH = 30
MAP_HEIGHT = 18
TILE_SIZE = 32

SCREEN_WIDTH = MAP_WIDTH * TILE_SIZE
SCREEN_HEIGHT = MAP_HEIGHT * TILE_SIZE

WALL = "#"
FLOOR = "."
PLAYER = "P"
EXIT = "E"
ENEMY = "M"
ITEM = "*"

COLORS = {
    WALL: (45, 45, 55),
    FLOOR: (185, 175, 145),
    PLAYER: (70, 130, 255),
    EXIT: (70, 210, 100),
    ENEMY: (220, 65, 65),
    ITEM: (245, 210, 70),
    "GRID": (35, 35, 40),
    "BACKGROUND": (20, 20, 25),
}


# =========================
# 맵 생성 함수
# =========================
def create_empty_map():
    return [[WALL for _ in range(MAP_WIDTH)] for _ in range(MAP_HEIGHT)]


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


def generate_dungeon(room_count=8):
    dungeon = create_empty_map()
    rooms = []

    for _ in range(room_count):
        room_w = random.randint(4, 8)
        room_h = random.randint(3, 5)

        x = random.randint(1, MAP_WIDTH - room_w - 2)
        y = random.randint(1, MAP_HEIGHT - room_h - 2)

        create_room(dungeon, x, y, room_w, room_h)

        center_x = x + room_w // 2
        center_y = y + room_h // 2

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
        x = random.randint(1, MAP_WIDTH - 2)
        y = random.randint(1, MAP_HEIGHT - 2)

        if dungeon[y][x] == FLOOR:
            dungeon[y][x] = symbol
            return x, y


# =========================
# pygame 그리기 함수
# =========================
def draw_map(screen, dungeon):
    screen.fill(COLORS["BACKGROUND"])

    for y in range(MAP_HEIGHT):
        for x in range(MAP_WIDTH):
            cell = dungeon[y][x]
            rect = pygame.Rect(
                x * TILE_SIZE,
                y * TILE_SIZE,
                TILE_SIZE,
                TILE_SIZE
            )

            if cell == WALL:
                pygame.draw.rect(screen, COLORS[WALL], rect)
            else:
                pygame.draw.rect(screen, COLORS[FLOOR], rect)

                if cell == PLAYER:
                    pygame.draw.circle(
                        screen,
                        COLORS[PLAYER],
                        rect.center,
                        TILE_SIZE // 3
                    )

                elif cell == EXIT:
                    exit_rect = rect.inflate(-10, -10)
                    pygame.draw.rect(screen, COLORS[EXIT], exit_rect)

                elif cell == ENEMY:
                    pygame.draw.circle(
                        screen,
                        COLORS[ENEMY],
                        rect.center,
                        TILE_SIZE // 3
                    )

                elif cell == ITEM:
                    pygame.draw.circle(
                        screen,
                        COLORS[ITEM],
                        rect.center,
                        TILE_SIZE // 5
                    )

            pygame.draw.rect(screen, COLORS["GRID"], rect, 1)


def create_game_map():
    dungeon, rooms = generate_dungeon()

    player_x, player_y = rooms[0]
    exit_x, exit_y = rooms[-1]

    dungeon[player_y][player_x] = PLAYER
    dungeon[exit_y][exit_x] = EXIT

    for _ in range(6):
        place_object(dungeon, ENEMY)

    for _ in range(5):
        place_object(dungeon, ITEM)

    return dungeon


# =========================
# main
# =========================
def main():
    pygame.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("DSA Dungeon Map Generator")

    clock = pygame.time.Clock()
    dungeon = create_game_map()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # R 누르면 새 맵 생성
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    dungeon = create_game_map()

        draw_map(screen, dungeon)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()