class Car:
    def __init__(self, direction, turn, orientation):
        if orientation == "horizontal":
            if direction == 1:
                x, y = 0, HEIGHT - 505
            else:
                x, y = WIDTH, 530
        else:
            if direction == 1:
                x, y = 950, 0
            else:
                x, y = WIDTH - 925, HEIGHT

        self.rect = pygame.Rect(x, y, 50, 20) if orientation == "horizontal" else pygame.Rect(x, y, 20, 50)
        self.direction = direction  # Направление движения (1 - вправо, -1 - влево / вверх, вниз)
        self.turn = turn  # Поворот (например, "up", "down", "forward")
        self.orientation = orientation  # Ориентация ("horizontal" или "vertical")
        self.angle = 0

        # Инициализация точек поворота в зависимости от направления и ориентации
        if orientation == "horizontal":
            if turn == "down":
                self.pov_x = 935
                self.pov_y = 0
            elif turn == "up":
                self.pov_x = WIDTH - 935
                self.pov_y = 0
            else:  # forward
                self.pov_x = WIDTH
                self.pov_y = HEIGHT // 2
        elif orientation == "vertical":
            if turn == "right":
                self.pov_x = 0
                self.pov_y = HEIGHT - 515
            elif turn == "left":
                self.pov_x = 0
                self.pov_y = 515
            else:  # forward
                self.pov_x = WIDTH // 2
                self.pov_y = HEIGHT

        self.original_surface = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        self.original_surface.fill((0, 0, 0))
        self.surface = self.original_surface

        # Флаг для остановки машины
        self.stopped = False

    def pos(self):
        return self.rect.topleft

    def move(self):
        # Если машина остановлена, ничего не делаем
        if self.stopped:
            return True

        if self.orientation == "horizontal":  # Движение по горизонтали
            if self.direction == 1:  # Движение вправо
                if self.rect.x < self.pov_x:
                    self.rect.x += 2
                else:
                    if self.turn == "up":
                        if self.angle < 90:
                            self.angle += 2
                            self.rect.y -= 2
                        else:
                            self.rect.y -= 2
                    elif self.turn == "down":
                        if self.angle > -90:
                            self.angle -= 2
                            self.rect.y += 2
                        else:
                            self.rect.y += 2
                    elif self.turn == "forward":
                        self.rect.x += 2
            elif self.direction == -1:
                if self.rect.x > self.pov_x:
                    self.rect.x -= 2
                else:
                    if self.turn == "up":
                        if self.angle > -90:
                            self.angle -= 2
                            self.rect.y -= 2
                        else:
                            self.rect.y -= 2
                    elif self.turn == "down":
                        if self.angle < 90:
                            self.angle += 2
                            self.rect.y += 2
                        else:
                            self.rect.y += 2
                    elif self.turn == "forward":
                        self.rect.x -= 2
        elif self.orientation == "vertical":
            if self.direction == 1:  # движение вниз
                if self.rect.y < self.pov_y:
                    self.rect.y += 2
                else:
                    if self.turn == "left":
                        if self.angle > -90:
                            self.angle -= 2
                            self.rect.x -= 2
                        else:
                            self.rect.x -= 2
                    elif self.turn == "right":
                        if self.angle < 90:
                            self.angle += 2
                            self.rect.x += 2
                        else:
                            self.rect.x += 2
                    elif self.turn == "forward":
                        self.rect.y += 2
            elif self.direction == -1:  # движение вверх
                if self.rect.y > self.pov_y:
                    self.rect.y -= 2
                else:
                    if self.turn == "left":
                        if self.angle < 90:
                            self.angle += 2
                            self.rect.x -= 2
                        else:
                            self.rect.x -= 2
                    elif self.turn == "right":
                        if self.angle > -90:
                            self.angle -= 2
                            self.rect.x += 2
                        else:
                            self.rect.x += 2
                    elif self.turn == "forward":
                        self.rect.y -= 2

        if self.rect.x > WIDTH or self.rect.x < 0 or self.rect.y < 0 or self.rect.y > HEIGHT:
            return False
        return True

    def draw(self, surface):
        rotated_surface = pygame.transform.rotozoom(self.original_surface, self.angle, 1)
        rotated_rect = rotated_surface.get_rect(center=self.rect.center)
        surface.blit(rotated_surface, rotated_rect.topleft)

    def stop(self):
        """Останавливает машину при вызове."""
        self.stopped = True

    def go(self):
        """Останавливает машину при вызове."""
        self.stopped = False