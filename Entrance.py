# File Name: Entrance.py
# Team Members: Nikhil Osuri, Ayush Bobra, Ranvith Adulla, Varun Gabbita
# Date: 06/09/23
# Description: Creates environment for entrance room, with grabbing a torch

# Import necessary libraries
import pygame
import sys
import random

# Initialize inventory to not show up
inventoryRender = False

# Define entrance function
def entrance(current_screen, screen, player_pos, character, is_flip, time, start_time, inventory, movement_speed, lives):
    # Define variables for jumping
    vel_x = movement_speed * 2
    vel_y = movement_speed * 2
    jump_y = 10
    jump = False

    # Initialize variables for the rocks
    enemy_list = []
    enemy_speed = 7

    # Initialize inventory to not show up
    global inventoryRender

    # Loops while the player is in the entrance room
    run = True
    while run:
        # Clear the screen
        screen.fill((255, 255, 255))

        # Draw the background
        background = pygame.image.load('assets/img/mainroom.png').convert_alpha()
        screen.blit(background, (0, 0))

        # Get the character image
        character_img = pygame.image.load(f'assets/img/{character}{is_flip}.png').convert_alpha()

        # Set the maximum boundaries of the screen
        screen_width = screen.get_width()
        screen_height = screen.get_height()
        min_y = screen.get_rect().centery + 75
        max_x = screen_width - character_img.get_width()
        max_y = screen_height - character_img.get_height()

        # Load the backpack image
        backpack_original = pygame.image.load("assets/img/backpack.png")
        backpack = pygame.transform.scale(backpack_original, (int(backpack_original.get_width()/2), int(backpack_original.get_height()/2)))

        # Get the backpack's dimensions and position
        backpack_width, backpack_height = backpack.get_size()
        backpack_x = screen_width - backpack_width - 10
        backpack_y = screen_height - backpack_height - 10

        # Load the inventory image
        inventory_image = pygame.image.load("assets/img/Inventory.png").convert_alpha()

        # Load inventory book image
        inventory_book = pygame.image.load("assets/img/inventory_book.png").convert_alpha() 
        inventory_book = pygame.transform.scale(inventory_book, (int(inventory_book.get_width()/5), int(inventory_book.get_height()/5)))

        # Load inventory book number
        inventory_font = pygame.font.Font("assets/font/Pixeloid_Font.ttf", 16)
        book_number = inventory_font.render("1", True, (0, 0, 0))

        # Set up jar image for the inventory
        jar_counter = 0
        jar = pygame.image.load("assets/img/jar.png")
        inventory_jar = pygame.transform.scale(jar, (int(jar.get_width()/5), int(jar.get_height()/5)))

        # Set up key image for the inventory
        inventory_key = pygame.image.load("assets/img/key.png")
        inventory_key = pygame.transform.scale(inventory_key, (int(inventory_key.get_width()/5), int(inventory_key.get_height()/5)))
        key_number = inventory_font.render("1", True, (0, 0, 0))

        # Set up torch image for the inventory
        inventory_torch = pygame.image.load("assets/img/torch.png")
        inventory_torch = pygame.transform.scale(inventory_torch, (int(inventory_torch.get_width()/6.1), int(inventory_torch.get_height()/6.1)))
        torch_number = inventory_font.render("1", True, (0, 0, 0))

        # If the player does not have the torch, draw the torch
        if "torch" not in inventory:
            torch = pygame.image.load("assets/img/torch.png").convert_alpha()
            torch = pygame.transform.scale(torch, (int(torch.get_width()/2), int(torch.get_height()/2)))
            screen.blit(torch, (45, 260))

        # Draw one heart for each life the player has
        if lives > 0:
            heart = pygame.image.load("assets/img/heart.png").convert_alpha()
            screen.blit(heart, (screen.get_width() - heart.get_width() - 20, 20))
        if lives > 1:
            screen.blit(heart, (screen.get_width() - heart.get_width()*2 - 40, 20))
        if lives > 2:
            screen.blit(heart, (screen.get_width() - heart.get_width()*3 - 60, 20))

        # Checks if player has pressed any keys
        keys = pygame.key.get_pressed()
        font = pygame.font.Font("assets/font/Pixeloid_Font.ttf", 36)

        # If user moves left, move the character left
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            is_flip = ""
            if player_pos[0] >= 0:
                player_pos[0] -= vel_x

        # If user moves right, move the character right
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            is_flip = "_flip"
            if player_pos[0] < max_x:
                player_pos[0] += vel_x
            else:
                player_pos = [0, screen.get_rect().centery + 75]
                current_screen = "dungeon"                          # Once user reaches the end of the screen, move to the next screen

        # If user moves up, move the character up
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            if player_pos[1] > min_y:
                player_pos[1] -= vel_y

        # If user moves down, move the character down
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            if player_pos[1] < max_y:
                player_pos[1] += vel_y

        # If the user presses X, check if they are in the right position to pick up the torch
        if keys[pygame.K_x]:
            if player_pos[1] <= 437 and player_pos[0] <= 100:
                if "torch" not in inventory:
                    # Checks if user has space in their inventory
                    if len(inventory) > 4:
                        too_many = font.render("You can only carry 4 items!", True, (255, 255, 255))
                        screen.blit(too_many, (20, 750))
                    # If user has space, add the torch to their inventory
                    else:
                        inventory.append("torch")

        # If the user presses space, check if they are already jumping
        if jump is False and keys[pygame.K_SPACE]:
            jump = True

        # If the user is jumping, move the character in a parabolic motion
        if jump is True:
            player_pos[1] -= jump_y * 4.2
            jump_y -= 1
            if jump_y < -10:
                jump = False
                jump_y = 10

        # Draw the character on the screen
        screen.blit(character_img, (player_pos[0], player_pos[1]))

        # Checks if the user has clicked the backpack
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if mouse_x >= 1100 and mouse_x <= 1200 and mouse_y >= 700 and mouse_y <= 800:
                    inventoryRender = True

        # If the user has clicked the backpack, draw the inventory
        while inventoryRender:
            # Adds the inventory background
            screen.blit(inventory_image, (10, 720))

            # Displays the torch, if the user has it
            if "torch" in inventory:
                screen.blit(inventory_torch, (30, 720))
                screen.blit(torch_number,(50, 742))

            # Displays the book, if the user has it
            if "book" in inventory:
                screen.blit(inventory_book, (70, 723))
                screen.blit(book_number,(100, 742))

            # Displays the jars, if the user has them
            if ("jar1" in inventory) and ("jar2" in inventory):
                jar_counter = 2
                jar_number = inventory_font.render(str(jar_counter), True, (0, 0, 0))
                screen.blit(inventory_jar, (120, 723))
                screen.blit(jar_number,(170, 742))
            elif ("jar1" in inventory) or ("jar2" in inventory):
                jar_counter = 1
                jar_number = inventory_font.render(str(jar_counter), True, (0, 0, 0))
                screen.blit(inventory_jar, (120, 723))
                screen.blit(jar_number,(170, 742))

            # Displays the key, if the user has it
            if "key" in inventory:
                screen.blit(inventory_key, (170, 730))
                screen.blit(key_number,(170, 742))

            # Draw the character and backpack on the screen
            screen.blit(character_img, (player_pos[0], player_pos[1]))
            screen.blit(backpack, (backpack_x, backpack_y))


            for event in pygame.event.get():
                # Check if user has exited the game, and if they have, quits
                if event.type == pygame.QUIT:
                    pygame.quit()
                    break

                # Checks if the user has clicked the backpack, and if they have, closes the inventory
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if mouse_x >= 1100 and mouse_x <= 1200 and mouse_y >= 700 and mouse_y <= 800:
                        inventoryRender = False

            # Updates the screen
            pygame.display.update()

        # Sets up the font for the text
        font = pygame.font.Font("assets/font/Pixeloid_Font.ttf", 36)

        # If the user is in the right position, display the text to pick up the torch
        if player_pos[1] <= 437 and (player_pos[0] >= 0 and player_pos[0] <= 100):
            get_torch = font.render("Press X to pick up torch", True, (255, 255, 255))
            screen.blit(get_torch, (20, 750))

        # Sets up rock image
        rock = pygame.image.load("assets/img/rock.png").convert_alpha()

        # Sets up random rock spawning
        delay = random.random()
        if len(enemy_list) < 8 and delay < 0.075:
            enemy_list.append([random.randint(700, 1100), 0])

        for idx, enemy_pos in enumerate(enemy_list):
            # Moves the rock down if it is on the screen
            if enemy_pos[1] >= 0 and enemy_pos[1] <= screen.get_height():
                enemy_pos[1] += enemy_speed
            
            # If the rock is off the screen, remove it from the list
            else:
                enemy_list.pop(idx)

        # Checks if the user has been hit by a rock
        detected = False
        for enemy_pos in enemy_list:
            if (enemy_pos[0] >= player_pos[0] and enemy_pos[0] < (player_pos[0] + character_img.get_width())) or (player_pos[0] >= enemy_pos[0] and player_pos[0] < (enemy_pos[0] + rock.get_width())):
                if (enemy_pos[1] >= player_pos[1] and enemy_pos[1] < (player_pos[1] + character_img.get_height())) or (player_pos[1] >= enemy_pos[1] and player_pos[1] < (enemy_pos[1] + rock.get_height())):
                    detected = True
                    break               # Breaks out of the loop if the user has been hit
        
        # If the user has been hit, remove a life and reset the user's position
        if detected:
            lives -= 1
            player_pos = [0, screen.get_rect().centery + 75]

        # Draw all the rocks on the screen
        for enemy_pos in enemy_list:
            screen.blit(rock, (enemy_pos[0], enemy_pos[1]))

        # Sets up timer font
        timer_font = pygame.font.Font("assets/font/Pixeloid_Font.ttf", 36)

        # Calculates the time remaining
        elapsed_time = pygame.time.get_ticks() - start_time
        duration = 180
        remaining_time = max(duration - int(elapsed_time / 1000), 0)
        minutes = int(remaining_time / 60)
        seconds = remaining_time % 60

        # Displays the time remaining
        time = '{:02d}:{:02d}'.format(minutes, seconds)
        timer_text = timer_font.render(time, True, (255, 255, 255))
        screen.blit(timer_text, (20, 20))

        # Draw the backpack button
        screen.blit(backpack, (backpack_x, backpack_y))

        # Update the screen
        pygame.display.update()

        # Checks if the user has exited the game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                sys.exit()

        # Delay each frame by 30 milliseconds
        pygame.time.delay(30)

        # Exits loop if user is on a different screen
        if current_screen != "entrance":
            break

        # Exits loop if the user has run out of lives or time
        if pygame.time.get_ticks() - start_time >= 180000 or lives <= 0:
            current_screen = "end"
            break

    return inventory, is_flip, time, current_screen, player_pos, lives