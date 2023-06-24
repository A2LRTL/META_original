import pygame
from pygame import mixer
from fighter import *
from game_config import *
import json
from custom_sprite_group import CustomSpriteGroup


mixer.init()
pygame.init()

# Create game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Brawler")

# Set framerate
clock = pygame.time.Clock()
FPS = 60

# Load music and sounds
pygame.mixer.music.load(music_path)
pygame.mixer.music.set_volume(0.15)
pygame.mixer.music.play(-1, 0.0, 5000)
sword_fx = pygame.mixer.Sound(sword_fx_path)
sword_fx.set_volume(0.5)
magic_fx = pygame.mixer.Sound(magic_fx_path)
magic_fx.set_volume(0.5)

# Load background image
bg_image = pygame.image.load(bg_image_path).convert_alpha()
data_panel_image = pygame.image.load(data_panel_image_path).convert_alpha()
# Load spritesheets
warrior_sheet = pygame.image.load(warrior_sheet_path).convert_alpha()
wizard_sheet = pygame.image.load(wizard_sheet_path).convert_alpha()

# Load victory image
victory_img = pygame.image.load(victory_img_path).convert_alpha()


# Define font
count_font = pygame.font.Font(count_font_path, 50)
round_font = pygame.font.Font(round_font_path, 50)
score_font = pygame.font.Font(score_font_path, 60)
victory_font = pygame.font.Font(score_font_path, 60)  # Add this line

# Create two instances of fighters
fighter_1 = Fighter(1, 200, 310, False, 'warrior.def')
fighter_2 = Fighter(2, 700, 310, True, 'wizard.def')


all_fighters = CustomSpriteGroup()
all_fighters.add(fighter_1, fighter_2)

# Game loop
last_count_update = pygame.time.get_ticks()
run = True
counter = 0
intro_count = 3
round = 1
countdown_time = 30
start_time = time.time() + 3
round_over = False
time_left = countdown_time
elapsed_time = 0

while run:
    if round > 3:
            run = False
            break
    clock.tick(FPS)
    # Draw background
    draw_bg(screen, bg_image)
    
    # Update the round status and related variables
    round_over, counter, intro_count, round, time_left, elapsed_time, start_time, last_count_update = process_round(
    screen, draw_round_data, round_font, count_font, victory_font, round_over, counter, intro_count, round, time_left, elapsed_time, countdown_time, start_time, fighter_1, fighter_2, score, last_count_update, data_panel_image)

    # Show player stats
    draw_health_bar(screen,1, fighter_1.health, 20, 20)
    draw_health_bar(screen,2, fighter_2.health, 580, 20)
    draw_text(screen, str(score[0]), score_font, RED, 400+5, 80-2)
    draw_text(screen, str(score[1]), score_font, RED, 580-40, 80-2)

    # Update fighters
    
    # Draw fighters
  
    all_fighters.update()
    all_fighters.draw(screen)
    # Event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            all_fighters.reset()

    # Update display
    pygame.display.update()

# Exit pygame
pygame.quit()
