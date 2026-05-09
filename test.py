import pygame
import sys

# pygame 초기화
pygame.init()

# 창 크기 설정
WIDTH = 800
HEIGHT = 600

# 게임 창 생성
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# 창 제목
pygame.display.set_caption("Dungeon Game")

# 게임 루프
running = True
while running:

    # 이벤트 처리
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 배경색 채우기 (검정)
    screen.fill((0, 0, 0))

    # 화면 업데이트
    pygame.display.update()

# 종료
pygame.quit()
sys.exit()