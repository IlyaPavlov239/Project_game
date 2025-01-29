def game():
    import pygame
    import math

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

    pygame.mixer.music.load('music/OMFG - Hello.mp3')
    pygame.mixer.music.play(-1)

    sw1 = True
    sw2 = True
    sw3 = True
    sw4 = True

    s1 = pygame.Rect(900, HEIGHT / 2 - 10, 20, 70)  # Светофор слева от перекрестка
    s2 = pygame.Rect(WIDTH - 900 + 25, HEIGHT / 2 - 10, 20, 70)  # Светофор справа
    s3 = pygame.Rect(WIDTH / 2 - 10, 480, 70, 20)  # Светофор сверху
    s4 = pygame.Rect(WIDTH / 2 - 10, HEIGHT - 455, 70, 20)  # Светофор снизу

    def rotate_rect(surface, color, rect, angle):
        """
        Функция, которая вращает прямоугольник вокруг его центра.

        :param surface: Экран, на котором рисуется (pygame.Surface)
        :param color: Цвет прямоугольника
        :param rect: Исходный прямоугольник (pygame.Rect)
        :param angle: Угол поворота (в градусах)
        """
        # Создаем новую поверхность с размером исходного прямоугольника
        rect_surface = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
        rect_surface.fill(color)

        # Поворачиваем поверхность
        rotated_surface = pygame.transform.rotate(rect_surface, angle)

        # Обновляем позицию так, чтобы центр остался прежним
        rotated_rect = rotated_surface.get_rect(center=rect.center)

        # Рисуем повернутую поверхность
        surface.blit(rotated_surface, rotated_rect.topleft)

    class CarHor:
        def __init__(self, x, y, z, turn):
            self.rect = pygame.Rect(x, y, 50, 20)
            self.z = z
            self.turn = turn
        def pos(self):
            return self.rect.center

        def move(self):
            if self.z == 1:
                self.rect.x += 1
            else:
                self.rect.x -= 1
            if self.rect.x > WIDTH or self.rect.x < -50:
                self.rect.x = 0 if self.z == 1 else WIDTH


        def draw(self, surface):
            pygame.draw.rect(surface, RED, self.rect)

    class CarVer:
        def __init__(self, x, y, z):
            self.rect = pygame.Rect(x, y, 20, 50)
            self.z = z

        def pos(self):
            return self.rect.center

        def move(self):
            if self.z == 1:
                self.rect.y += 1
            else:
                self.rect.y -= 1
            if self.rect.y > HEIGHT or self.rect.y < -50:
                self.rect.y = 0 if self.z == 1 else HEIGHT

        def draw(self, surface):
            pygame.draw.rect(surface, BLACK, self.rect)

    # Создаем машины
    hor_cars = [CarHor(0, HEIGHT / 2 - 10, 1), CarHor(WIDTH, HEIGHT / 2 + 30, -1)]
    ver_cars = [CarVer(WIDTH / 2 - 10, 0, 1), CarVer(WIDTH / 2 + 30, HEIGHT, -1)]

    # Основной игровой цикл
    running = True
    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # 1 - левая кнопка мыши
                    if s1.colliderect(event.pos):
                        sw1 = not sw1
                    if s2.colliderect(event.pos):
                        sw2 = not sw2
                    if s3.colliderect(event.pos):
                        sw3 = not sw3
                    if s4.colliderect(event.pos):
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

        # Обновляем и рисуем машины
        for car in hor_cars:
            if car.z == 1 and not (s1.colliderect(car.rect) and not sw1):  # Проверка светофора слева
                car.move()
            elif car.z == -1 and not (s2.colliderect(car.rect) and not sw2):  # Проверка светофора справа
                car.move()
            car.draw(screen)

        for car in ver_cars:
            if car.z == 1 and not (s3.colliderect(car.rect) and not sw3):  # Проверка светофора сверху
                car.move()
            elif car.z == -1 and not (s4.colliderect(car.rect) and not sw4):  # Проверка светофора снизу
                car.move()
            car.draw(screen)

        # Обновляем экран
        pygame.display.flip()
        clock.tick(FPS)

    # Завершение Pygame
    pygame.mixer.quit()
    pygame.quit()
