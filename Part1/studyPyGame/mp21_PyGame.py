# Python Game - PyGame
# pip install pygame
# ./Part1/studyPyGame/Assets
import pygame

pygame.init() # 게임 초기화 필수 1
# get-set 가져오고 설정하고
win = pygame.display.set_mode((1000, 500))
pygame.display.set_caption('게임 만들기')

bg_img = pygame.image.load('./Part1/studyPyGame/Assets/Backgound.png')
BG = pygame.transform.scale(bg_img, (1000, 500))# 스케일 업

icon = pygame.image.load('./Part1/studyPyGame/game.png')
pygame.display.set_icon(icon)

loop = 0
run = True
width = 1000 
# 시그널 = 이벤트 
# GUI도 내부적으로 사용자가 뭐하는지 돌면서 계속 감시하고 있음
while run:
    win.fill((0,0,0))
    for event in pygame.event.get(): # 2. 이벤트 받기
        if event.type == pygame.QUIT:
            run = False

    # 배경을 그림
    win.blit(BG, (loop, 0))
    win.blit(BG, (width + loop, 0))
    if loop == -width: # loop가 -1000이랑 같아지면
        loop = 0
    loop -= 1

    pygame.display.update()