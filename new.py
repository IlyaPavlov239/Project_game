import pygame
import random

# Инициализация Pygame
pygame.init()

# Константы
WIDTH, HEIGHT = 1920, 1080
FPS = 60

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
RED = (255, 0, 0)
GREEN = (10, 247, 49)

# Настройка окна
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Дороги и Машины")

sw1=True
sw2=True
sw3=True
sw4=True

class CarHor:
    def __init__(self, x, y, z):
        self.rect = pygame.Rect(x, y, 50, 20)
        self.z=z

    def pos(self):
        return self.rect.center

    def move(self):
        if self.z==True:
            self.rect.x += 1
        else:
            self.rect.x -= 1
        if self.rect.y > HEIGHT or self.rect.y<0 or self.rect.x > WIDTH or self.rect.x < 0:
            if self.z==True:
                self.rect.y=HEIGHT/2-10
                self.rect.x=0

    def draw(self, surface):
        pygame.draw.rect(surface, RED, self.rect)

testcar=CarHor(0,HEIGHT/2-10,True)

# Основной игровой цикл
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Заполнение фона
    screen.fill(WHITE)



    # Рисуем дороги
    pygame.draw.rect(screen, GRAY, (0, HEIGHT/2-25, WIDTH, 100))
    pygame.draw.rect(screen, GRAY, (WIDTH/2-25, 0, 100, HEIGHT))
    if sw1==True:
        pygame.draw.rect(screen, GREEN, (900, HEIGHT/2-10, 20, 70))
    else:
        pygame.draw.rect(screen, RED, (900, HEIGHT/2-10, 20, 70))

    if sw2==True:
        pygame.draw.rect(screen, GREEN, (WIDTH-900+25, HEIGHT/2-10, 20, 70))
    else:
        pygame.draw.rect(screen, RED, (WIDTH-900+25, HEIGHT/2-10, 20, 70))

    if sw3==True:
        pygame.draw.rect(screen, GREEN, (WIDTH/2-10, 480, 70, 20))
    else:
        pygame.draw.rect(screen, RED, (WIDTH/2-10, 480, 70, 20))

    if sw4==True:
        pygame.draw.rect(screen, GREEN, (WIDTH/2-10, HEIGHT-455, 70, 20))
    else:
        pygame.draw.rect(screen, RED, (WIDTH/2-10, HEIGHT-455, 70, 20))

    testcar.draw(screen)


    keys = pygame.key.get_pressed()

    if keys[pygame.K_1]:
        sw1=not sw1
    if keys[pygame.K_2]:
        sw2 = not sw2
    if keys[pygame.K_3]:
        sw3 = not sw3
    if keys[pygame.K_4]:
        sw4 = not sw4

    if not(sw1==False and testcar.pos()[0]==850):
        testcar.move()

    # Обновляем экран
    pygame.display.flip()
    clock.tick(FPS)

# Завершение Pygame
pygame.quit()
