import pygame
import sys
import main
import buildings

# Инициализация Pygame
pygame.init()

# Разрешение экрана (будет полноэкранным)
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
width, height = screen.get_size()

# Загрузка изображений
background_image = pygame.image.load('images/background.png')  # Путь к фоновому изображению
button_image = pygame.image.load('images/start_buttton.png')  # Путь к изображению кнопки
exit_button_image = pygame.image.load('images/exit_button.png')  # Путь к изображению кнопки выхода
image_to_display = pygame.image.load('images/if_start.jpg')  # Путь к изображению, которое будет отображаться

# Масштабируем кнопки под размеры
button_rect = button_image.get_rect(center=(width // 2, height // 2))
exit_button_rect = exit_button_image.get_rect(topleft=(60, 45))  #  кнопка выхода

# Цвета
WHITE = (255, 255, 255)

# Создание шрифта для текста
font = pygame.font.SysFont('Arial', 36)

# Функция для отрисовки текста на экране
def draw_text(text, x, y):
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)

# Функция для показа изображения
def show_image():
    running_image_window = True
    image_window = pygame.display.set_mode((800, 600))  # Окно для отображения изображения, можно настроить размер
    while running_image_window:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running_image_window = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Выход из окна изображения
                    running_image_window = False

        # Отображение изображения
        image_window.fill((0, 0, 0))  # Черный фон
        image_window.blit(image_to_display, (0, 0))  # Отображение изображения
        pygame.display.flip()  # Обновление окна

    # Закрытие окна
    pygame.display.quit()

default = buildings.construction("гравийная дорога", "300", 1, "10", 'images/road1.png')

# Основной цикл
running = True
while running:

    screen.fill((0, 0, 0))  # Черный фон
    screen.blit(background_image, (0, 0))  # Фоновое изображение

    # Отображение кнопок
    screen.blit(button_image, button_rect)  # Основная кнопка
    screen.blit(exit_button_image, exit_button_rect)  # Кнопка выхода



    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if button_rect.collidepoint(event.pos):
                main.game()

            if exit_button_rect.collidepoint(event.pos):  # Проверка нажатия на кнопку выхода
                running = False  # Выход из игры

    # Обновление экрана
    pygame.display.flip()

# Завершение работы
pygame.quit()
sys.exit()
