import pygame
import sys

# Инициализация Pygame
pygame.init()

# Установка размеров окна
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Кнопка Выхода")

# Цвета
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Размеры кнопки
button_width, button_height = 200, 100
button_rect = pygame.Rect((WIDTH // 2 - button_width // 2, HEIGHT // 2 - button_height // 2), (button_width, button_height))

# Основной игровой цикл
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Проверка нажатия кнопки мыши
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos  # Получаем позицию курсора мыши
            if button_rect.collidepoint(mouse_pos):  # Проверяем, находится ли курсор внутри кнопки
                running = False

    # Заполнение фона
    screen.fill(WHITE)

    # Рисуем кнопку выхода
    pygame.draw.rect(screen, RED, button_rect)  # Рисуем красную кнопку

    # Обновляем экран
    pygame.display.flip()

# Завершение Pygame
pygame.quit()
sys.exit()
