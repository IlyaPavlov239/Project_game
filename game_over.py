import pygame

def run(screen, time, difficulty):
    # Инициализация Pygame
    pygame.init()

    # Размеры окна
    WIDTH, HEIGHT = 1920, 1080

    # Увеличенный шрифт
    font = pygame.font.Font("KellySlab-Regular.ttf", 80)  # Укажи путь к шрифту

    # Чтение и обновление рекордов
    records = {}
    try:
        with open("record.txt", "r") as file:
            for line in file:
                if ":" in line:
                    key, value = line.strip().split(":")
                    records[key.strip()] = int(value.strip())
    except FileNotFoundError:
        pass  # Если файл не существует, создадим его позже

    # Проверка и обновление рекорда для текущего уровня сложности
    if difficulty in records:
        if time > records[difficulty]:
            records[difficulty] = time
    else:
        records[difficulty] = time

    # Запись обновленных рекордов в файл
    with open("record.txt", "w") as file:
        for key, value in records.items():
            file.write(f"{key}: {value}\n")

    # Текущий рекорд для отображения
    record = records[difficulty]

    # Создание текстов (черного цвета, увеличенного размера)
    text1 = font.render("GAME OVER", True, (0, 0, 0))  # "GAME OVER"
    text2 = font.render(f"TIME: {time}", True, (0, 0, 0))  # "TIME: #"
    text3 = font.render(f"DIFFICULTY: {difficulty.upper()}", True, (0, 0, 0))  # "DIFFICULTY: #"
    text4 = font.render(f"RECORD: {record}", True, (0, 0, 0))  # "RECORD: #"

    # Координаты для центрирования текста (подняты выше)
    text1_rect = text1.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 300))  # "GAME OVER"
    text2_rect = text2.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 200))  # "TIME: #"
    text3_rect = text3.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 100))  # "DIFFICULTY: #"
    text4_rect = text4.get_rect(center=(WIDTH // 2, HEIGHT // 2))  # "RECORD: #"

    # Увеличенные кнопки
    menu_button_rect = pygame.Rect(WIDTH/2, 700, 300, 100)  # "Menu" (в левом верхнем углу)
    retry_button_rect = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2 + 150, 400, 100)  # "Try Again"
    menu_button_rect.center = (WIDTH/2, HEIGHT // 2 + 150)  # Подняты выше на 50 пикселей
    retry_button_rect.center = (WIDTH/2, HEIGHT // 2 + 300)  # Подняты выше на 50 пикселей

    # Переменные для анимации кнопок
    menu_button_pressed = False
    retry_button_pressed = False
    menu_button_hovered = False
    retry_button_hovered = False

    running = True
    while running:
        screen.fill((255, 255, 255))  # Белый фон

        # Отображаем текст
        screen.blit(text1, text1_rect)  # "GAME OVER"
        screen.blit(text2, text2_rect)  # "TIME: #"
        screen.blit(text3, text3_rect)  # "DIFFICULTY: #"
        screen.blit(text4, text4_rect)  # "RECORD: #"

        # Получаем позицию мыши
        mouse_pos = pygame.mouse.get_pos()

        # Обработка наведения на кнопку "Menu"
        if menu_button_rect.collidepoint(mouse_pos):
            menu_button_hovered = True
            menu_button_color = (0, 0, 200)  # Темнее синий при наведении
        else:
            menu_button_hovered = False
            menu_button_color = (0, 0, 255)  # Обычный синий

        # Обработка наведения на кнопку "Попробовать снова"
        if retry_button_rect.collidepoint(mouse_pos):
            retry_button_hovered = True
            retry_button_color = (0, 200, 0)  # Темнее зеленый при наведении
        else:
            retry_button_hovered = False
            retry_button_color = (0, 255, 0)  # Обычный зеленый

        # Рисуем кнопку "Menu" (увеличенный размер)
        if menu_button_pressed:
            menu_button_color = (0, 0, 150)  # Еще темнее при нажатии
        pygame.draw.rect(screen, menu_button_color, menu_button_rect, border_radius=20)
        menu_text = font.render("Menu", True, (255, 255, 255))
        menu_text_rect = menu_text.get_rect(center=menu_button_rect.center)
        if menu_button_pressed:
            menu_text_rect.move_ip(5, 5)  # Смещение текста при нажатии
        screen.blit(menu_text, menu_text_rect)

        # Рисуем кнопку "Попробовать снова" (увеличенный размер)
        if retry_button_pressed:
            retry_button_color = (0, 150, 0)  # Еще темнее при нажатии
        pygame.draw.rect(screen, retry_button_color, retry_button_rect, border_radius=20)
        retry_text = font.render("Try Again", True, (255, 255, 255))
        retry_text_rect = retry_text.get_rect(center=retry_button_rect.center)
        if retry_button_pressed:
            retry_text_rect.move_ip(5, 5)  # Смещение текста при нажатии
        screen.blit(retry_text, retry_text_rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                # Проверка клика по кнопке "Menu"
                if menu_button_rect.collidepoint(mouse_pos):
                    menu_button_pressed = True
                # Проверка клика по кнопке "Попробовать снова"
                elif retry_button_rect.collidepoint(mouse_pos):
                    retry_button_pressed = True
            elif event.type == pygame.MOUSEBUTTONUP:
                mouse_pos = event.pos
                if menu_button_pressed:
                    menu_button_pressed = False
                    if menu_button_rect.collidepoint(mouse_pos):
                        return "menu"
                if retry_button_pressed:
                    retry_button_pressed = False
                    if retry_button_rect.collidepoint(mouse_pos):
                        return "game"