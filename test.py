import pygame

def rotate_surface(surface, angle):
    """
    Поворачивает объект Surface вокруг его центра на заданный угол.

    :param surface: pygame.Surface, объект для поворота.
    :param angle: Угол поворота в градусах (по часовой стрелке).
    :return: Новая повернутая поверхность (Surface).
    """
    # Поворачиваем поверхность
    rotated_surface = pygame.transform.rotate(surface, angle)
    return rotated_surface

# Пример использования
pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

# Создаем объект Surface
original_surface = pygame.Surface((100, 100), pygame.SRCALPHA)
original_surface.fill((255, 0, 0))  # Красный квадрат

# Устанавливаем его положение
rect = original_surface.get_rect(center=(400, 300))

angle = 0  # Начальный угол

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Очищаем экран
    screen.fill((0, 0, 0))  # Черный фон

    # Поворачиваем объект
    rotated_surface = rotate_surface(original_surface, angle)
    rotated_rect = rotated_surface.get_rect(center=rect.center)  # Центрируем повернутую поверхность

    # Отображаем объект
    screen.blit(rotated_surface, rotated_rect.topleft)

    # Увеличиваем угол
    angle = (angle + 1) % 360

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
