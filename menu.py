import pygame


def run(screen):
    # Размеры окна
    WIDTH, HEIGHT = 1920, 1080

    # Инициализация шрифта
    font = pygame.font.Font("KellySlab-Regular.ttf", 80)  # Укажи путь к шрифту

    # Создание текстов кнопок
    start_text = font.render("START", True, (255, 255, 255))
    exit_text = font.render("EXIT", True, (255, 255, 255))

    # Определение кнопок
    start_button_rect = pygame.Rect(0, 0, 300, 100)
    exit_button_rect = pygame.Rect(250, 150, 200, 80)

    start_button_rect.center = (WIDTH // 2, HEIGHT // 2)

    running = True
    while running:
        screen.fill((255, 255, 255))  # Белый фон

        # Рисуем кнопку "START"
        pygame.draw.rect(screen, (0, 255, 0), start_button_rect, border_radius=20)
        start_text_rect = start_text.get_rect(center=start_button_rect.center)
        screen.blit(start_text, start_text_rect)

        # Рисуем кнопку "EXIT"
        pygame.draw.rect(screen, (255, 0, 0), exit_button_rect, border_radius=20)
        exit_text_rect = exit_text.get_rect(center=exit_button_rect.center)
        screen.blit(exit_text, exit_text_rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return "quit"
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if start_button_rect.collidepoint(mouse_pos):
                    return "game"
                elif exit_button_rect.collidepoint(mouse_pos):
                    return "quit"
