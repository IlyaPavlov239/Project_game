import pygame
import menu
import game
import game_over
import instruction  # Импортируем модуль с инструкциями

# Инициализация pygame
pygame.init()

# Настройки
WIDTH, HEIGHT = 1920, 1080
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Игра с меню")

# Переменная для хранения текущего состояния
state = "menu"
time = 0
running = True

# Основной игровой цикл
while running:
    if state == "menu":
        state = menu.run(screen)  # Передаем экран и получаем новое состояние
    elif state == "game":
        state, time = game.run(screen)  # Запускаем игровой процесс
    elif state == "game_over":
        state = game_over.run(screen, time)  # Экран окончания игры
    elif state == "instruction":  # Новое состояние для инструкций
        state = instruction.run(screen)  # Запуск экрана с инструкциями
    elif state == "quit":
        running = False  # Завершаем игру

pygame.quit()