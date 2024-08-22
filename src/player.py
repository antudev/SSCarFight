import pygame
import os
from bullet import Bullet

class Player:
    def __init__(self, x, y, sounds):
        # Cargar la imagen del jugador
        image_path = os.path.join('assets', 'images', 'player.png')
        self.image = pygame.image.load(image_path).convert_alpha()
        
        # Ajustar el tamaño de la imagen del jugador
        self.image = pygame.transform.scale(self.image, (30, 50))  # Ajustar a 50x50 píxeles
        
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.health = 200  # Salud inicial del jugador
        self.top_reaches = 0  # Contador de veces que llega a la parte superior
        self.bullets = []
        self.sounds = sounds
        self.is_moving = False

    def move(self, dx, dy, game_started):
        self.rect.x += dx
        self.rect.y += dy
        
        # Verificar si el jugador ha alcanzado la parte superior del mapa
        if self.rect.top <= 0:
            self.rect.bottom = 600  # Reposicionar en la parte inferior del mapa
            self.top_reaches += 1  # Incrementar el contador
        
        # Reproducir sonido del motor si se está moviendo y el juego ha comenzado
        if game_started:
            if dx != 0 or dy != 0:
                if not self.is_moving:
                    self.sounds["player_car"].play(-1)  # Reproducir en bucle
                    self.is_moving = True
            else:
                if self.is_moving:
                    self.sounds["player_car"].stop()
                    self.is_moving = False
    
    def shoot(self):
        bullet_image_path = os.path.join('assets', 'images', 'bullet1.png')
        bullet = Bullet(self.rect.centerx, self.rect.top, bullet_image_path, -1)
        self.bullets.append(bullet)
        self.sounds["bullet"].play()  # Reproducir sonido de disparo
            
    def update(self, boss):
        for bullet in self.bullets:
            bullet.update()
            if bullet.rect.bottom < 0:
                self.bullets.remove(bullet)
            # Verificar colisión con el jefe
            if bullet.rect.colliderect(boss.rect):
                boss.health -= 10
                self.sounds["impact"].play()  # Reproducir sonido de impacto
                self.bullets.remove(bullet)

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)
        for bullet in self.bullets:
            bullet.draw(screen)
    
    def handle_movement(self, keys, game_started):
        # Movimiento del jugador (Flechas)
        if keys[pygame.K_UP]:
            self.move(0, -5, game_started)
        if keys[pygame.K_DOWN]:
            self.move(0, 5, game_started)
        if keys[pygame.K_LEFT]:
            self.move(-5, 0, game_started)
        if keys[pygame.K_RIGHT]:
            self.move(5, 0, game_started)
        if not (keys[pygame.K_UP] or keys[pygame.K_DOWN] or keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]):
            self.move(0, 0, game_started)  # Detener el sonido si no hay movimiento