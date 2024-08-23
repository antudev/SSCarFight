import pygame
import time

class Menu:
    def __init__(self, sounds):
        self.font = pygame.font.Font('assets/fonts/MilkyVintage-Regular.ttf', 32)
        self.main_menu_options = ["Jugar", "Controles", "Salir"]
        self.pause_menu_options = ["Continuar", "Reiniciar", "Controles", "Salir"]
        self.options = self.main_menu_options
        self.selected_option = 0
        self.game_started = False
        self.show_controls = False
        self.confirm_exit = False
        self.paused = False
        self.restart_requested = False 
        self.sounds = sounds
        

    def update(self):
        pass

    def draw(self, screen):
        if self.show_controls:
            self.draw_controls(screen)
        elif self.confirm_exit:
            self.draw_confirm_exit(screen)
        elif self.paused:
            self.draw_pause_menu(screen)
        else:
            self.draw_menu(screen)
    
    def draw_menu(self, screen):
        for i, option in enumerate(self.options):
            color = (255, 255, 255) if i == self.selected_option else (100, 100, 100)
            text = self.font.render(option, True, color)
            rect = text.get_rect(center=(400, 300 + i * 50))
            screen.blit(text, rect)
            
    def draw_controls(self, screen):
        controls_text = [
            "Movimiento",
            "El jugador puede mover su coche utilizando las teclas de flechas",
            "Disparo",
            "Q"
        ]
        for i, line in enumerate(controls_text):
            text = self.font.render(line, True, (255, 255, 255))
            rect = text.get_rect(center=(400, 300 + i * 50))
            screen.blit(text, rect)
        back_text = self.font.render("Presiona Enter para volver", True, (255, 255, 255))
        back_rect = back_text.get_rect(center=(400, 500))
        screen.blit(back_text, back_rect)
    
    def draw_confirm_exit(self, screen):
        confirm_text = [
            "Salir del juego",
            "Cancelar"
        ]
        for i, line in enumerate(confirm_text):
            color = (255, 255, 255) if i == self.selected_option else (100, 100, 100)
            text = self.font.render(line, True, color)
            rect = text.get_rect(center=(400, 300 + i * 50))
            screen.blit(text, rect)

    def draw_pause_menu(self, screen):
        for i, option in enumerate(self.pause_menu_options):
            color = (255, 255, 255) if i == self.selected_option else (100, 100, 100)
            text = self.font.render(option, True, color)
            rect = text.get_rect(center=(400, 300 + i * 50))
            screen.blit(text, rect)
    
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.enter_pressed()
                
            elif event.key == pygame.K_UP:
                self.selected_option = (self.selected_option - 1) % len(self.options)
                self.sounds["menu_select"].play()
            elif event.key == pygame.K_DOWN:
                self.selected_option = (self.selected_option + 1) % len(self.options)
                self.sounds["menu_select"].play()
            elif event.key == pygame.K_ESCAPE and self.game_started:
                self.paused = not self.paused
                self.options = self.pause_menu_options if self.paused else self.main_menu_options
                self.selected_option = 0
                self.sounds["menu_select"].play()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            for i, option in enumerate(self.options):
                rect = pygame.Rect(300, 300 + i * 50 - 20, 200, 40)
                if rect.collidepoint(mouse_pos):
                    self.selected_option = i
                    self.sounds["menu_select"].play()
                    self.enter_pressed()

    def enter_pressed(self):
        if self.show_controls:
            self.show_controls = False
        elif self.confirm_exit:
            if self.selected_option == 0:  # Confirmar
                pygame.quit()
                exit()
            elif self.selected_option == 1:  # Cancelar
                self.confirm_exit = False
                self.options = self.pause_menu_options if self.paused else self.main_menu_options
                self.selected_option = 2  # Volver a la opción "Salir"
        else:
            if self.options == self.main_menu_options:
                if self.selected_option == 0:
                    self.start_countdown()
                elif self.selected_option == 1:
                    self.show_controls = True
                elif self.selected_option == 2:
                    self.confirm_exit = True
                    self.options = ["Confirmar", "Cancelar"]
                    self.selected_option = 0
            elif self.options == self.pause_menu_options:
                if self.selected_option == 0:
                    self.paused = False
                    self.options = self.pause_menu_options
                elif self.selected_option == 1:
                    self.restart_game()
                elif self.selected_option == 2:
                    self.show_controls = True
                elif self.selected_option == 3:
                    self.confirm_exit = True
                    self.options = ["Confirmar", "Cancelar"]
                    self.selected_option = 0

    def start_countdown(self):
        self.sounds["countdown"].play()
        for i in range(3, 0, -1):
            self.show_countdown(i)
            time.sleep(1)
        
        self.show_countdown("ya")
        time.sleep(1)
        self.game_started = True
        self.paused = False
        self.options = self.pause_menu_options
        print("Game Started!")  

    def show_countdown(self, text):
        screen = pygame.display.get_surface()
        background_image = pygame.Surface(screen.get_size())
        background_image.fill((0, 0, 0))  # Fondo negro
        screen.blit(background_image, (0, 0))
        countdown_text = self.font.render(str(text), True, (255, 255, 255))
        screen.blit(countdown_text, (400, 300))
        pygame.display.flip()

    def restart_game(self):
        self.restart_requested = True
        self.paused = False
        self.options = self.main_menu_options
        self.selected_option = 0
        print("Game Restarted!")  