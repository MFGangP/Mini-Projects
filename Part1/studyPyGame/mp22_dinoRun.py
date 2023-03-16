# dinoRun 공룡런

import pygame
import os

pygame.init()

ASSETS = './Part1/studyPyGame/Assets/'
SCREEN = pygame.display.set_mode((1100, 600))

icon = pygame.image.load('./Part1/studyPyGame/dinoRun.png')
pygame.display.set_icon(icon)
# 배경 이미지 로드
BG = pygame.image.load(os.path.join(f'{ASSETS}Other', 'Track.png'))
# 공룡 이미지 로드
RUNNING = [pygame.image.load('./Part1/studyPyGame/Assets/Dino/DinoRun1.png'),
           pygame.image.load(f'{ASSETS}Dino/DinoRun2.png')]
DUCKING = [pygame.image.load(f'{ASSETS}Dino/DinoDuck1.png'),
           pygame.image.load(f'{ASSETS}Dino/DinoDuck2.png')]
JUMPING = pygame.image.load(f'{ASSETS}Dino/DinoJump.png')


class Dino: # 공룡 클래스
    X_POS = 80; Y_POS = 310; Y_POS_DUCK = 340; JUMP_VEL = 9.0

    def __init__(self) -> None:
        self.run_img = RUNNING; self.duck_img = DUCKING; self.jump_img = JUMPING
        self.dino_run = True; self.dino_duck = False; self.dino_jump = False # 공룡 상태 3개

        self.step_index = 0
        self.jump_vel = self.JUMP_VEL # 점프 초기 값 9.0
        self.image = self.run_img[0]
        self.dino_rect = self.image.get_rect() # 사각형 이미지 정보
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS


    def update(self, userInput) -> None:
        if self.dino_run:
            self.run()
        elif self.dino_duck:
            self.duck()
        elif self.dino_jump:
            self.jump()
        
        if self.step_index >= 10: self.step_index = 0 # 애니메이션 스텝을 위해서

        if userInput[pygame.K_UP] and not self.dino_jump: # 점프
            self.dino_run = False
            self.dino_duck = False
            self.dino_jump = True
        elif userInput[pygame.K_DOWN] and not self.dino_jump: # 숙이기
            self.dino_run = False
            self.dino_duck = True
            self.dino_jump = False
        elif not (self.dino_jump or userInput[pygame.K_DOWN]): # 런
            self.dino_run = True
            self.dino_duck = False
            self.dino_jump = False            

    def run(self):
        self.image = self.run_img[self.step_index // 5] # run_img 10 1,0 반복
        self.dino_rect = self.image.get_rect() # 이미지 사각형 정보
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS
        self.step_index += 1

    def duck(self):
        self.image = self.duck_img[self.step_index // 5] # duck_img
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS 
        self.dino_rect.y = self.Y_POS_DUCK # 이미지 높이가 작으니까
        self.step_index += 1

    def jump(self):
        self.image = self.jump_img
        if self.dino_jump:
            self.dino_rect.y -= self.jump_vel * 4
            self.jump_vel -= 0.8
        if self.jump_vel < - self.JUMP_VEL: # -9.0이 되면 점프 중단
            self.dino_jump = False
            self.jump_vel = self.JUMP_VEL # 9.0으로 초기화 안그러면 땅에 박아버림

    def draw(self, SCREEN) -> None:
        SCREEN.blit(self.image, (self.dino_rect.x, self.dino_rect.y))

def main():
    run = True
    clock = pygame.time.Clock()

    dino = Dino()

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        SCREEN.fill((255,255,255)) # 배경 흰색
        userInput = pygame.key.get_pressed()

        dino.draw(SCREEN) # 공룡 그리기
        dino.update(userInput)

        clock.tick(30)
        pygame.display.update() # 초당 30번 업데이트 수행

if __name__ == '__main__':
    main()