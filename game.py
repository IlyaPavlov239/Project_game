import pygame
import random
import math
import os

def run(screen, difficulty):   
    # Инициализация Pygame
    pygame.mixer.init()
    start_time = pygame.time.get_ticks()
    tspawn = 0
    font = pygame.font.Font("KellySlab-Regular.ttf", 80)
    # Цвета
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GRAY = (128, 128, 128)
    RED = (255, 0, 0)
    GREEN = (10, 247, 49)
    BLUE = (0, 0, 255)  # Цвет кнопки CONTINUE
    DARK_BLUE = (0, 0, 200)  # Темный синий для наведения
    DARKER_BLUE = (0, 0, 150)  # Еще темнее синий для нажатия
    GREEN_BUTTON = (0, 255, 0)  # Цвет кнопки MENU
    DARK_GREEN = (0, 200, 0)  # Темный зеленый для наведения
    DARKER_GREEN = (0, 150, 0)  # Еще темнее зеленый для нажатия

    # Константы
    WIDTH, HEIGHT = 1920, 1080
    FPS = 60
    paused = False
    pause1 = pygame.image.load('images/pause1.png')
    pause2 = pygame.image.load('images/pause2.png')
    pause1_rect = pause1.get_rect(topleft=(300, 130))
    pause2_rect = pause2.get_rect(topleft=(300, 130))
    press = False

    def load_cari_files(directory):
        """
        Загружает файлы вида 'cari.*' (где i - натуральное число) из указанной директории
        Возвращает список загруженных поверхностей (Surface)
        """
        images = []
        i = 1
        
        while True:
            # Формируем базовое имя файла (без расширения)
            base_name = f"car{i}"
            
            # Ищем файл с таким именем и любым расширением
            found = False
            for file in os.listdir(directory):
                if file.startswith(base_name):
                    try:
                        # Пытаемся загрузить изображение
                        img = pygame.image.load(os.path.join(directory, file)).convert_alpha()
                        images.append(img)
                        found = True
                        i += 1
                        break
                    except pygame.error:
                        continue
            
            # Если файл не найден, прерываем цикл
            if not found:
                break
        
        return images

    # Кнопка CONTINUE
    continue_rect = pygame.Rect(WIDTH / 2, 250, 380, 90)  # Позиция и размер кнопки
    continue_rect.center = (WIDTH / 2, 500)
    continue_text = font.render("CONTINUE", True, WHITE)

    # Кнопка MENU
    finish_rect = pygame.Rect(WIDTH / 2, 250, 240, 90)  # Позиция и размер кнопки
    finish_rect.center = (WIDTH / 2, 700)
    finish_text = font.render("MENU", True, WHITE)

    # Переменные для анимации кнопок
    continue_button_pressed = False
    finish_button_pressed = False
    continue_button_hovered = False
    finish_button_hovered = False

    advert1 = pygame.image.load("images/advert1.png")  # Убедись, что файл находится в той же папке
    advert2 = pygame.image.load("images/advert2.png")  # Убедись, что файл находится в той же папке

    # Загрузка изображений машин
    car_horizontal_right = load_cari_files("images/hor_right")
    car_horizontal_left = load_cari_files("images/hor_left")
    car_vertical_down = load_cari_files("images/ver_down")
    car_vertical_up = load_cari_files("images/ver_up")

    # Фоновая музыка
    pygame.mixer.music.load('music/OMFG - Hello.mp3')
    pygame.mixer.music.play(-1)

    # Состояния светофоров
    sw = [True, True, True, True]
    s = [pygame.Rect(900, HEIGHT / 2 - 15, 20, 100), pygame.Rect(WIDTH - 900 + 55, HEIGHT / 2 - 15, 20, 100), pygame.Rect(WIDTH / 2 - 15, 480, 100, 20), pygame.Rect(WIDTH / 2 - 15, HEIGHT - 425, 100, 20)]
    # Устанавливаем центры светофоров
    s[0].center = (WIDTH / 2 - 85, HEIGHT / 2)  # Левый горизонтальный
    s[1].center = (WIDTH / 2 + 85, HEIGHT / 2)  # Правый горизонтальный
    s[2].center = (WIDTH / 2, HEIGHT / 2 - 85)  # Верхний вертикальный
    s[3].center = (WIDTH / 2, HEIGHT / 2 + 85)  # Нижний вертикальный

    def is_near(cars):
        for i in cars:
            for k in cars:
                if i != k and i.direction == k.direction and i.orientation == k.orientation:
                    # Если машина i уже повернула, она не должна блокировать другие машины
                    if i.orientation == "horizontal":
                        if (i.direction == 1 and i.x > k.x and i.x < 856) or (i.direction == -1 and i.x < k.x and i.x > 1063):
                            if abs(i.x - k.x) < 120:
                                # Если машина i уже повернула, она не блокирует k
                                if not (i.turn == "up" and i.y < 437) and not (i.turn == "down" and i.y > 643):
                                    k.stop()
                    elif i.orientation == "vertical":
                        if (i.direction == 1 and i.y > k.y and i.y < 437) or (i.direction == -1 and i.y < k.y and i.y > 643):
                            if abs(i.y - k.y) < 120:
                                # Если машина i уже повернула, она не блокирует k
                                if not (i.turn == "left" and i.x < 856) and not (i.turn == "right" and i.x > 1063):
                                    k.stop()

    def is_red(cars):
        for j in cars:
            j.go()
        for i in cars:
            if i.orientation == "horizontal":
                if i.x > s[0].center[0] - 50 and i.x < s[0].center[0]-40 and i.direction == 1 and not sw[0]:
                    i.stop()
                elif i.x < s[1].center[0] + 50 and i.x > s[1].center[0]+40 and i.direction == -1 and not sw[1]:
                    i.stop()
            else:
                if i.y > s[2].center[1] - 50 and i.y < s[2].center[1]-40 and i.direction == 1 and not sw[2]:
                    i.stop()
                elif i.y < s[3].center[1] + 50 and i.y > s[3].center[1]+40 and i.direction == -1 and not sw[3]:
                    i.stop()

    # Класс машины (работает с изображениями)
    class Car:
        def __init__(self, direction, turn, orientation, speed):
            # Начальные координаты машины
            if orientation == "horizontal":
                if direction == 1:
                    self.x, self.y = 0, HEIGHT - 500  # Начальная позиция для горизонтальных машин
                    self.image = car_horizontal_right[random.randrange(0, len(car_horizontal_right)-1, 1)]  # Используем изображение для движения вправо
                else:
                    self.x, self.y = WIDTH, 495
                    self.image = car_horizontal_left[random.randrange(0, len(car_horizontal_right)-1, 1)]  # Используем изображение для движения влево
            else:
                if direction == 1:
                    self.x, self.y = 915, 0  # Начальная позиция для вертикальных машин
                    self.image = car_vertical_down[random.randrange(0, len(car_horizontal_right)-1, 1)]  # Используем изображение для движения вниз
                else:
                    self.x, self.y = WIDTH - 920, HEIGHT
                    self.image = car_vertical_up[random.randrange(0, len(car_horizontal_right)-1, 1)]  # Используем изображение для движения вверх

            self.direction = direction  # Направление движения (1 - вправо, -1 - влево / вверх, вниз)
            self.turn = turn  # Поворот (например, "up", "down", "forward")
            self.orientation = orientation  # Ориентация ("horizontal" или "vertical")
            self.angle = 0  # Угол поворота машины
            self.speed = speed  # Скорость машины
            self.angv = speed / abs(speed) * (abs(speed) + 1)  # Угловая скорость

            # Точки поворота
            if orientation == "horizontal":
                if turn == "up":
                    self.pov_x, self.pov_y = 1000, 465  # Точка поворота вверх
                elif turn == "down":
                    self.pov_x, self.pov_y = 915, 615  # Точка поворота вниз
                else:  # forward
                    self.pov_x, self.pov_y = WIDTH, HEIGHT // 2  # Прямо
            elif orientation == "vertical":
                if turn == "left":
                    self.pov_x, self.pov_y = 935, 500  # Точка поворота влево
                elif turn == "right":
                    self.pov_x, self.pov_y = 1035, 580  # Точка поворота вправо
                else:  # forward
                    self.pov_x, self.pov_y = WIDTH // 2, HEIGHT  # Прямо

            # Создаем маску для машины
            self.mask = pygame.mask.from_surface(self.image, threshold=127)
            rotated_surface = pygame.transform.rotozoom(self.image, self.angle, 1)
            self.rect = rotated_surface.get_rect(center=(self.x, self.y))
            self.stopped = False  # Флаг остановки машины

        def move(self):
            """Двигает машину в зависимости от её направления и ориентации."""
            if self.stopped:
                return True

            if self.orientation == "horizontal":
                if self.direction == 1:  # Движение вправо
                    if self.x < self.pov_x:
                        self.x += self.speed
                    else:
                        if self.turn == "up":
                            if self.angle < 90:
                                self.angle += self.angv
                                self.y -= self.speed
                            else:
                                self.y -= self.speed
                        elif self.turn == "down":
                            if self.angle > -90:
                                self.angle -= self.angv
                                self.y += self.speed
                            else:
                                self.y += self.speed
                        elif self.turn == "forward":
                            self.x += self.speed
                elif self.direction == -1:  # Движение влево
                    if self.x > self.pov_x:
                        self.x -= self.speed
                    else:
                        if self.turn == "up":
                            if self.angle > -90:
                                self.angle -= self.angv
                                self.y -= self.speed
                            else:
                                self.y -= self.speed
                        elif self.turn == "down":
                            if self.angle < 90:
                                self.angle += self.angv
                                self.y += self.speed
                            else:
                                self.y += self.speed
                        elif self.turn == "forward":
                            self.x -= self.speed
            elif self.orientation == "vertical":
                if self.direction == 1:  # Движение вниз
                    if self.y < self.pov_y:
                        self.y += self.speed
                    else:
                        if self.turn == "left":
                            if self.angle > -90:
                                self.angle -= self.angv
                                self.x -= self.speed
                            else:
                                self.x -= self.speed
                        elif self.turn == "right":
                            if self.angle < 90:
                                self.angle += self.angv
                                self.x += self.speed
                            else:
                                self.x += self.speed
                        elif self.turn == "forward":
                            self.y += self.speed
                elif self.direction == -1:  # Движение вверх
                    if self.y > self.pov_y:
                        self.y -= self.speed
                    else:
                        if self.turn == "left":
                            if self.angle < 90:
                                self.angle += self.angv
                                self.x -= self.speed
                            else:
                                self.x -= self.speed
                        elif self.turn == "right":
                            if self.angle > -90:
                                self.angle -= self.angv
                                self.x += self.speed
                            else:
                                self.x += self.speed
                        elif self.turn == "forward":
                            self.y -= self.speed

            # Обновляем маску после изменения положения или поворота
            rotated_surface = pygame.transform.rotozoom(self.image, self.angle, 1)
            self.mask = pygame.mask.from_surface(rotated_surface, threshold=127)
            self.rect = rect = rotated_surface.get_rect(center=(self.x, self.y))
            # Проверка на выход за границы экрана
            if self.x > WIDTH or self.x < 0 or self.y < 0 or self.y > HEIGHT:
                return False
            return True

        def draw(self, surface):
            """Отрисовывает машину на экране."""
            # Поворачиваем изображение машины
            rotated_surface = pygame.transform.rotozoom(self.image, self.angle, 1)
            # Корректируем позицию после поворота
            surface.blit(rotated_surface, self.rect.topleft)

        def stop(self):
            """Останавливает машину."""
            self.stopped = True

        def go(self):
            """Запускает машину."""
            self.stopped = False

    def is_collision(m, j):
        """Проверяет, есть ли реальное столкновение между машинами m и j."""
        offset = (int(j.rect.topleft[0] - m.rect.topleft[0]), int(j.rect.topleft[1] - m.rect.topleft[1]))
        collision = m.mask.overlap(j.mask, offset) is not None
        if collision:
            print(f"Collision between cars at ({m.x}, {m.y}) and ({j.x}, {j.y})")
        return collision

    # Основной игровой цикл
    running = True
    clock = pygame.time.Clock()
    last_spawn_time = pygame.time.get_ticks() - start_time

    cars = []  # Список для хранения всех машин

    while running:
        current_time = pygame.time.get_ticks() - start_time

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Левая кнопка мыши
                    print(event.pos)
                    if not paused:
                        for i in range(len(s)):
                            if s[i].collidepoint(event.pos):
                                sw[i] = not sw[i]
                    else:
                        if continue_rect.collidepoint(event.pos):
                            continue_button_pressed = True
                        if finish_rect.collidepoint(event.pos):
                            finish_button_pressed = True
                    if pause1_rect.collidepoint(event.pos) or pause2_rect.collidepoint(event.pos):
                        press = not press
                        paused = not paused
            elif event.type == pygame.MOUSEBUTTONUP:
                if continue_button_pressed:
                    continue_button_pressed = False
                    if continue_rect.collidepoint(event.pos):
                        press = not press
                        paused = not paused
                if finish_button_pressed:
                    finish_button_pressed = False
                    if finish_rect.collidepoint(event.pos):
                        return ("menu", (current_time // 1000))

        # Заполнение фона
        screen.fill(WHITE)

        if press:
            screen.blit(pause2, pause2_rect)
        else:
            screen.blit(pause1, pause1_rect)

        if not paused:
            # Спавн машин каждую 3 секунды
            if current_time - last_spawn_time >= tspawn:  # Если прошло tspawn секунды
                direction = random.choice([-1, 1])  # Случайное направление
                orientation = random.choice(["horizontal", "vertical"])  # Случайная ориентация
                if orientation == "horizontal":
                    turn = random.choice(["up", "down", "forward"])
                else:
                    turn = random.choice(["left", "right", "forward"])

                # Создаем новую машину и добавляем её в список
                new_car = Car(direction, turn, orientation, 2)
                cars.append(new_car)

                last_spawn_time = current_time  # Обновляем время последнего спавна


            # Установка формулы в зависимости от уровня сложности
            if difficulty == "easy":
                tspawn = max(1200, 2500 * math.exp(-current_time / 80000))
            elif difficulty == "medium":
                tspawn = max(1000, 2000 * math.exp(-current_time / 40000))
            elif difficulty == "hard":
                tspawn = max(800, 1500 * math.exp(-current_time / 20000))

            # Рисуем дороги
            pygame.draw.rect(screen, GRAY, (0, HEIGHT / 2 - 75, WIDTH, 150))
            pygame.draw.rect(screen, GRAY, (WIDTH / 2 - 75, 0, 150, HEIGHT))

            # Рисуем светофоры
            for i in range(len(s)):
                pygame.draw.rect(screen, GREEN if sw[i] else RED, s[i])

            texttime = font.render(f"Time: {current_time // 1000}", True, (0, 0, 0))
            texttime_rect = texttime.get_rect(topleft=(500, 130))
            screen.blit(texttime, texttime_rect)

            # Движение машин
            for car in cars[:]:
                if not car.move():  # Если машина вышла за границы, удаляем её
                    cars.remove(car)

            # Отрисовываем машины
            for car in cars:
                car.draw(screen)

            if cars != []:
                is_red(cars)
                is_near(cars)

            if current_time > 2000:
                for m in cars:
                    for j in cars:
                        if m != j:
                            # Проверяем расстояние между машинами
                            distance = math.sqrt((m.x - j.x) ** 2 + (m.y - j.y) ** 2)
                            if distance < 100:  # Проверяем только близкие машины
                                if is_collision(m, j):
                                    return ("game_over", (current_time // 1000))

        else:
            # Получаем позицию мыши
            mouse_pos = pygame.mouse.get_pos()

            # Обработка наведения на кнопку CONTINUE
            if continue_rect.collidepoint(mouse_pos):
                continue_button_hovered = True
                continue_button_color = DARK_BLUE  # Темный синий при наведении
            else:
                continue_button_hovered = False
                continue_button_color = BLUE  # Обычный синий

            # Обработка наведения на кнопку MENU
            if finish_rect.collidepoint(mouse_pos):
                finish_button_hovered = True
                finish_button_color = DARK_GREEN  # Темный зеленый при наведении
            else:
                finish_button_hovered = False
                finish_button_color = GREEN_BUTTON  # Обычный зеленый

            # Рисуем кнопку CONTINUE
            if continue_button_pressed:
                continue_button_color = DARKER_BLUE  # Еще темнее синий при нажатии
            pygame.draw.rect(screen, continue_button_color, continue_rect, border_radius=20)
            continue_text_rect = continue_text.get_rect(center=continue_rect.center)
            if continue_button_pressed:
                continue_text_rect.move_ip(5, 5)  # Смещение текста при нажатии
            screen.blit(continue_text, continue_text_rect)

            # Рисуем кнопку MENU
            if finish_button_pressed:
                finish_button_color = DARKER_GREEN  # Еще темнее зеленый при нажатии
            pygame.draw.rect(screen, finish_button_color, finish_rect, border_radius=20)
            finish_text_rect = finish_text.get_rect(center=finish_rect.center)
            if finish_button_pressed:
                finish_text_rect.move_ip(5, 5)  # Смещение текста при нажатии
            screen.blit(finish_text, finish_text_rect)

        # Обновляем экран
        pygame.display.flip()
        clock.tick(FPS)

    # Завершение Pygame
    pygame.mixer.quit()