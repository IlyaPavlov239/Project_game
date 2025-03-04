import pygame

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)  # Цвет кнопки
DARK_BLUE = (0, 0, 200)  # Темный синий для наведения
DARKER_BLUE = (0, 0, 150)  # Еще темнее синий для нажатия

def draw_text(screen, text, x, y, font, color=BLACK):
    """Функция для отображения текста на экране."""
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

def run(screen):
    """Основная функция, которая отображает инструкции на экране."""
    # Получаем размеры экрана
    WIDTH, HEIGHT = screen.get_size()

    # Загрузка изображений
    images = [
        pygame.image.load('images/inst1.png'),
        pygame.image.load('images/inst2.png'),
        pygame.image.load('images/inst3.png')
    ]

    # Тексты инструкций
    texts = [
        "Control traffic lights",
        "Prevent car accidents",
        "Keep track of the number of cars"
    ]

    # Масштабирование изображений
    scaled_images = []
    max_image_height = int(HEIGHT * 0.7)  # Изображение занимает 70% высоты экрана
    max_image_width = int(WIDTH * 0.8)  # Изображение занимает 80% ширины экрана

    for img in images:
        # Масштабируем изображение, сохраняя пропорции
        scale_factor = min(max_image_width / img.get_width(), max_image_height / img.get_height())
        new_width = int(img.get_width() * scale_factor)
        new_height = int(img.get_height() * scale_factor)
        scaled_images.append(pygame.transform.scale(img, (new_width, new_height)))

    # Загрузка шрифта
    try:
        font = pygame.font.Font("KellySlab-Regular.ttf", 45)  # Шрифт для текста
        arrow_font = pygame.font.Font("KellySlab-Regular.ttf", 60)  # Шрифт для стрелки
    except FileNotFoundError:
        print("Шрифт 'KellySlab-Regular.ttf' не найден. Убедитесь, что файл находится в правильной директории.")
        return "menu"  # Возвращаемся в меню, если шрифт не найден

    # Создание кнопки-стрелочки
    arrow_button_width = 150  # Ширина кнопки
    arrow_button_height = 100  # Высота кнопки
    arrow_button_rect = pygame.Rect(
        WIDTH - arrow_button_width - 230,  # Отступ справа 230 пикселей
        HEIGHT - arrow_button_height - 150,  # Отступ снизу 150 пикселей
        arrow_button_width,
        arrow_button_height
    )

    # Переменные для анимации кнопки
    arrow_button_pressed = False
    arrow_button_hovered = False

    # Основной цикл программы
    current_instruction = 0  # Текущая инструкция (0, 1, 2)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"  # Завершаем игру
            if event.type == pygame.MOUSEBUTTONDOWN:  # Обработка клика мыши
                if arrow_button_rect.collidepoint(event.pos):  # Если клик по кнопке-стрелочке
                    arrow_button_pressed = True
            if event.type == pygame.MOUSEBUTTONUP:  # Обработка отпускания кнопки мыши
                if arrow_button_pressed:
                    arrow_button_pressed = False
                    if arrow_button_rect.collidepoint(event.pos):  # Если отпустили на кнопке
                        current_instruction += 1  # Переход к следующей инструкции
                        if current_instruction >= len(images):  # Если инструкции закончились
                            return "menu"  # Возвращаемся в меню

        # Получаем позицию мыши
        mouse_pos = pygame.mouse.get_pos()

        # Обработка наведения на кнопку "Next"
        if arrow_button_rect.collidepoint(mouse_pos):
            arrow_button_hovered = True
            arrow_button_color = DARK_BLUE  # Темный синий при наведении
        else:
            arrow_button_hovered = False
            arrow_button_color = BLUE  # Обычный синий

        # Очистка экрана
        screen.fill(WHITE)

        # Отображение текущего изображения
        current_image = scaled_images[current_instruction]
        current_text = texts[current_instruction]

        # Центрируем изображение по горизонтали
        x_offset = (WIDTH - current_image.get_width()) // 2
        y_offset = 150  # Отступ сверху

        screen.blit(current_image, (x_offset, y_offset))

        # Отображение текста под изображением
        text_y = y_offset + current_image.get_height() - 60
        draw_text(screen, current_text, x_offset - 55, text_y, font)

        # Отрисовка кнопки-стрелочки
        if arrow_button_pressed:
            arrow_button_color = DARKER_BLUE  # Еще темнее синий при нажатии
        pygame.draw.rect(screen, arrow_button_color, arrow_button_rect, border_radius=20)  # Рисуем кнопку
        next_text = "Next"
        next_text_surface = arrow_font.render(next_text, True, WHITE)
        next_text_rect = next_text_surface.get_rect(center=arrow_button_rect.center)
        if arrow_button_pressed:
            next_text_rect.move_ip(5, 5)  # Смещение текста при нажатии
        screen.blit(next_text_surface, next_text_rect)

        # Обновление экрана
        pygame.display.flip()

    return "menu"  # Возвращаемся в меню после завершения