# Python Game - PyGame
# pip install pygame
# ./Part1/studyPyGame/Assets
import pygame

width = 500; height = 500

pygame.init() # 게임 초기화 필수 1
# get-set 가져오고 설정하고
win = pygame.display.set_mode((width, height)) # 윈도우 500, 500
pygame.display.set_caption('게임 만들기')

icon = pygame.image.load('./Part1/studyPyGame/game.png')
pygame.display.set_icon(icon)

# object 설정
x = 250
y = 250
radius = 10
# 속도 velocity
vel_x = 10
vel_y = 10
jump = False

run = True

# 시그널 = 이벤트 
# GUI도 내부적으로 사용자가 뭐하는지 돌면서 계속 감시하고 있음
while run:
    win.fill((0,0,0)) # 전체 배경을 검은색으로 
    pygame.draw.circle(win, (255,255,255), (x, y), radius)

    for event in pygame.event.get(): # 2. 이벤트 받기
        if event.type == pygame.QUIT:
            run = False

    # 객체 이동
    userInput = pygame.key.get_pressed()
    if userInput[pygame.K_LEFT] and x > 10:
        x -= vel_x # 왼쪽으로 10씩 이동
    elif userInput[pygame.K_RIGHT] and x < width - 10:
        x += vel_x
    # elif userInput[pygame.K_UP] and y > 10:
    #     y -= vel_x # 여기 조심 해야된다. 왼쪽 위가 0이라서
    # elif userInput[pygame.K_DOWN] and y < height - 10:
    #     y += vel_x

    # 객체 점프
    if jump is False and userInput[pygame.K_SPACE]:
        jump = True
    elif jump is True:
        y -= vel_y * 3
        vel_y -= 1
        if vel_y < -10:
            jump = Falsew
            vel_y = 10
        
    pygame.time.delay(10)
    pygame.display.update() # 3. 화면 업데이트(전환)
