def move_enemies(dungeon, player_x, player_y, WALL, FLOOR, PLAYER, ENEMY, EXIT, ITEM):
    enemies = []

    # 현재 적 위치 찾기
    for y in range(len(dungeon)):
        for x in range(len(dungeon[0])):
            if dungeon[y][x] == ENEMY:
                enemies.append((x, y))

    for enemy_x, enemy_y in enemies:
        dx = 0
        dy = 0

        # x 방향으로 플레이어에게 가까워지기
        if player_x > enemy_x:
            dx = 1
        elif player_x < enemy_x:
            dx = -1

        # x 방향 이동이 막혀 있으면 y 방향 시도
        new_x = enemy_x + dx
        new_y = enemy_y

        if dungeon[new_y][new_x] in [FLOOR, PLAYER]:
            dungeon[enemy_y][enemy_x] = FLOOR
            dungeon[new_y][new_x] = ENEMY

            if dungeon[new_y][new_x] == PLAYER:
                print("적에게 잡혔습니다!")

        else:
            if player_y > enemy_y:
                dy = 1
            elif player_y < enemy_y:
                dy = -1

            new_x = enemy_x
            new_y = enemy_y + dy

            if dungeon[new_y][new_x] in [FLOOR, PLAYER]:
                dungeon[enemy_y][enemy_x] = FLOOR
                dungeon[new_y][new_x] = ENEMY

                if dungeon[new_y][new_x] == PLAYER:
                    print("적에게 잡혔습니다!")