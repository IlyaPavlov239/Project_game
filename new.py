import pygame
import math
import random

def game():
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
                    self.pov_x = WIDTH  # Для прямолинейного движения
                    self.pov_y = HEIGHT // 2  # Для прямолинейного движения
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

            self.original_surface = pygame.Surface((self.rect.width, self.rect.height))  # Оригинальная поверхность
            self.original_surface.fill(BLACK)
            self.surface = self.original_surface  # Отображаемая поверхность

        def pos(self):
            return self.rect.topleft

        def move(self):
            if self.orientation == "horizontal":  # Движение по горизонтали
                if self.direction == 1:  # Движение вправо
                    if self.rect.x < self.pov_x:  # Пока не достигли точки поворота
                        self.rect.x += 2
                    else:  # Начало поворота
                        if self.turn == "up":  # Начало поворота вверх
                            if self.angle < 90:
                                self.angle += 2
                                self.surface = pygame.transform.rotate(self.original_surface, self.angle)
                                self.rect.y -= 2
                            else:  # Продолжение движения вверх после поворота
                                self.rect.y -= 2
                        elif self.turn == "down":  # Начало поворота вниз
                            if self.angle > -90:
                                self.angle -= 2
                                self.surface = pygame.transform.rotate(self.original_surface, self.angle)
                                self.rect.y += 2
                            else:  # Продолжение движения вниз после поворота
                                self.rect.y += 2
                        elif self.turn == "forward":  # Прямолинейное движение вправо без поворота
                            self.rect.x += 2
                elif self.direction == -1:  # Движение влево
                    if self.rect.x > self.pov_x:  # Пока не достигли точки поворота
                        self.rect.x -= 2
                    else:  # Начало поворота
                        if self.turn == "up":  # Начало поворота вверх
                            if self.angle > -90:
                                self.angle -= 2
                                self.surface = pygame.transform.rotate(self.original_surface, self.angle)
                                self.rect.y -= 2
                            else:  # Продолжение движения вверх после поворота
                                self.rect.y -= 2
                        elif self.turn == "down":  # Начало поворота вниз
                            if self.angle < 90:
                                self.angle += 2
                                self.surface = pygame.transform.rotate(self.original_surface, self.angle)
                                self.rect.y += 2
                            else:  # Продолжение движения вниз после поворота
                                self.rect.y += 2
                        elif self.turn == "forward":  # Прямолинейное движение влево без поворота
                            self.rect.x -= 2

            elif self.orientation == "vertical":  # Движение по вертикали
                if self.direction == 1:  # Движение вниз
                    if self.rect.y < self.pov_y:  # Пока не достигли точки поворота
                        self.rect.y += 2
                    else:  # Начало поворота
                        if self.turn == "left":  # Начало поворота влево
                            if self.angle < 90:
                                self.angle += 2
                                self.surface = pygame.transform.rotate(self.original_surface, self.angle)
                                self.rect.x -= 2
                            else:  # Продолжение движения влево после поворота
                                self.rect.x -= 2
                        elif self.turn == "right":  # Начало поворота вправо
                            if self.angle > -90:
                                self.angle -= 2
                                self.surface = pygame.transform.rotate(self.original_surface, self.angle)
                                self.rect.x += 2
                            else:  # Продолжение движения вправо после поворота
                                self.rect.x += 2
                        elif self.turn == "forward":  # Прямолинейное движение вниз без поворота
                            self.rect.y += 2
                elif self.direction == -1:  # Движение вверх
                    if self.rect.y > self.pov_y:  # Пока не достигли точки поворота
                        self.rect.y -= 2
                    else:  # Начало поворота
                        if self.turn == "left":  # Начало поворота влево
                            if self.angle > -90:
                                self.angle -= 2
                                self.surface = pygame.transform.rotate(self.original_surface, self.angle)
                                self.rect.x -= 2
                            else:  # Продолжение движения влево после поворота
                                self.rect.x -= 2
                        elif self.turn == "right":  # Начало поворота вправо
                            if self.angle < 90:
                                self.angle += 2
                                self.surface = pygame.transform.rotate(self.original_surface, self.angle)
                                self.rect.x += 2
                            else:  # Продолжение движения вправо после поворота
                                self.rect.x += 2
                        elif self.turn == "forward":  # Прямолинейное движение вверх без поворота
                            self.rect.y -= 2

            # Проверка на выход за границы
            if self.rect.x > WIDTH or self.rect.x < 0 or self.rect.y < 0 or self.rect.y > HEIGHT:
                return False  # Возвращаем False, если машина вышла за границы
            return True  # Машина не вышла за границы

        def draw(self, surface):
            rotated_surface = pygame.transform.rotate(self.original_surface, self.angle)
            rotated_rect = rotated_surface.get_rect(center=self.rect.center)
            surface.blit(rotated_surface, rotated_rect.topleft)


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

        # Обновляем экран
        pygame.display.flip()
        clock.tick(FPS)

    # Завершение Pygame
    pygame.mixer.quit()
    pygame.quit()
