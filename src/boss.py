import pygame
import os
import random
from bullet import Bullet

class Boss:
    def __init__(self, x, y, sounds):
        # Cargar la imagen del jefe
        image_path = os.path.join('assets', 'images', 'boss.png')
        self.image = pygame.image.load(image_path).convert_alpha()
        
        # Ajustar el tamaño de la imagen del jugador
        self.image = pygame.transform.scale(self.image, (30, 50))  # Ajustar a 30x50 píxeles
        
        self.rect = self.image.get_rect()
        self.rect.topleft = (300, 500)  # Posición inicial
        self.direction_y = 1  # 1 para abajo, -1 para arriba
        self.direction_x = 1  # 1 para derecha, -1 para izquierda
        self.health = 100  # Salud inicial del boss
        self.top_reaches = 0  # Contador de veces que llega a la parte superior
        self.bullets = []  # Lista de balas disparadas por el jefe
        self.move_sideways = False  # Bandera para mover hacia los lados
        self.sounds = sounds
        self.is_moving = False
                
    def move(self, dx, dy, game_started):
        self.rect.x += dx
        self.rect.y += dy
        
        # Reproducir sonido del motor si se está moviendo y el juego ha comenzado
        if game_started:
            if dx != 0 or dy != 0:
                if not self.is_moving:
                    self.sounds["boss_car"].play(-1)  # Reproducir en bucle
                    self.is_moving = True
            else:
                if self.is_moving:
                    self.sounds["boss_car"].stop()
                    self.is_moving = False

    def update(self, player):
        # Actualizar las balas
        for bullet in self.bullets:
            bullet.update()
            # Eliminar la bala si sale de la pantalla
            if bullet.rect.bottom < 0 or bullet.rect.top > 600:
                self.bullets.remove(bullet)
            # Verificar colisión con el jugador
            if bullet.rect.colliderect(player.rect):
                player.health -= 10
                self.sounds["impact"].play()  # Reproducir sonido de impacto
                self.bullets.remove(bullet)
        
        # Verificar si el jugador ha disparado
        for bullet in player.bullets:
            if bullet.rect.colliderect(self.rect):
                self.move_sideways = True
                break
            
        # Mover hacia los lados si es necesario
        if self.move_sideways:
            if self.rect.left <= 0:
                self.direction_x = 1  # Cambiar dirección hacia la derecha
            elif self.rect.right >= 800:
                self.direction_x = -1  # Cambiar dirección hacia la izquierda
            self.move(self.direction_x * 3, 0)  # Mover solo en la dirección X

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)
        for bullet in self.bullets:
            bullet.draw(screen)
        
    def auto_move(self, game_started):
        # Movimiento automático: el jefe se mueve hacia arriba y hacia abajo
        if self.rect.top <= 0:
            self.rect.bottom = 600  # Reposicionar en la parte inferior
            self.top_reaches += 1  # Incrementar el contador
        elif self.rect.bottom >= 600:
            self.direction_y = -1  # Cambiar dirección hacia arriba
        
        
        self.move(0, self.direction_y * 4, game_started)  # Mover solo en la dirección Y, el numero entero "4" se encarga de la velocidad de el defe
               
    def shoot(self, player):
        # Disparar una bala solo si el jugador está directamente frente al jefe
        if abs(self.rect.centerx - player.rect.centerx) < 10:  # Ajustar el umbral según sea necesario
            if random.random() < 0.10:  # 10% de probabilidad de disparar en cada fotograma
                bullet = Bullet(self.rect.centerx, self.rect.top, 'assets/images/bullet3.png', -1)
                self.bullets.append(bullet)
                self.sounds["bullet"].play()  # Reproducir sonido de disparo