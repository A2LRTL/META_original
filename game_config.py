import os
import pygame
import time

main_dir = os.path.dirname(os.path.abspath(__file__))

# Paths
music_path = os.path.join(main_dir, 'assets', 'audio', 'music.mp3')
sword_fx_path = os.path.join(main_dir, 'assets', 'audio', 'sword.wav')
magic_fx_path = os.path.join(main_dir, 'assets', 'audio', 'magic.wav')
bg_image_path = os.path.join(main_dir, 'assets', 'images', 'background', 'background.png')
warrior_sheet_path = os.path.join(main_dir, 'assets', 'images', 'warrior', 'Sprites', 'warrior.png')
wizard_sheet_path = os.path.join(main_dir, 'assets', 'images', 'wizard', 'Sprites', 'wizard.png')
victory_img_path = os.path.join(main_dir, 'assets', 'images', 'icons', 'victory.png')
count_font_path = os.path.join(main_dir, 'assets', 'fonts', 'PermanentMarker-Regular.ttf')
round_font_path = os.path.join(main_dir, 'assets', 'fonts', 'PermanentMarker-Regular.ttf')
score_font_path = os.path.join(main_dir, 'assets', 'fonts', 'PressStart2P-Regular.ttf')  # Change if needed
data_panel_image_path=os.path.join(main_dir, 'assets', 'images', 'dataPanel', 'dataPanel.png')
# Screen dimensions
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

# Colors
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
GRAY = (100,100,100)

# Game variables
intro_count = 3
round_over = False
score = [0, 0]  # player scores. [P1, P2]
ROUND_OVER_COOLDOWN = 2000

#Initialisation:
FIGHTERS_INITIAL_POSITION=[200, 310, 720, 310]

# Helper functions
def draw_text(screen, text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect.topleft)


def draw_bg(screen, bg_image):
    scaled_bg = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.blit(scaled_bg, (0, 0))

def draw_health_bar(screen, fighter, health, x, y):
    lengthbar = 400
    lengthbar_under = 300
    ratio = health / 100

    if ratio > 0.5:
        lengthbar_top = (ratio - 0.5) * 2 * lengthbar
        lengthbar_bottom = lengthbar_under
    else:
        lengthbar_top = 0
        lengthbar_bottom = (ratio * 2) * lengthbar_under

    if fighter == 1:
        # Top bar
        pygame.draw.polygon(screen, WHITE, ((x-1+20, y), (x-1+lengthbar-20, y), (x-1+lengthbar-20, y+30), (x-1+50, y+30)))
        pygame.draw.polygon(screen, GRAY, ((x-1+20, y), (x-1+lengthbar-20, y), (x-1+lengthbar-20, y+30), (x-1+50, y+30)), 2)

        if health < 100:
            pygame.draw.rect(screen, YELLOW, (x + lengthbar - lengthbar_top + 20, y, lengthbar_top - 40, 30))
        else : 
            pygame.draw.polygon(screen, YELLOW, ((x + lengthbar - lengthbar_top + 20, y), (x + lengthbar - 20, y),
                                      (x + lengthbar - 20, y + 30), (x + lengthbar - lengthbar_top + 50, y + 30)))

        # Under bar
        pygame.draw.polygon(screen, WHITE, ((x-1+lengthbar-lengthbar_under-30, y+32), (x-1+lengthbar-20, y+32), (x-1+lengthbar-20, y+50), (x-1+lengthbar-lengthbar_under, y+50)))
        pygame.draw.polygon(screen, GRAY, ((x-1+lengthbar-lengthbar_under-30, y+32), (x-1+lengthbar-20, y+32), (x-1+lengthbar-20, y+50), (x-1+lengthbar-lengthbar_under, y+50)), 2)

        if health < 50:
            pygame.draw.rect(screen, YELLOW, (x - 1 + lengthbar - lengthbar_bottom - 30, y + 32, lengthbar_bottom + 10, 18))
        else : 
            pygame.draw.polygon(screen, YELLOW, ((x - 1 + lengthbar - lengthbar_bottom - 30, y + 32), (x - 1 + lengthbar - 20, y + 32),
                                      (x - 1 + lengthbar - 20, y + 50), (x - 1 + lengthbar - lengthbar_bottom, y + 50)))
       
    if fighter == 2:
        # Top bar
        pygame.draw.polygon(screen, WHITE, ((x-1+20, y), (x-1+lengthbar-60, y), (x-1+lengthbar-60-20, y+30), (x-1+20, y+30)))
        pygame.draw.polygon(screen, GRAY, ((x-1+20, y), (x-1+lengthbar-60, y), (x-1+lengthbar-60-20, y+30), (x-1+20, y+30)), 2)

        if health < 100:
            pygame.draw.rect(screen, YELLOW, (x + 20, y, lengthbar_top - 60, 30))
        else : 
            pygame.draw.polygon(screen, YELLOW, ((x + 20, y), (x + lengthbar_top-60, y),
                                      (x + lengthbar_top - 60 - 20 , y + 30), (x + 20, y + 30)))

        # Under bar
        pygame.draw.polygon(screen, WHITE, ((x-1+20, y+32), (x-1+lengthbar_under+10, y+32), (x-1+lengthbar_under+10-20, y+50), (x-1+20, y+50)))
        pygame.draw.polygon(screen, GRAY,((x-1+20,y+32),(x-1+lengthbar_under+10,y+32),(x-1+lengthbar_under+10-20,y+50),(x-1+20,y+50)),2)
        
        if health < 50:
            pygame.draw.rect(screen, YELLOW, (x -1 + 20, y+32, lengthbar_bottom - 60, 18))
        else : 
            pygame.draw.polygon(screen, YELLOW, ((x - 1 + 20, y + 32), (x - 1 + lengthbar_bottom + 10, y + 32),
                                      (x - 1 + lengthbar_bottom + 10 - 20, y + 50), (x - 1 + 20, y + 50)))
               
def draw_round_data(screen, round_font, round, time_text,dataPanel_Image):
    #pygame.draw.rect(screen, GRAY,(SCREEN_WIDTH // 2-150,10,300,100))
    dataPanel_scaled = pygame.transform.scale(dataPanel_Image, (390, 130))
    screen.blit(dataPanel_scaled, (SCREEN_WIDTH // 2 - 195, 15))
    textRound = round_font.render("Round {}".format(int(round)), True, (255, 255, 255))
    screen.blit(textRound, (SCREEN_WIDTH // 2 - textRound.get_width() // 2, 5 ))
    textTimer = round_font.render("{}".format(int(time_text)), True, (255, 255, 255))
    screen.blit(textTimer, (SCREEN_WIDTH // 2 - textTimer.get_width() // 2, textRound.get_height()))

def process_round(screen, draw_round_data, round_font, count_font, victory_font, round_over, counter, intro_count, round, time_left, elapsed_time, countdown_time, start_time, fighter1, fighter2, score, last_count_update, data_panel_image):
    elapsed_time = time.time() - start_time
    time_left = countdown_time - elapsed_time

    if intro_count <= 0:
       
        if not round_over:
            # Move fighters
            fighter1.move(SCREEN_WIDTH, SCREEN_HEIGHT, fighter2, round_over)
            fighter2.move(SCREEN_WIDTH, SCREEN_HEIGHT, fighter1, round_over)
            # Countdown
            draw_round_data(screen, round_font, round, time_left, data_panel_image)

        if time_left < 0 or not (fighter1.alive and fighter2.alive):
            counter +=1
            if not round_over:
                if not fighter1.alive:
                    score[1] += 1
                elif not fighter2.alive:
                    score[0] += 1
                
                if score[0] >= 2:
                    draw_text(screen, "Fighter 1 Wins!", victory_font, RED, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3)
                    # Here you can add logic to terminate the game or transition to another screen

                elif score[1] >= 2:
                    draw_text(screen, "Fighter 2 Wins!", victory_font, RED, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3)
                    # Here you can add logic to terminate the game or transition to another screen

                round_over = True
                

            if counter > 100:
                # Reinitialize the fighters' positions and health
                fighter1.rect.x, fighter1.rect.y = FIGHTERS_INITIAL_POSITION[0], FIGHTERS_INITIAL_POSITION[1]
                fighter2.rect.x, fighter2.rect.y = FIGHTERS_INITIAL_POSITION[2], FIGHTERS_INITIAL_POSITION[3]
                fighter1.alive, fighter1.health = True, 100
                fighter2.alive, fighter2.health = True, 100
                round += 1
                time_left = countdown_time
                elapsed_time = 0
                start_time = time.time() + 3
                round_over = False
                intro_count = 3
                counter = 0

    else:
        draw_round_data(screen, round_font, round, countdown_time, data_panel_image)
        # Display count timer
        draw_text(screen, str(intro_count), count_font, RED, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3)
        # Update count timer
        if (pygame.time.get_ticks() - last_count_update) >= 1000:
            intro_count -= 1
            last_count_update = pygame.time.get_ticks()

    # Return the modified values
    return round_over, counter, intro_count, round, time_left, elapsed_time, start_time, last_count_update
