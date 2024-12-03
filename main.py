def game():
    import pygame
    # Инициализация Pygame
    pygame.init()

    # Настройка экрана (полноэкранный режим)
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    width, height = screen.get_size()
    pygame.display.set_caption("Name of game")

    # Загрузка изображения фона
    background_image = pygame.image.load('images/background.png')  # Путь к вашему изображению
    bg_width, bg_height = background_image.get_size()

    # Начальная позиция фона
    bg_x, bg_y = 0, 0

    # Флаг для отслеживания состояния зажатой кнопки мыши
    dragging = False
    last_x, last_y = 0, 0  # Последняя позиция мыши, чтобы отслеживать движение

    # Основной цикл программы
    running=True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Обрабатываем зажатие кнопки мыши
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Левая кнопка мыши
                    dragging = True
                    last_x, last_y = event.pos  # Сохраняем начальную позицию мыши

            # Обрабатываем отпускание кнопки мыши
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:  # Левая кнопка мыши
                    dragging = False

            # Обрабатываем движение мыши
            if event.type == pygame.MOUSEMOTION:
                if dragging:
                    # Вычисляем смещение мыши
                    dx = event.pos[0] - last_x
                    dy = event.pos[1] - last_y
                    # Обновляем позицию фона
                    bg_x += dx
                    bg_y += dy
                    # Обновляем последнюю позицию мыши
                    last_x, last_y = event.pos

        # Отображаем фон, перемещая его на экран
        screen.fill((0, 0, 0))  # Заполняем экран черным цветом
        screen.blit(background_image, (bg_x, bg_y))  # Отображаем фон в новой позиции

        # Обновляем экран
        pygame.display.flip()

    # Завершение работы
    pygame.quit()
    sys.exit()
