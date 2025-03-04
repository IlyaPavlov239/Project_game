import pygame

def run(screen):
    # Инициализация Pygame
    pygame.init()

    # Цвета
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GRAY = (128, 128, 128)
    BLUE = (0, 0, 255)
    DARK_BLUE = (0, 0, 200)
    DARKER_BLUE = (0, 0, 150)
    GREEN = (0, 255, 0)
    DARK_GREEN = (0, 200, 0)
    DARKER_GREEN = (0, 150, 0)
    RED = (255, 0, 0)
    DARK_RED = (200, 0, 0)
    DARKER_RED = (150, 0, 0)

    # Размеры окна
    WIDTH, HEIGHT = 1920, 1080


    # Шрифты
    font = pygame.font.Font("KellySlab-Regular.ttf", 80)  # Укажи путь к шрифту
    title_font = pygame.font.Font("KellySlab-Regular.ttf", 100)  # Шрифт для заголовка

    # Текст заголовка
    title_text = title_font.render("Select Difficulty Level", True, BLACK)
    title_rect = title_text.get_rect(center=(WIDTH // 2, 200))

    # Кнопки
    easy_button_rect = pygame.Rect(0, 0, 300, 100)
    medium_button_rect = pygame.Rect(0, 0, 400, 100)
    hard_button_rect = pygame.Rect(0, 0, 300, 100)

    # Центрирование кнопок с большим отступом
    easy_button_rect.center = (WIDTH // 2, HEIGHT // 2 - 150)  # Кнопка "Easy" выше
    medium_button_rect.center = (WIDTH // 2, HEIGHT // 2)      # Кнопка "Medium" по центру
    hard_button_rect.center = (WIDTH // 2, HEIGHT // 2 + 150)  # Кнопка "Hard" ниже

    # Тексты кнопок
    easy_text = font.render("Easy", True, WHITE)
    medium_text = font.render("Medium", True, WHITE)
    hard_text = font.render("Hard", True, WHITE)

    # Переменные для анимации кнопок
    easy_button_pressed = False
    medium_button_pressed = False
    hard_button_pressed = False
    easy_button_hovered = False
    medium_button_hovered = False
    hard_button_hovered = False

    # Основной цикл программы
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if easy_button_rect.collidepoint(mouse_pos):
                    easy_button_pressed = True
                elif medium_button_rect.collidepoint(mouse_pos):
                    medium_button_pressed = True
                elif hard_button_rect.collidepoint(mouse_pos):
                    hard_button_pressed = True
            elif event.type == pygame.MOUSEBUTTONUP:
                mouse_pos = event.pos
                if easy_button_pressed and easy_button_rect.collidepoint(mouse_pos):
                    print("Easy difficulty selected")
                    easy_button_pressed = False
                    return ("game", "easy")
                elif medium_button_pressed and medium_button_rect.collidepoint(mouse_pos):
                    print("Medium difficulty selected")
                    medium_button_pressed = False
                    return ("game", "medium")
                elif hard_button_pressed and hard_button_rect.collidepoint(mouse_pos):
                    print("Hard difficulty selected")
                    hard_button_pressed = False
                    return ("game", "hard")
                easy_button_pressed = False
                medium_button_pressed = False
                hard_button_pressed = False

        # Получаем позицию мыши
        mouse_pos = pygame.mouse.get_pos()

        # Обработка наведения на кнопки
        easy_button_hovered = easy_button_rect.collidepoint(mouse_pos)
        medium_button_hovered = medium_button_rect.collidepoint(mouse_pos)
        hard_button_hovered = hard_button_rect.collidepoint(mouse_pos)

        # Очистка экрана
        screen.fill(WHITE)

        # Отображение заголовка
        screen.blit(title_text, title_rect)

        # Рисуем кнопку "Easy"
        easy_button_color = DARK_GREEN if easy_button_hovered else GREEN
        if easy_button_pressed:
            easy_button_color = DARKER_GREEN
        pygame.draw.rect(screen, easy_button_color, easy_button_rect, border_radius=20)
        easy_text_rect = easy_text.get_rect(center=easy_button_rect.center)
        if easy_button_pressed:
            easy_text_rect.move_ip(5, 5)  # Смещение текста при нажатии
        screen.blit(easy_text, easy_text_rect)

        # Рисуем кнопку "Medium"
        medium_button_color = DARK_BLUE if medium_button_hovered else BLUE
        if medium_button_pressed:
            medium_button_color = DARKER_BLUE
        pygame.draw.rect(screen, medium_button_color, medium_button_rect, border_radius=20)
        medium_text_rect = medium_text.get_rect(center=medium_button_rect.center)
        if medium_button_pressed:
            medium_text_rect.move_ip(5, 5)  # Смещение текста при нажатии
        screen.blit(medium_text, medium_text_rect)

        # Рисуем кнопку "Hard"
        hard_button_color = DARK_RED if hard_button_hovered else RED
        if hard_button_pressed:
            hard_button_color = DARKER_RED
        pygame.draw.rect(screen, hard_button_color, hard_button_rect, border_radius=20)
        hard_text_rect = hard_text.get_rect(center=hard_button_rect.center)
        if hard_button_pressed:
            hard_text_rect.move_ip(5, 5)  # Смещение текста при нажатии
        screen.blit(hard_text, hard_text_rect)

        # Обновление экрана
        pygame.display.flip()

