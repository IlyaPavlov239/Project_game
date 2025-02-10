import pygame


def run(screen):
    font = pygame.font.Font(None, 50)
    clock = pygame.time.Clock()

    while True:
        screen.fill((30, 30, 30))

        title = font.render("Главное меню", True, (255, 255, 255))
        start_btn = font.render("Начать игру (Enter)", True, (200, 200, 200))
        quit_btn = font.render("Выход (Esc)", True, (200, 200, 200))

        screen.blit(title, (300, 150))
        screen.blit(start_btn, (250, 300))
        screen.blit(quit_btn, (250, 350))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Enter
                    return "game"
                if event.key == pygame.K_ESCAPE:  # Esc
                    return "quit"

        clock.tick(30)
