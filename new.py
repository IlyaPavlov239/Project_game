import pygame
import math
import random


# Инициализация Pygame
pygame.init()
pygame.mixer.init()

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

# Фоновая музыка
pygame.mixer.music.load('music/OMFG - Hello.mp3')
pygame.mixer.music.play(-1)

# Состояния светофоров
sw1 = True
sw2 = True
sw3 = True
sw4 = True

# Светофоры
s1 = pygame.Rect(900, HEIGHT / 2 - 10, 20, 70)
s2 = pygame.Rect(WIDTH - 900 + 25, HEIGHT / 2 - 10, 20, 70)
s3 = pygame.Rect(WIDTH / 2 - 10, 480, 70, 20)
s4 = pygame.Rect(WIDTH / 2 - 10, HEIGHT - 455, 70, 20)

def is_near(cars):

        for i in range(len(cars)):
            if not (cars[i].rect.center[0]<1035 and cars[i].rect.center[0]>935 and cars[i].rect.center[1]>515 and cars[i].rect.center[1]<615):
                for k in range(len(cars)):
                    if k!=i and cars[i].orientation == cars[k].orientation and cars[i].direction == cars[k].direction:
                            if cars[i].orientation=="horizontal":
                                if cars[i].rect.center[0] == cars[k].rect.center[0] + cars[i].direction * (25):
                                    cars[k].stop()
                                    break
                            if cars[i].orientation == "vertical":
                                if cars[i].rect.center[1] == cars[k].rect.center[1] + cars[i].direction * (25):
                                    cars[k].stop()
                                    break


# Класс машины (универсальный)

class Car:
    def __init__(self, direction, turn, orientation):
        if orientation == "horizontal":
            if direction == 1:
                x, y = 0, HEIGHT - 505
            else:
                x, y = WIDTH, 530
        else:
            if direction == 1:
                x, y = 950, 0
            else:
                x, y = WIDTH - 925, HEIGHT

        self.rect = pygame.Rect(x, y, 50, 20) if orientation == "horizontal" else pygame.Rect(x, y, 20, 50)
        self.direction = direction  # Направление движения (1 - вправо, -1 - влево / вверх, вниз)
        self.turn = turn  # Поворот (например, "up", "down", "forward")
        self.orientation = orientation  # Ориентация ("horizontal" или "vertical")
        self.angle = 0

        # Инициализация точек поворота в зависимости от направления и ориентации
        if orientation == "horizontal":
            if turn == "down":
                self.pov_x = 935
                self.pov_y = 0
            elif turn == "up":
                self.pov_x = WIDTH - 935
                self.pov_y = 0
            else:  # forward
                self.pov_x = WIDTH
                self.pov_y = HEIGHT // 2
        elif orientation == "vertical":
            if turn == "right":
                self.pov_x = 0
                self.pov_y = HEIGHT - 515
            elif turn == "left":
                self.pov_x = 0
                self.pov_y = 515
            else:  # forward
                self.pov_x = WIDTH // 2
                self.pov_y = HEIGHT

        self.original_surface = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        self.original_surface.fill((0, 0, 0))
        self.surface = self.original_surface

        # Флаг для остановки машины
        self.stopped = False

    def pos(self):
        return self.rect.topleft

    def move(self):
        # Если машина остановлена, ничего не делаем
        if self.stopped:
            return True

        if self.orientation == "horizontal":  # Движение по горизонтали
            if self.direction == 1:  # Движение вправо
                if self.rect.x < self.pov_x:
                    self.rect.x += 2
                else:
                    if self.turn == "up":
                        if self.angle < 90:
                            self.angle += 2
                            self.rect.y -= 2
                        else:
                            self.rect.y -= 2
                    elif self.turn == "down":
                        if self.angle > -90:
                            self.angle -= 2
                            self.rect.y += 2
                        else:
                            self.rect.y += 2
                    elif self.turn == "forward":
                        self.rect.x += 2
            elif self.direction == -1:
                if self.rect.x > self.pov_x:
                    self.rect.x -= 2
                else:
                    if self.turn == "up":
                        if self.angle > -90:
                            self.angle -= 2
                            self.rect.y -= 2
                        else:
                            self.rect.y -= 2
                    elif self.turn == "down":
                        if self.angle < 90:
                            self.angle += 2
                            self.rect.y += 2
                        else:
                            self.rect.y += 2
                    elif self.turn == "forward":
                        self.rect.x -= 2
        elif self.orientation == "vertical":
            if self.direction == 1:  # движение вниз
                if self.rect.y < self.pov_y:
                    self.rect.y += 2
                else:
                    if self.turn == "left":
                        if self.angle > -90:
                            self.angle -= 2
                            self.rect.x -= 2
                        else:
                            self.rect.x -= 2
                    elif self.turn == "right":
                        if self.angle < 90:
                            self.angle += 2
                            self.rect.x += 2
                        else:
                            self.rect.x += 2
                    elif self.turn == "forward":
                        self.rect.y += 2
            elif self.direction == -1:  # движение вверх
                if self.rect.y > self.pov_y:
                    self.rect.y -= 2
                else:
                    if self.turn == "left":
                        if self.angle < 90:
                            self.angle += 2
                            self.rect.x -= 2
                        else:
                            self.rect.x -= 2
                    elif self.turn == "right":
                        if self.angle > -90:
                            self.angle -= 2
                            self.rect.x += 2
                        else:
                            self.rect.x += 2
                    elif self.turn == "forward":
                        self.rect.y -= 2

        if self.rect.x > WIDTH or self.rect.x < 0 or self.rect.y < 0 or self.rect.y > HEIGHT:
            return False
        return True

    def draw(self, surface):
        rotated_surface = pygame.transform.rotozoom(self.original_surface, self.angle, 1)
        rotated_rect = rotated_surface.get_rect(center=self.rect.center)
        surface.blit(rotated_surface, rotated_rect.topleft)

    def stop(self):
        """Останавливает машину при вызове."""
        self.stopped = True


# Основной игровой цикл
running = True
clock = pygame.time.Clock()
last_spawn_time = pygame.time.get_ticks()

cars = []  # Список для хранения всех машин

while running:
    current_time = pygame.time.get_ticks()

    # Спавн машин каждую 3 секунды
    if current_time - last_spawn_time >= 3000:  # Если прошло 3 секунды
        direction = random.choice([-1, 1])  # Случайное направление
        orientation = random.choice(["horizontal", "vertical"])  # Случайная ориентация
        if orientation == "horizontal":
            turn = random.choice(["up", "down", "forward"])
        else:
            turn = random.choice(["left", "right", "forward"])

        # Создаем новую машину и добавляем её в список
        new_car = Car(direction, turn, orientation)
        cars.append(new_car)

        last_spawn_time = current_time  # Обновляем время последнего спавна

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            print(pygame.mouse.get_pos())
            if event.button == 1:  # Левая кнопка мыши
                if s1.collidepoint(event.pos):
                    sw1 = not sw1
                if s2.collidepoint(event.pos):
                    sw2 = not sw2
                if s3.collidepoint(event.pos):
                    sw3 = not sw3
                if s4.collidepoint(event.pos):
                    sw4 = not sw4

    # Заполнение фона
    screen.fill(WHITE)

    # Рисуем дороги
    pygame.draw.rect(screen, GRAY, (0, HEIGHT / 2 - 25, WIDTH, 100))
    pygame.draw.rect(screen, GRAY, (WIDTH / 2 - 25, 0, 100, HEIGHT))

    # Рисуем светофоры
    pygame.draw.rect(screen, GREEN if sw1 else RED, s1)
    pygame.draw.rect(screen, GREEN if sw2 else RED, s2)
    pygame.draw.rect(screen, GREEN if sw3 else RED, s3)
    pygame.draw.rect(screen, GREEN if sw4 else RED, s4)

    # Движение машин
    for car in cars[:]:
        if not car.move():  # Если машина вышла за границы, удаляем её
            cars.remove(car)

    # Отрисовываем машины
    for car in cars:
        car.draw(screen)

    if cars != []:
        is_near(cars)

    # Обновляем экран
    pygame.display.flip()
    clock.tick(FPS)

# Завершение Pygame
pygame.mixer.quit()
pygame.quit()