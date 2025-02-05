import pygame
import random
from menu import menu
from pygame.examples.moveit import WIDTH

import game_over

# Инициализация Pygame
pygame.init()
pygame.mixer.init()

font = pygame.font.Font("KellySlab-Regular.ttf", 80)
# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
RED = (255, 0, 0)
GREEN = (10, 247, 49)

# Константы
WIDTH, HEIGHT = 1920, 1080
FPS = 60
paused=False
pause1 = pygame.image.load('images/pause1.png')
pause2 = pygame.image.load('images/pause2.png')
pause1_rect = pause1.get_rect(topleft=(300,130))
pause2_rect = pause2.get_rect(topleft=(300,130))
press=False
continue_rect = pygame.Rect(WIDTH/2, 250, 380, 90)  # Позиция и размер кнопки
continue_rect.center = (WIDTH/2, 500)
continue_text = font.render("CONTINUE", True, WHITE)
finish_rect = pygame.Rect(WIDTH/2, 250, 270, 90)  # Позиция и размер кнопки
finish_rect.center = (WIDTH/2, 700)
finish_text = font.render("FINISH", True, WHITE)




# Настройка окна
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Дороги и Машины")

# Фоновая музыка
pygame.mixer.music.load('music/OMFG - Hello.mp3')
pygame.mixer.music.play(-1)

# Состояния светофоров
sw = [True, True, True, True]
s = [pygame.Rect(900, HEIGHT / 2 - 10, 20, 70), pygame.Rect(WIDTH - 900 + 25, HEIGHT / 2 - 10, 20, 70), pygame.Rect(WIDTH / 2 - 10, 480, 70, 20), pygame.Rect(WIDTH / 2 - 10, HEIGHT - 455, 70, 20)]



def is_near(cars):
    for i in cars:
        #if i.stopped == False:
            for k in cars:
                if not (i.rect.center[0]<1035 and i.rect.center[0]>935 and i.rect.center[1]>515 and i.rect.center[1]<615) and i.direction==k.direction and i.orientation==k.orientation and i!=k:
                    if i.orientation=="horizontal" and ((i.direction==1 and i.rect.center[0]>k.rect.center[0] and i.rect.center[0]<935) or (i.direction==-1 and i.rect.center[0]<k.rect.center[0] and i.rect.center[0]>1035)) and abs(i.rect.center[0]-k.rect.center[0])<70:
                        k.stop()
                    if i.orientation=="vertical" and ((i.direction==1 and i.rect.center[1]>k.rect.center[1] and i.rect.center[1]<515) or (i.direction==-1 and i.rect.center[1]<k.rect.center[1] and i.rect.center[1]>615)) and abs(i.rect.center[1]-k.rect.center[1])<70:
                        k.stop()

def is_red(cars):
    for j in cars:
        j.go()
    for i in cars:
        if i.orientation == "horizontal":
            if  i.rect.center[0] > s[0].center[0] - 5 and i.rect.center[0]<s[0].center[0] and i.direction==1 and not sw[0]:
                i.stop()
            elif  i.rect.center[0] < s[1].center[0] + 5 and i.rect.center[0]>s[1].center[0] and i.direction==-1 and not sw[1]:
                i.stop()

        else:
            if i.rect.center[1] > s[2].center[1] - 5 and i.rect.center[1]<s[2].center[1] and i.direction==1 and not sw[2]:
                i.stop()
            elif  i.rect.center[1] < s[3].center[1] + 5 and i.rect.center[1]>s[3].center[1] and i.direction==-1 and not sw[3]:
                i.stop()


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

    def go(self):
        """Останавливает машину при вызове."""
        self.stopped = False


# Основной игровой цикл
running = True
clock = pygame.time.Clock()
last_spawn_time = pygame.time.get_ticks()

cars = []  # Список для хранения всех машин

while running:
    current_time = pygame.time.get_ticks()

    # Спавн машин каждую 3 секунды
    if current_time - last_spawn_time >= 1000:  # Если прошло 3 секунды
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
            if event.button == 1:  # Левая кнопка мыши
                if not paused:
                    for i in range(len(s)):
                        if s[i].collidepoint(event.pos):
                            sw[i] = not sw[i]
                else:
                    if continue_rect.collidepoint(event.pos):
                        press = not press
                        paused = not paused
                    if finish_rect.collidepoint(event.pos):
                        menu.menu()
                if pause1_rect.collidepoint(event.pos) or pause2_rect.collidepoint(event.pos):
                    press=not press
                    paused=not paused
    # Заполнение фона
    screen.fill(WHITE)

    if press:
        screen.blit(pause2,pause2_rect)
    else:
        screen.blit(pause1, pause1_rect)

    if not paused:
        # Рисуем дороги
        pygame.draw.rect(screen, GRAY, (0, HEIGHT / 2 - 25, WIDTH, 100))
        pygame.draw.rect(screen, GRAY, (WIDTH / 2 - 25, 0, 100, HEIGHT))

        # Рисуем светофоры
        for i in range(len(s)):
            pygame.draw.rect(screen, GREEN if sw[i] else RED, s[i])

        texttime = font.render(f"Time: {pygame.time.get_ticks() // 1000}", True, (0, 0, 0))
        texttime_rect = texttime.get_rect(topleft=(500,130))
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

        if current_time>2000:
            for m in cars:
                for j in cars:
                    if ((m.rect.center[0]<1035 and m.rect.center[0]>935 and m.rect.center[1]>515 and m.rect.center[1]<615) and j.rect.colliderect(m.rect) and m != j) or new_car.stopped==True:
                        game_over.game_over(pygame.time.get_ticks()//1000)
                        running=False
                        #screen.blit(game_over_image, game_over_image_rect)
    else:
        pygame.draw.rect(screen, GRAY, continue_rect)
        screen.blit(continue_text,continue_rect)
        pygame.draw.rect(screen, GRAY, finish_rect)
        screen.blit(finish_text, finish_rect)
    # Обновляем экран
    pygame.display.flip()
    clock.tick(FPS)

# Завершение Pygame
pygame.mixer.quit()
pygame.quit()