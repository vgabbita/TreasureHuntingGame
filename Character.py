# File Name: Character.py
# Team Members: Nikhil Osuri, Ayush Bobra, Ranvith Adulla, Varun Gabbita
# Date: 06/09/23
# Description: Creates screen that allows user to choose character

# Import necessary library
import pygame

# Define character screen function
def character_screen(character, current_screen, screen):
    # Clear the screen
    screen.fill((255,255,255))

    # Load background image and place it on screen
    background = pygame.image.load("assets/img/dunes.png").convert()
    screen.blit(background, (0, 0))

    # Draw the "Choose a Character" subheading
    subheading_font = pygame.font.Font("assets/font/Pixeloid_Font.ttf", 48)
    subheading_text = subheading_font.render("Choose a Character", True, (0,0,0))
    subheading_rect = subheading_text.get_rect()
    subheading_rect.centerx = screen.get_rect().centerx
    subheading_rect.top = 150
    screen.blit(subheading_text, subheading_rect)

    # Load the male and female character images
    male_img = pygame.image.load("assets/img/male.png").convert_alpha()
    female_img = pygame.image.load("assets/img/female.png").convert_alpha()

    # Font for character buttons
    button_font = pygame.font.Font("assets/font/Pixeloid_Font.ttf", 30)

    # Set up male character button
    male_button_text = button_font.render("Hunter", True, (0, 0, 0))
    male_button_rect = male_button_text.get_rect()
    male_button_rect.centerx = screen.get_rect().centerx / 2
    male_button_rect.top = subheading_rect.bottom + 200

    # Set up female character button
    female_button_text = button_font.render("Violet", True, (0, 0, 0))
    female_button_rect = female_button_text.get_rect()
    female_button_rect.centerx = screen.get_rect().centerx * 3 / 2
    female_button_rect.top = subheading_rect.bottom + 200

    # Draw the male and female character images and buttons
    screen.blit(male_img, (male_button_rect.centerx - male_img.get_width() / 2, male_button_rect.bottom + 25))
    screen.blit(male_button_text, male_button_rect)
    screen.blit(female_img, (female_button_rect.centerx - female_img.get_width() / 2, female_button_rect.bottom + 25))
    screen.blit(female_button_text, female_button_rect)

    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            if male_button_rect.collidepoint(event.pos):        # If male button is clicked, use male character
                character = "male"
                current_screen = "intro"
            if female_button_rect.collidepoint(event.pos):      # If female button is clicked, use female character
                character = "female"
                current_screen = "intro"

    # Update the screen
    pygame.display.update()

    return current_screen, character