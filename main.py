# File Name: Main.py
# Description: Contains main game loop and calls functions from other files

# Import necessary outside libraries
import pygame
import sys

# Import functions from other files
from Start import start
from Character import character_screen
from Dungeon import dungeon
from End import end
from Snake import snake
from Library import library
from Temple import temple
from Embalming import embalming
from Intro import intro
from Puzzle import puzzle
from Tomb import tomb
from Entrance import entrance

# Initialize pygame
pygame.init()

# Define window size
screen_info = pygame.display.Info()
screen_width = 1200
screen_height = 800

# Define screen
screen = pygame.display.set_mode((screen_width, screen_height))

# Initialize variables needed for multiple rooms
is_flip = ""
character = ""
time = ""
start_time = 0
inventory = []
lives = 3
movement_speed = 5
player_pos = [0, screen.get_rect().centery + 90]
current_screen = "start"
game_over = False

# Load and play the music
pygame.mixer.music.load('egypt.wav')
pygame.mixer.music.play(-1)             # -1 means loop indefinitely

# Main game loop
while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:       # If user closes the window, end the game
            pygame.quit()
            sys.exit()

    # Start screen
    if current_screen == "start":
        current_screen = start(current_screen, screen)

    # Character selection screen
    elif current_screen == "character":
        current_screen, character = character_screen(character, current_screen, screen)

    # Game introduciton screen
    elif current_screen == "intro":
        current_screen, player_pos, start_time = intro(current_screen, screen, player_pos, start_time)

    # Ending screen, triggers if time runs out or no lives left
    elif current_screen == "end" or pygame.time.get_ticks() - start_time > 180000 or lives <= 0:
        current_screen, player_pos, is_flip, character, time, start_time, inventory, lives = end(
            current_screen, screen, start_time, lives, inventory, time, character, is_flip, player_pos)

    # Entrance room
    elif current_screen == "entrance":
        inventory, is_flip, time, current_screen, player_pos, lives = entrance(
            current_screen, screen, player_pos, character, is_flip, time, start_time, inventory, movement_speed, lives)

    # Dungeon room
    elif current_screen == "dungeon":
        is_flip, time, current_screen, inventory, player_pos, lives = dungeon(
            current_screen, screen, character, inventory, is_flip, player_pos, movement_speed, start_time, lives, time)

    # Library room
    elif current_screen == "library":
        inventory, is_flip, time, current_screen, player_pos = library(
            inventory, screen, character, is_flip, player_pos, movement_speed, start_time, current_screen, lives)

    # Temple room
    elif current_screen == "temple":
        inventory, is_flip, time, current_screen, player_pos = temple(
            screen, current_screen, inventory, start_time, character, is_flip, player_pos, movement_speed, lives)

    # Snake room
    elif current_screen == "snake":
        inventory, is_flip, time, current_screen, player_pos, lives = snake(
            current_screen, screen, inventory, character, is_flip, player_pos, movement_speed, start_time, lives)

    # Embalming room
    elif current_screen == "embalming":
        inventory, is_flip, current_screen, player_pos, lives = embalming(
            screen, current_screen, inventory, start_time, character, is_flip, player_pos, movement_speed, lives)

    # Puzzle room
    elif current_screen == "puzzle":
        inventory, is_flip, current_screen, player_pos = puzzle(
            screen, current_screen, inventory, start_time, character, is_flip, player_pos, movement_speed, lives)

    # Tomb room
    elif current_screen == "tomb":
        inventory, is_flip, current_screen, player_pos = tomb(
            screen, current_screen, inventory, start_time, character, is_flip, player_pos, movement_speed, lives)