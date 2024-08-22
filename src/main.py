import sys
import os
import pygame

# Directorio 'src' 
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from player import Player
from boss import Boss
from menu import Menu

# Mezclador de sonido 
pygame.mixer.init()

# Cargar sonidos
boss_car_sound = pygame.mixer.Sound(os.path.join('assets', 'sounds', 'bosscarsound.wav'))
player_car_sound = pygame.mixer.Sound(os.path.join('assets', 'sounds', 'playercarsound.wav'))
car_explosion_sound = pygame.mixer.Sound(os.path.join('assets', 'sounds', 'carexplosion.wav'))
countdown_fx = pygame.mixer.Sound(os.path.join('assets', 'sounds', 'countdownfx.wav'))
impact_fx = pygame.mixer.Sound(os.path.join('assets', 'sounds', 'impactfx.wav'))
win_sound = pygame.mixer.Sound(os.path.join('assets', 'sounds', 'winsound.wav'))
lose_sound = pygame.mixer.Sound(os.path.join('assets', 'sounds', 'losesound.wav'))
menu_select_fx = pygame.mixer.Sound(os.path.join('assets', 'sounds', 'menuselectfx.wav'))
bullet_sound = pygame.mixer.Sound(os.path.join('assets', 'sounds', 'bullet.wav'))

# Lista de sonidos
sounds = {
    "boss_car": boss_car_sound,
    "player_car": player_car_sound,
    "car_explosion": car_explosion_sound,
    "countdown": countdown_fx,
    "impact": impact_fx,
    "win": win_sound,
    "lose": lose_sound,
    "menu_select": menu_select_fx,
    "bullet": bullet_sound
}

def reset_game():
    global player, boss, show_finish_line, boss_visible
    player = Player(x=500, y=500, sounds=sounds)  # Posición inicial del jugador
    boss = Boss(x=300, y=500, sounds=sounds)      # Posición inicial del jefe
    show_finish_line = False  # Reiniciar la bandera de la línea de meta
    boss_visible = True  # Reiniciar la visibilidad del jefe

def stop_engine_sounds():
    sounds["player_car"].stop()
    sounds["boss_car"].stop()
    
def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("SSCarFight")
    clock = pygame.time.Clock()
    running = True
    
    # Cargar la imagen de fondo
    background_image = pygame.image.load(os.path.join('assets', 'images', 'background.png')).convert()

    global player, boss, menu, show_finish_line, boss_visible
    player = Player(x=500, y=500, sounds=sounds)  # Posición inicial del jugador
    boss = Boss(x=300, y=500, sounds=sounds)      # Posición inicial del jefe
    menu = Menu(sounds=sounds)
    
    finish_line_y = 50  # Posición de la línea de meta en el eje Y
    show_finish_line = False  # Bandera para mostrar la línea de meta
    boss_visible = True  # Bandera para controlar la visibilidad del jefe
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    player.shoot()
            menu.handle_event(event)

        keys = pygame.key.get_pressed()
        
        if not menu.paused:
        
            # Movimiento del jugador 
            player.handle_movement(keys, menu.game_started)

            # Movimiento automático del jefe
            boss.auto_move(menu.game_started)
            boss.shoot(player)  # Hacer que el jefe dispare balas
            
            # Dibujar la imagen de fondo
            screen.blit(background_image, (0, 0))
            
            # Verificar si se debe mostrar la línea de meta
            if player.top_reaches >= 10 or boss.top_reaches >= 10:
                show_finish_line = True
            
            # Dibujar la línea de meta si es necesario
            if show_finish_line:
                square_size = 20  # Tamaño de cada cuadro
                num_squares = screen.get_width() // square_size  # Número de cuadros necesarios para cubrir el ancho de la pantalla
                for row in range(2):  # Dibujar dos filas
                    for i in range(num_squares):
                        color = (255, 255, 255) if (i + row) % 2 == 0 else (0, 0, 0)  # Alternar entre blanco y negro
                        pygame.draw.rect(screen, color, (i * square_size, finish_line_y + row * square_size, square_size, square_size))

            def show_message(screen, message):
                font = pygame.font.Font('assets/fonts/MilkyVintage-Regular.ttf', 74)
                text = font.render(message, True, (255, 255, 255))
                text_rect = text.get_rect(center=(screen.get_width() / 2, screen.get_height() / 2))
                screen.blit(text, text_rect)
                pygame.display.flip()
                pygame.time.wait(2000)  # Esperar 2 segundos para que el jugador vea el mensaje
                    
            if menu.game_started:
                player.update(boss)
                boss.update(player)
                player.draw(screen)
                
                # Actualizar la visibilidad del jefe
                if player.top_reaches > boss.top_reaches:
                    boss_visible = False
                elif boss.top_reaches > player.top_reaches:
                    boss_visible = False
                else:
                    boss_visible = True
                
                # Dibujar al jefe solo si es visible
                if boss_visible:
                    boss.draw(screen)
                
                # Verificar si algún vehículo ha cruzado la línea de meta
                if show_finish_line:
                    if player.top_reaches > boss.top_reaches:  # Comparar cuántas vueltas completaron
                        if player.rect.top <= finish_line_y:
                            stop_engine_sounds()
                            sounds["win"].play() 
                            print("Player wins!")
                            show_message(screen, "1° LUGAR!")
                            menu.game_started = False  # Volver al menú principal
                            menu.paused = False  # Asegurarse de que el menú no esté en pausa
                            reset_game()  # Reiniciar el juego
                    elif boss.top_reaches > player.top_reaches:
                        if boss.rect.top <= finish_line_y:
                            stop_engine_sounds()
                            print("Boss wins!")
                            sounds["lose"].play() 
                            show_message(screen, "2° LUGAR!")
                            menu.game_started = False  # Volver al menú principal
                            menu.paused = False  # Asegurarse de que el menú no esté en pausa
                            reset_game()  # Reiniciar el juego
                    else:  # Ambos tienen las mismas vueltas
                        if player.rect.top <= finish_line_y and boss.rect.top <= finish_line_y:
                            # Si ambos llegan a la meta al mismo tiempo
                            stop_engine_sounds()
                            sounds["win"].play() 
                            if player.rect.top < boss.rect.top:
                                print("Draw!")
                                show_message(screen, "Empate!")
                            else:
                                print("Draw!")
                                show_message(screen, "Empate!")
                            menu.game_started = False  # Volver al menú principal
                            menu.paused = False  # Asegurarse de que el menú no esté en pausa
                            reset_game()  # Reiniciar el juego
                        elif player.rect.top <= finish_line_y:  # Solo el jugador cruzó la meta
                            stop_engine_sounds()
                            sounds["win"].play() 
                            print("Player wins!")
                            show_message(screen, "1° LUGAR!")
                            menu.game_started = False  # Volver al menú principal
                            menu.paused = False  # Asegurarse de que el menú no esté en pausa
                            reset_game()  # Reiniciar el juego
                        elif boss.rect.top <= finish_line_y:  # Solo el jefe cruzó la meta
                            stop_engine_sounds()
                            sounds["lose"].play() 
                            print("Boss wins!")
                            show_message(screen, "2° LUGAR!")
                            menu.game_started = False  # Volver al menú principal
                            menu.paused = False  # Asegurarse de que el menú no esté en pausa
                            reset_game()  # Reiniciar el juego
                
                # Verificar si algún vehículo ha sido destruido
                if player.health <= 0:
                    stop_engine_sounds()
                    sounds["car_explosion"].play()
                    sounds["lose"].play() 
                    print("Boss wins!")
                    show_message(screen, "Boss te ha destruido!")
                    menu.game_started = False  # Volver al menú principal
                    menu.paused = False  # Asegurarse de que el menú no esté en pausa
                    reset_game()  # Reiniciar el juego
                elif boss.health <= 0:
                    stop_engine_sounds()
                    sounds["car_explosion"].play()
                    sounds["win"].play() 
                    print("Player wins!")
                    show_message(screen, "Haz destruido a Boss!")
                    menu.game_started = False  # Volver al menú principal
                    menu.paused = False  # Asegurarse de que el menú no esté en pausa
                    reset_game()  # Reiniciar el juego
            else:
                menu.update()
                menu.draw(screen)

        else:
            # Dibujar el menú de pausa
            screen.blit(background_image, (0, 0))  # Redibujar el fondo
            menu.draw(screen)
        
        # Verificar si se ha solicitado reiniciar el juego
        if menu.restart_requested:
            reset_game()
            menu.restart_requested = False
        
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()