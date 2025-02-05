import pygame

def game_over(time):
    # Инициализация Pygame
    pygame.init()

    # Размеры окна
    WIDTH, HEIGHT = 1920, 1080
    # Создание окна
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    # Увеличенный шрифт
    font = pygame.font.Font("KellySlab-Regular.ttf", 80)  # Укажи путь к шрифту

    with open("record.txt", "r") as file:
        record = int(file.read())  # Читаем содержимое
    if time > record:
        record=time
        with open("record.txt", "w") as file:
            file.write(f"{record}")  # Читаем содержимое

    # Создание текстов (черного цвета, увеличенного размера)
    text1 = font.render("GAME OVER", True, (0, 0, 0))
    text2 = font.render(f"TIME: {time}", True, (0, 0, 0))
    text3 = font.render(f"RECORD: {record}", True, (0, 0, 0))  # Новый текст "RECORD"

    # Координаты для центрирования текста
    text1_rect = text1.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 150))
    text2_rect = text2.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
    text3_rect = text3.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))  # Размещаем ниже TIME

    # Увеличенные кнопки
    menu_button_rect = pygame.Rect(150, 100, 300, 100)  # "Menu" (в левом верхнем углу)
    retry_button_rect = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2 + 150, 300, 100)  # "Try Again"

    # Загрузка и проигрывание музыки
    pygame.mixer.music.load("music/game_over.mp3")  # Укажи путь к файлу музыки
    pygame.mixer.music.play(-1)  # -1 для зацикливания



    running = True
    while running:
        screen.fill((255, 255, 255))  # Белый фон

        # Отображаем текст
        screen.blit(text1, text1_rect)
        screen.blit(text2, text2_rect)
        screen.blit(text3, text3_rect)  # Отображаем рекорд

        # Рисуем кнопку "Menu" (увеличенный размер)
        pygame.draw.rect(screen, (0, 0, 255), menu_button_rect, border_radius=20)
        menu_text = font.render("Menu", True, (255, 255, 255))
        menu_text_rect = menu_text.get_rect(center=menu_button_rect.center)
        screen.blit(menu_text, menu_text_rect)

        # Рисуем кнопку "Попробовать снова" (увеличенный размер)
        pygame.draw.rect(screen, (0, 255, 0), retry_button_rect, border_radius=20)
        retry_text = font.render("Try Again", True, (0, 0, 0))
        retry_text_rect = retry_text.get_rect(center=retry_button_rect.center)
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
                    print("Going to Menu...")  # Тут можно добавить переход в меню
                    running = False
                # Проверка клика по кнопке "Попробовать снова"
                elif retry_button_rect.collidepoint(mouse_pos):
                    print("Restarting game...")  # Тут можно перезапустить игру

    pygame.quit()
