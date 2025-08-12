# File Name: Start.py
# Team Members: Nikhil Osuri, Ayush Bobra, Ranvith Adulla, Varun Gabbita
# Date: 06/09/23
# Description: Creates start screen for the game

# Import necessary library
import pygame

# Define start function
def start(current_screen, screen):
    # Load background image and place it on screen
    background = pygame.image.load("assets/img/pyramids.png")
    screen.blit(background, (0, 0))

    # Define title text
    title_font = pygame.font.Font("assets/font/Pixeloid_Font.ttf", 96)
    title_text = title_font.render("Pharaoh's Fortune", True, (0, 0, 0))

    # Define subtitle text
    subtitle_font = pygame.font.Font("assets/font/Pixeloid_Font.ttf", 48)
    subtitle_text = subtitle_font.render("The Quest for Ancient Treasure", True, (0, 0, 0))

    # Define button text
    button_font = pygame.font.Font("assets/font/Pixeloid_Font.ttf", 24)
    button_text = button_font.render("Start Game", True, (0, 0, 0))

    # Get dimensions of title text
    title_text_rect = title_text.get_rect()

    # Center title text horizontally and position 100 units from top of screen
    title_text_rect.centerx = screen.get_rect().centerx
    title_text_rect.top = 100

    # Get dimensions of subtitle text
    subtitle_text_rect = subtitle_text.get_rect()

    # Center subtitle text horizontally and position below title text
    subtitle_text_rect.centerx = screen.get_rect().centerx
    subtitle_text_rect.top = title_text_rect.bottom + 10

    # Get dimensions of button text
    button_text_rect = button_text.get_rect()

    # Center button text horizontally and vertically
    button_text_rect.centerx = screen.get_rect().centerx
    button_text_rect.top = screen.get_rect().centery

    # Define button rect
    start_button_rect = pygame.Rect(button_text_rect.left - 10, button_text_rect.top - 10, button_text_rect.width + 20, button_text_rect.height + 20)

    # Show title text on screen
    screen.blit(title_text, title_text_rect)
    
    # Show subtitle text on screen
    screen.blit(subtitle_text, subtitle_text_rect)
    
    # Add button to screen
    pygame.draw.rect(screen, (255, 255, 255), start_button_rect)
    screen.blit(button_text, button_text_rect)

    # Update screen
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            if start_button_rect.collidepoint(event.pos):   # If the button is clicked, continue to next screen
                current_screen = "character"

    return current_screen