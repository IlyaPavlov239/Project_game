import pygame


# Инициализация Pygame
pygame.init()

class construction:     #класс для всех сооружений моей игры:дороги, железные дороги, порты



    def __init__(self, name, price, capacity, service,image,):
        self.name = name
        self.price = price
        self.capacity = capacity
        self.service = service
        self.image = pygame.image.load(image)


    def build(self,position, screen):
        image_rect = self.image.get_rect()
        image_rect.topleft = position
        screen.blit(self.image, image_rect)
        #как сделать уменьшение денег в игре прямо в классе?

