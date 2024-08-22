import pygame
import os

class Bullet:
    def __init__(self, x, y, image_path, direction):
        # Cargar y redimensionar la imagen de la bala
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (40, 10))  # Ajustar el tamaño de la bala
        
        # Rotar la imagen de la bala 90 grados para que se vea de forma vertical
        self.image = pygame.transform.rotate(self.image, 90)
        
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction  # 1 para abajo, -1 para arriba

    def update(self):
        self.rect.y += self.direction * 5  # Ajustar la velocidad según sea necesario

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)