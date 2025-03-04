import pygame

def run(screen):
    # Размеры окна
    WIDTH, HEIGHT = 1920, 1080

    # Инициализация шрифта
    font = pygame.font.Font("KellySlab-Regular.ttf", 80)  # Укажи путь к шрифту

    # Создание текстов кнопок
    start_text = font.render("START", True, (255, 255, 255))
    exit_text = font.render("EXIT", True, (255, 255, 255))
    instructions_text = font.render("HOW TO PLAY", True, (255, 255, 255))  # Текст для кнопки инструкций

    # Определение кнопок
    start_button_rect = pygame.Rect(0, 0, 300, 100)
    exit_button_rect = pygame.Rect(0, 0, 200, 80)
    instructions_button_rect = pygame.Rect(0, 0, 500, 100)  # Кнопка для инструкций

    # Центрирование кнопок
    start_button_rect.center = (WIDTH // 2, HEIGHT // 2 - 150)  # Кнопка START выше
    instructions_button_rect.center = (WIDTH // 2, HEIGHT // 2)  # Кнопка INSTRUCTIONS по центру
    exit_button_rect.center = (WIDTH // 2, HEIGHT // 2 + 150)  # Кнопка EXIT ниже

    # Переменные для анимации кнопок
    start_button_pressed = False
    exit_button_pressed = False
    instructions_button_pressed = False
    start_button_hovered = False
    exit_button_hovered = False
    instructions_button_hovered = False

    running = True
    while running:
        screen.fill((255, 255, 255))  # Белый фон

        # Получаем позицию мыши
        mouse_pos = pygame.mouse.get_pos()

        # Обработка наведения на кнопку "START"
        if start_button_rect.collidepoint(mouse_pos):
            start_button_hovered = True
            start_button_color = (0, 200, 0)  # Темнее зеленый при наведении
        else:
            start_button_hovered = False
            start_button_color = (0, 255, 0)  # Обычный зеленый

        # Обработка наведения на кнопку "INSTRUCTIONS"
        if instructions_button_rect.collidepoint(mouse_pos):
            instructions_button_hovered = True
            instructions_button_color = (0, 0, 200)  # Темнее синий при наведении
        else:
            instructions_button_hovered = False
            instructions_button_color = (0, 0, 255)  # Обычный синий

        # Обработка наведения на кнопку "EXIT"
        if exit_button_rect.collidepoint(mouse_pos):
            exit_button_hovered = True
            exit_button_color = (200, 0, 0)  # Темнее красный при наведении
        else:
            exit_button_hovered = False
            exit_button_color = (255, 0, 0)  # Обычный красный

        # Рисуем кнопку "START"
        if start_button_pressed:
            start_button_color = (0, 150, 0)  # Еще темнее при нажатии
        pygame.draw.rect(screen, start_button_color, start_button_rect, border_radius=20)
        start_text_rect = start_text.get_rect(center=start_button_rect.center)
        if start_button_pressed:
            start_text_rect.move_ip(5, 5)  # Смещение текста при нажатии
        screen.blit(start_text, start_text_rect)

        # Рисуем кнопку "INSTRUCTIONS"
        if instructions_button_pressed:
            instructions_button_color = (0, 0, 150)  # Еще темнее при нажатии
        pygame.draw.rect(screen, instructions_button_color, instructions_button_rect, border_radius=20)
        instructions_text_rect = instructions_text.get_rect(center=instructions_button_rect.center)
        if instructions_button_pressed:
            instructions_text_rect.move_ip(5, 5)  # Смещение текста при нажатии
        screen.blit(instructions_text, instructions_text_rect)

        # Рисуем кнопку "EXIT"
        if exit_button_pressed:
            exit_button_color = (150, 0, 0)  # Еще темнее при нажатии
        pygame.draw.rect(screen, exit_button_color, exit_button_rect, border_radius=20)
        exit_text_rect = exit_text.get_rect(center=exit_button_rect.center)
        if exit_button_pressed:
            exit_text_rect.move_ip(5, 5)  # Смещение текста при нажатии
        screen.blit(exit_text, exit_text_rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return "quit"
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                # Проверка клика по кнопке "START"
                if start_button_rect.collidepoint(mouse_pos):
                    start_button_pressed = True
                # Проверка клика по кнопке "INSTRUCTIONS"
                elif instructions_button_rect.collidepoint(mouse_pos):
                    instructions_button_pressed = True
                # Проверка клика по кнопке "EXIT"
                elif exit_button_rect.collidepoint(mouse_pos):
                    exit_button_pressed = True
            elif event.type == pygame.MOUSEBUTTONUP:
                mouse_pos = event.pos
                if start_button_pressed:
                    start_button_pressed = False
                    if start_button_rect.collidepoint(mouse_pos):
                        return "difficult"
                if instructions_button_pressed:
                    instructions_button_pressed = False
                    if instructions_button_rect.collidepoint(mouse_pos):
                        return "instruction"  # Переход в раздел с инструкциями
                if exit_button_pressed:
                    exit_button_pressed = False
                    if exit_button_rect.collidepoint(mouse_pos):
                        return "quit"