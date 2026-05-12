import pygame

from settings import FLOOR, HEIGHT, STAIRS, WALL, WIDTH


TILE = 32
PANEL_WIDTH = 330
LOG_HEIGHT = 130
SCREEN_WIDTH = WIDTH * TILE + PANEL_WIDTH
SCREEN_HEIGHT = HEIGHT * TILE + LOG_HEIGHT
FPS = 60

COLORS = {
    "bg": (8, 10, 18),
    "panel": (14, 16, 28),
    "grid": (30, 34, 50),
    "floor": (18, 20, 32),
    "wall": (67, 73, 96),
    "wall_dark": (52, 58, 80),
    "stairs": (250, 210, 64),
    "text": (232, 236, 245),
    "muted": (142, 150, 170),
    "cyan": (28, 220, 220),
    "yellow": (255, 215, 40),
    "red": (255, 52, 74),
    "green": (80, 225, 110),
    "blue": (72, 145, 255),
    "orange": (255, 150, 35),
    "purple": (155, 82, 255),
}

ENEMY_COLORS = {
    "s": (70, 225, 105),
    "g": (90, 210, 90),
    "o": (255, 78, 54),
    "w": (135, 76, 215),
    "D": (255, 72, 72),
}

ITEM_COLORS = {
    "heal": (255, 70, 95),
    "weapon": (255, 210, 70),
    "armor": (105, 170, 255),
}


def draw_text(surface, font, text, x, y, color=None):
    image = font.render(str(text), True, color or COLORS["text"])
    surface.blit(image, (x, y))


def draw_bar(surface, x, y, width, height, value, maximum, color):
    pygame.draw.rect(surface, (58, 60, 72), (x, y, width, height), border_radius=4)
    ratio = max(0, min(1, value / maximum))
    pygame.draw.rect(surface, color, (x, y, int(width * ratio), height), border_radius=4)


def draw_map(surface, game, font):
    dungeon = game.dungeon
    player = game.player
    enemies = {(enemy.x, enemy.y): enemy for enemy in dungeon.enemies if enemy.alive}

    for y in range(HEIGHT):
        for x in range(WIDTH):
            rect = pygame.Rect(x * TILE, y * TILE, TILE, TILE)
            tile = dungeon.grid[y][x]
            if tile == WALL:
                pygame.draw.rect(surface, COLORS["wall"], rect)
                pygame.draw.rect(surface, COLORS["wall_dark"], rect.inflate(-6, -6), 1)
            else:
                pygame.draw.rect(surface, COLORS["floor"], rect)
                pygame.draw.rect(surface, COLORS["grid"], rect, 1)
                if tile == STAIRS:
                    pygame.draw.polygon(
                        surface,
                        COLORS["stairs"],
                        [(rect.centerx, rect.top + 6), (rect.right - 7, rect.centery), (rect.centerx, rect.bottom - 6), (rect.left + 7, rect.centery)],
                    )

            if (x, y) in dungeon.items:
                item = dungeon.items[(x, y)]
                pygame.draw.circle(surface, ITEM_COLORS.get(item.kind, COLORS["cyan"]), rect.center, 7)
                draw_text(surface, font, item.icon, rect.left + 11, rect.top + 7, COLORS["bg"])

            if (x, y) in enemies:
                enemy = enemies[(x, y)]
                color = ENEMY_COLORS.get(enemy.icon, COLORS["red"])
                pygame.draw.circle(surface, color, rect.center, 11)
                hp_width = int(18 * max(0, enemy.hp) / enemy.max_hp)
                pygame.draw.rect(surface, (62, 62, 72), (rect.left + 7, rect.top + 4, 18, 4))
                pygame.draw.rect(surface, COLORS["green"], (rect.left + 7, rect.top + 4, hp_width, 4))
                draw_text(surface, font, enemy.icon.upper(), rect.left + 11, rect.top + 8, COLORS["bg"])

            if player.x == x and player.y == y:
                pygame.draw.circle(surface, COLORS["blue"], rect.center, 12)
                pygame.draw.polygon(
                    surface,
                    COLORS["yellow"],
                    [(rect.centerx, rect.top + 4), (rect.centerx - 5, rect.top + 12), (rect.centerx + 5, rect.top + 12)],
                )
                draw_text(surface, font, "@", rect.left + 10, rect.top + 7, COLORS["text"])


def draw_panel(surface, game, font, small):
    x = WIDTH * TILE
    player = game.player
    pygame.draw.rect(surface, COLORS["panel"], (x, 0, PANEL_WIDTH, SCREEN_HEIGHT))
    pygame.draw.line(surface, (52, 56, 84), (x, 0), (x, SCREEN_HEIGHT), 2)

    draw_text(surface, font, "== DUNGEON CRAWLER ==", x + 18, 18, COLORS["cyan"])
    draw_text(surface, font, player.name, x + 18, 50, COLORS["text"])
    draw_text(surface, font, f"Floor: {game.floor_no}/{game.max_floors}", x + 18, 78, COLORS["yellow"])
    draw_text(surface, font, f"Level: {player.level}  XP: {player.xp}/{player.level * 30}", x + 18, 106, COLORS["green"])

    draw_text(surface, small, f"HP: {player.hp}/{player.max_hp}", x + 18, 141, COLORS["red"])
    draw_bar(surface, x + 18, 164, PANEL_WIDTH - 36, 16, player.hp, player.max_hp, COLORS["red"])

    draw_text(surface, small, f"ATK:{player.atk}  DEF:{player.defense}  Kills:{player.kills}", x + 18, 198, COLORS["orange"])
    draw_text(surface, small, f"Weapon: {player.weapon_name}", x + 18, 226, COLORS["yellow"])
    draw_text(surface, small, f"Undo used:{player.undo_used}  states:{len(game.turn.undo)}", x + 18, 254, COLORS["green"])

    draw_text(surface, font, "[Inventory]", x + 18, 296, COLORS["yellow"])
    labels = player.inventory.labels() or ["empty"]
    for i, label in enumerate(labels[:6]):
        draw_text(surface, small, label, x + 18, 328 + i * 23, COLORS["text"])

    controls = ["WASD / Arrows: move", "Space/F: attack nearby enemy", "I: inventory  1-9: use/equip", "U: undo   R: restart", "Q or ESC: quit"]
    base = SCREEN_HEIGHT - 138
    for i, line in enumerate(controls):
        draw_text(surface, small, line, x + 18, base + i * 24, COLORS["muted"])


def draw_logs(surface, game, small):
    y = HEIGHT * TILE
    pygame.draw.rect(surface, (5, 6, 10), (0, y, WIDTH * TILE, LOG_HEIGHT))
    pygame.draw.line(surface, (52, 56, 84), (0, y), (WIDTH * TILE, y), 2)
    for i, log in enumerate(game.turn.logs[-5:]):
        color = COLORS["yellow"] if i == len(game.turn.logs[-5:]) - 1 else COLORS["muted"]
        draw_text(surface, small, log, 14, y + 14 + i * 23, color)


def draw_end_screen(surface, game, font, small):
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 210))
    surface.blit(overlay, (0, 0))
    title = "YOU ESCAPED!" if game.won else "GAME OVER"
    draw_text(surface, font, title, 56, 54, COLORS["yellow"] if game.won else COLORS["red"])
    draw_text(surface, font, f"Final score: {game.final_score}", 56, 92, COLORS["cyan"])
    draw_text(surface, small, "Leaderboard", 56, 146, COLORS["text"])
    draw_text(surface, small, f"{'Rank':<6}{'Name':<12}{'Score':<10}{'Time':<8}{'Undo'}", 56, 178, COLORS["muted"])
    for i, row in enumerate(game.leaderboard_rows[:8], 1):
        minute, second = divmod(row["time"], 60)
        line = f"{i:<6}{row['name']:<12}{row['score']:<10}{minute:02d}:{second:02d}   {row['undo']}"
        draw_text(surface, small, line, 56, 206 + i * 28, COLORS["yellow"] if i == 1 else COLORS["text"])
    draw_text(surface, small, "R: restart   Q/ESC: quit", 56, SCREEN_HEIGHT - 72, COLORS["muted"])


def draw_start_screen(surface, name_text, font, small):
    surface.fill(COLORS["bg"])
    draw_text(surface, font, "DUNGEON CRAWLER RPG", 64, 92, COLORS["cyan"])
    draw_text(surface, small, "Enter your player name, then press Enter.", 64, 142, COLORS["muted"])
    box = pygame.Rect(64, 188, 420, 52)
    pygame.draw.rect(surface, COLORS["panel"], box, border_radius=6)
    pygame.draw.rect(surface, COLORS["cyan"], box, 2, border_radius=6)
    shown = name_text if name_text else "Player"
    draw_text(surface, font, shown, box.x + 16, box.y + 14, COLORS["text"] if name_text else COLORS["muted"])
    draw_text(surface, small, "Backspace: delete   Enter: start", 64, 266, COLORS["yellow"])
    draw_text(surface, small, "Goal: clear 3 floors, collect weapons, defeat stronger enemies.", 64, 318, COLORS["text"])


def draw_inventory_overlay(surface, game, font, small):
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    surface.blit(overlay, (0, 0))
    box = pygame.Rect(70, 70, SCREEN_WIDTH - 140, SCREEN_HEIGHT - 140)
    pygame.draw.rect(surface, COLORS["panel"], box, border_radius=8)
    pygame.draw.rect(surface, COLORS["cyan"], box, 2, border_radius=8)
    draw_text(surface, font, "Inventory", box.x + 24, box.y + 22, COLORS["yellow"])
    draw_text(surface, small, "Press 1-9 to use or equip an item. Press I to close.", box.x + 24, box.y + 58, COLORS["muted"])
    labels = game.player.inventory.labels()
    if not labels:
        draw_text(surface, font, "Inventory is empty.", box.x + 24, box.y + 118, COLORS["text"])
    for i, label in enumerate(labels[:9]):
        draw_text(surface, font, label, box.x + 24, box.y + 112 + i * 34, COLORS["text"])
    draw_text(surface, small, f"Equipped weapon: {game.player.weapon_name} (+{game.player.weapon_power} ATK)", box.x + 24, box.bottom - 74, COLORS["orange"])
    draw_text(surface, small, f"Armor: {game.player.armor_name} (+{game.player.armor_power} DEF)", box.x + 24, box.bottom - 46, COLORS["blue"])


def handle_key(game, key):
    if key in (pygame.K_w, pygame.K_UP):
        return "w"
    if key in (pygame.K_s, pygame.K_DOWN):
        return "s"
    if key in (pygame.K_a, pygame.K_LEFT):
        return "a"
    if key in (pygame.K_d, pygame.K_RIGHT):
        return "d"
    if key == pygame.K_u:
        return "u"
    if key == pygame.K_r:
        return "r"
    if key in (pygame.K_SPACE, pygame.K_f):
        return "attack"
    if pygame.K_1 <= key <= pygame.K_9:
        return f"i {key - pygame.K_1 + 1}"
    if key == pygame.K_i:
        return "i"
    return None


def run_pygame(game):
    pygame.init()
    pygame.display.set_caption("Dungeon Crawler RPG - DSA Project")
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("menlo,consolas,courier", 20)
    small = pygame.font.SysFont("menlo,consolas,courier", 16)
    entering_name = True
    name_text = ""
    show_inventory = False

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if entering_name:
                    if event.key == pygame.K_RETURN:
                        game.set_player_name(name_text)
                        entering_name = False
                    elif event.key == pygame.K_BACKSPACE:
                        name_text = name_text[:-1]
                    elif event.unicode and event.unicode.isprintable() and len(name_text) < 12:
                        name_text += event.unicode
                elif event.key in (pygame.K_ESCAPE, pygame.K_q):
                    running = False
                elif game.finished and event.key == pygame.K_r:
                    game.reset()
                    entering_name = True
                    name_text = game.player_name
                    show_inventory = False
                elif not game.finished:
                    if event.key == pygame.K_i:
                        show_inventory = not show_inventory
                        if show_inventory:
                            game.turn.player_action("i")
                        continue
                    command = handle_key(game, event.key)
                    if command:
                        game.turn.player_action(command)
                        if command.startswith("i "):
                            show_inventory = True
                    else:
                        game.turn.add_log("Unknown command.")

        if not game.finished and game.player.hp <= 0:
            game.finish(False)

        if entering_name:
            draw_start_screen(screen, name_text, font, small)
        else:
            screen.fill(COLORS["bg"])
            draw_map(screen, game, small)
            draw_logs(screen, game, small)
            draw_panel(screen, game, font, small)
            if show_inventory and not game.finished:
                draw_inventory_overlay(screen, game, font, small)
            if game.finished:
                draw_end_screen(screen, game, font, small)
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
