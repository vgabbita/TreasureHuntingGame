# File Name: Intro.py
# Team Members: Nikhil Osuri, Ayush Bobra, Ranvith Adulla, Varun Gabbita
# Date: 06/09/23
# Description: Creates introduction screen for the game

# Import necessary library
import pygame

# Define intro function
def intro(current_screen, screen, player_pos, start_time):
    # Clear the screen
    screen.fill((255,255,255))

    # Load background image and place it on screen
    background = pygame.image.load("assets/img/intro.png").convert_alpha()
    screen.blit(background, (0, 0))

    # Draw the title and footer of the scroll
    title_font = pygame.font.Font("assets/font/Pixeloid_Font.ttf", 42)
    title = title_font.render("Welcome to Pharaoh's Fortune!", True, (0,0,0))
    footer = title_font.render("Press X to continue.", True, (0,0,0))
    screen.blit(title, (screen.get_width()//2 - title.get_width()//2, 75))
    screen.blit(footer, (screen.get_width()//2 - footer.get_width()//2, screen.get_height() - 125))

    # Add the instructions to the scroll
    font = pygame.font.Font("assets/font/Pixeloid_Font.ttf", 22)
    instructions = open("assets/text/instructions.txt", "r")        # Gets the instructions from the text file

    # Renders each line of the instructions and places it on the screen
    for index, line in enumerate(instructions):
        line = font.render(line.strip(), True, (0,0,0))
        screen.blit(line, (screen.get_width()//2 - line.get_width()//2, 210 + index*29))

    # Checks if the user has pressed a key
    keys = pygame.key.get_pressed()

    # If the user presses X, the game starts
    if keys[pygame.K_x]:
        current_screen = "entrance"
        player_pos = [0, screen.get_height()//2 + 75]
        start_time = pygame.time.get_ticks()

    # Update the screen
    pygame.display.update()

    return current_screen, player_pos, start_time