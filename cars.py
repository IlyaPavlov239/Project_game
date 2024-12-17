import pygame



pygame.init()

class CarHor:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 50, 20)

    def move(self, x):
        if x==True
            self.rect.x += 5
        else:
            self.rect.x -= 5
        # Если машина выходит за пределы экрана, перемещаем её обратно вверх
        if self.rect.y > HEIGHT or self.rect.y<0 or self.rect.x > WIDTH or self.rect.x < 0:
            self.rect.y = random.randint(-100, -40)
            self.rect.x = random.choice([100, WIDTH - 100 - ROAD_WIDTH])  # Случайная позиция на дороге

    def draw(self, surface):
        pygame.draw.rect(surface, RED, self.rect)