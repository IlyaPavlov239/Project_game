import pygame
import random

# Инициализация Pygame
pygame.init()


# Настройки экрана
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Светофор на перекрестке")

# Цвета
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)



# Класс для машин
class Car:
    def __init__(self, x, y):
        self.image = pygame.Surface((40, 20))
        self.image.fill((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = random.randint(3, 5)

    def move(self):
        self.rect.x += self.speed


# Создание машин
cars = [Car(random.randint(0, WIDTH), random.randint(0, HEIGHT // 2)) for _ in range(5)]


# Светофор
class TrafficLight:
    def __init__(self):
        self.state = "RED"
        self.timer = 0

    def update(self):
        if self.state == "RED":
            if self.timer >= 300:  # Длительность красного света
                self.state = "GREEN"
                self.timer = 0
        elif self.state == "GREEN":
            if self.timer >= 300:  # Длительность зеленого света
                self.state = "YELLOW"
                self.timer = 0
        elif self.state == "YELLOW":
            if self.timer >= 100:  # Длительность желтого света
                self.state = "RED"
                self.timer = 0

    def draw(self):
        if self.state == "RED":
            color = RED
        elif self.state == "GREEN":
            color = GREEN
        else:
            color = YELLOW

        pygame.draw.rect(screen, color, (WIDTH // 2 - 20, HEIGHT // 2 - 50, 40, 100))


# Основной цикл игры
def main():
    clock = pygame.time.Clock()
    running = True
    traffic_light = TrafficLight()

    while running:
        screen.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Управление светофором с помощью клавиш
        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:  # Красный свет
            traffic_light.state = "RED"
            traffic_light.timer = 0
        elif keys[pygame.K_g]:  # Зеленый свет
            traffic_light.state = "GREEN"
            traffic_light.timer = 0
        elif keys[pygame.K_y]:  # Желтый свет
            traffic_light.state = "YELLOW"
            traffic_light.timer = 0

        # Обновление состояния светофора
        traffic_light.timer += 1
        traffic_light.update()

        # Движение машин
        for car in cars:
            if traffic_light.state == "RED" and car.rect.x > WIDTH // 2 - 20 and car.rect.x < WIDTH // 2 + 20:
                car.speed = 0  # Останавливаем машину на красный свет
            else:
                car.speed = random.randint(3, 5)  # Возвращаем случайную скорость

            car.move()
            screen.blit(car.image, car.rect)

        # Отрисовка светофора
        traffic_light.draw()

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
