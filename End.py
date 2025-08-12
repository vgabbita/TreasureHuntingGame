# File Name: End.py
# Team Members: Nikhil Osuri, Ayush Bobra, Ranvith Adulla, Varun Gabbita
# Date: 06/09/23
# Description: Creates screen for ending "winning" or "losing" message

# Import necessary libraries
import pygame
import sys

# Define end function
def end(current_screen, screen, start_time, lives, inventory, time, character, is_flip, player_pos):
    # Show background on screen
    background = pygame.image.load("assets/img/pyramids.png")
    screen.blit(background, (0, 0))

    # Define title font
    title_font = pygame.font.Font("assets/font/Pixeloid_Font.ttf", 96)

    # If the user won, show "You win!" message
    if pygame.time.get_ticks() - start_time < 180000 and lives > 0:
        title_text = title_font.render("You win! :)", True, (255, 255, 255))
        image = pygame.image.load("assets/img/trophy.png").convert_alpha()

    # If the user lost, show "You died!" message
    else:
        dark = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        dark.fill((0, 0, 0, 100))
        screen.blit(dark, (0, 0))
        
        title_text = title_font.render("You died! :(", True, (0, 0, 0))
        image = pygame.image.load("assets/img/skull.png").convert_alpha()
        image = pygame.transform.scale(image, (image.get_width() * (200/30), image.get_height() * (200/30)))

    # Display the title text and image on screen
    screen.blit(title_text, (screen.get_rect().centerx - title_text.get_width()//2, 20))
    screen.blit(image, (screen.get_rect().centerx - image.get_width()//2, 175))

    # Define button font
    button_font = pygame.font.Font("assets/font/Pixeloid_Font.ttf", 42)

    # Quit button to close the window
    quit_text = button_font.render("Quit", True, (0, 0, 0))
    quit_rect = quit_text.get_rect()
    quit_rect.centerx = screen.get_rect().centerx / 2
    quit_rect.top = 400

    # Play again function to restart the game
    play_again_text = button_font.render("Play Again!", True, (0, 0, 0))
    play_again_rect = play_again_text.get_rect()
    play_again_rect.centerx = screen.get_rect().centerx * 3 / 2
    play_again_rect.top = 400

    # Display buttons on screen
    screen.blit(quit_text, quit_rect)
    screen.blit(play_again_text, play_again_rect)

    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            if quit_rect.collidepoint(event.pos):       # If user quits, close the window
                sys.exit()
            if play_again_rect.collidepoint(event.pos): # If user plays again, reset all variables and restart the game
                current_screen = "character"
                player_pos = [screen.get_rect().centerx, screen.get_rect().centery + 90]
                is_flip = ""
                character = ""
                time = ""
                start_time = 0
                inventory = []
                lives = 3

    # Update the screen
    pygame.display.update()

    return current_screen, player_pos, is_flip, character, time, start_time, inventory, lives