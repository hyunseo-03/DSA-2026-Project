import time

from settings import MAX_UNDO
from undo import UndoStack


class TurnManager:
    def __init__(self, game) -> None:
        self.game = game
        self.undo = UndoStack(MAX_UNDO)
        self.started_at = time.time()
        self.logs = ["[1] Escape the dungeon!"]

    #현제 게임 상태를 저장
    def snapshot(self):
        return {
            "player": self.game.player,
            "dungeon": self.game.dungeon,
            "floor": self.game.floor_no,
            "logs": list(self.logs),
        }

    #저장된 게임 상태로 복원
    def restore(self, state) -> None:
        self.game.player = state["player"]
        self.game.dungeon = state["dungeon"]
        self.game.floor_no = state["floor"]
        self.logs = state["logs"]

    def add_log(self, message: str) -> None:
        self.logs.append(message)
        
        #로그가 너무 길어지지 않도록 최근 7개 로그만 유지
        self.logs = self.logs[-7:]

    #플레이어 행동 처리
    def player_action(self, command: str) -> bool:
        player = self.game.player
        dungeon = self.game.dungeon
        moves = {"w": (0, -1), "s": (0, 1), "a": (-1, 0), "d": (1, 0)}

        if command == "attack":
            #현재 상태 저장
            self.undo.push(self.snapshot())
            if self.attack_adjacent_enemy():
                #적이 공격당한 후 바로 적의 행동이 이어지도록 함
                self.enemy_turn()
            return True

        #이동 명령 처리
        if command in moves:
            #현재 상태 저장
            self.undo.push(self.snapshot())
            #방향 가져오기
            dx, dy = moves[command]
            #플레이어가 이동하려는 위치 계산
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

            #적이 없는 경우 이동 시도
            elif dungeon.is_walkable(nx, ny):
                player.x, player.y = nx, ny
                if (nx, ny) in dungeon.items:
                    item = dungeon.items.pop((nx, ny))
                    player.inventory.add(item)
                    self.add_log(f"Picked up {item.name}.")
                
                #계단 위치로 이동하면 다음 층으로 이동
                if (nx, ny) == dungeon.stairs:
                    self.game.next_floor()
                    if self.game.finished:
                        return True
            
            #벽이나 장애물이 있는 경우
            else:
                self.add_log("A wall blocks the way.")
            self.enemy_turn()
            return True

        if command == "u":
            #이전 상태로 되돌리기
            state = self.undo.pop()
            if state:
                self.restore(state)
                #플레이어가 되돌리기를 사용할 때마다 undo_used 카운터 증가
                self.game.player.undo_used += 1
                self.add_log("Undo restored the previous turn.")
            else:
                self.add_log("No undo state available.")
            return True

        #인벤토리 사용 명령 처리
        if command.startswith("i"):
            parts = command.split()
            #입력이 i 1처럼 두 단어 인지 확인 & 두 번째 단어가 숫자인지 확인
            if len(parts) == 2 and parts[1].isdigit():
                #현재 상태 저장
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
        #공격 가능한 적들을 담을 리스트
        targets = []

        for enemy in dungeon.enemies:
            if enemy.alive and dungeon.distance((player.x, player.y), (enemy.x, enemy.y)) == 1:
                targets.append(enemy)
        if not targets:
            self.add_log("No enemy in melee range.")
            return False
        
        #공격 가능한 적들 중 hp가 가장 낮은 적을 선택
        enemy = min(targets, key=lambda target: target.hp)
        damage = max(1, player.atk - enemy.defense)
        enemy.hp -= damage
        self.add_log(f"{player.name} attacks {enemy.name} for {damage}.")
        if not enemy.alive:
            player.kills += 1
            self.add_log(f"{enemy.name} defeated. {player.gain_xp(enemy.xp)}")
            dungeon.remove_dead()
        return True


    #플레이어 턴이 끝난 후 실행
    def enemy_turn(self) -> None:
        player = self.game.player
        dungeon = self.game.dungeon
        #현재 적들이 차지하는 칸. 적들이 겹쳐서 이동하지 않도록 하기 위해 사용
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
                #적이 이동하기 전에 현재 위치를 occupied에서 제거하여 적이 자신의 위치로 이동할 수 있도록 함
                occupied.discard((enemy.x, enemy.y))
                
                #적이 플레이어를 향해 한 칸 이동하도록 함. BFS를 사용하여 최적의 경로를 찾음    
                step = dungeon.next_step_toward((enemy.x, enemy.y), (player.x, player.y), occupied)
                if step != (player.x, player.y):
                    enemy.x, enemy.y = step
                occupied.add((enemy.x, enemy.y))
