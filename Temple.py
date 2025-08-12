# File Name: Temple.py
# Team Members: Nikhil Osuri, Ayush Bobra, Ranvith Adulla, Varun Gabbita
# Date: 06/09/23
# Description: Creates library room for the game

# Import necessary libraries
import pygame
import sys

# Initializes inventory to not show
inventoryRender = False

# Defines temple function
def temple(screen, current_screen, inventory, start_time, character, is_flip, player_pos, movement_speed, lives):
    # Define variables for jumping
    vel_x = movement_speed * 2.5
    vel_y = movement_speed * 2.5
    jump_y = 10
    jump = False

    # Initialize inventory
    global inventoryRender

    # Loops while user is in temple room
    run = True
    while run:
        # Clears screen
        screen.fill((255, 255, 255))

        # Draws the background
        background = pygame.image.load('assets/img/temple.jpg').convert()
        screen.blit(background, (0, 0))

        # Draws a heart for each life
        if lives > 0:
            heart = pygame.image.load("assets/img/heart.png").convert_alpha()
            screen.blit(heart, (screen.get_width() - heart.get_width() - 20, 20))
        if lives > 1:
            screen.blit(heart, (screen.get_width() - heart.get_width()*2 - 40, 20))
        if lives > 2:
            screen.blit(heart, (screen.get_width() - heart.get_width()*3 - 60, 20))

        # Loads the character image
        character_img = pygame.image.load(f"assets/img/{character}{is_flip}.png").convert_alpha()

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

        # Load the inventory background
        inventory_image = pygame.image.load("assets/img/Inventory.png").convert_alpha()

        # Set up book image for the inventory
        inventory_book = pygame.image.load("assets/img/inventory_book.png").convert_alpha() 
        inventory_book = pygame.transform.scale(inventory_book, (int(inventory_book.get_width()/5), int(inventory_book.get_height()/5)))
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

        # If the player does not have the jars, draw them
        if "jar1" not in inventory:
            jar = pygame.image.load("assets/img/jar.png")
            jar1 = pygame.transform.scale(jar, (int(jar.get_width()/1.7), int(jar.get_height()/1.7)))
            screen.blit(jar1, (230, 480))
        if "jar2" not in inventory:
            jar = pygame.image.load("assets/img/jar.png")
            jar2 = pygame.transform.scale(jar, (int(jar.get_width()/1.7), int(jar.get_height()/1.7)))
            screen.blit(jar2, (830, 480))

        # Checks if user has pressed any keys
        keys = pygame.key.get_pressed()

        # If the user moves left, move the character left
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            # Change character image to face left
            is_flip = ""

            # Restrict movement if character goes beyond the left boundary
            if player_pos[1] >= 475:
                if player_pos[0] > 0:
                    player_pos[0] -= vel_x
                else:
                    player_pos = [screen_width - character_img.get_width(), screen.get_rect().centery + 75]
                    current_screen = "library"      # Change screen to library if user goes beyond left boundary

            # Allows user to move on stairs
            else:
                if player_pos[0] >= 400 and player_pos[0] <= 610:
                    player_pos[0] -= vel_x

        # If the user moves right, move the character right
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            # Change character image to face right
            is_flip = "_flip"

            # Restrict movement if character goes beyond the right boundary
            if player_pos[1] >= 475:
                if player_pos[0] < max_x:
                    player_pos[0] += vel_x
                else:
                    player_pos = [0, screen.get_rect().centery + 75]
                    current_screen = "snake"        # Change screen to snake if user goes beyond right boundary

            # Allows user to move on stairs
            else:
                if player_pos[0] >= 400 and player_pos[0] <= 610:
                    player_pos[0] += vel_x

        # If the user moves up, move the character up
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            # Check if the character is within the climbing area
            if player_pos[0] >= 400 and player_pos[0] <= 610 and player_pos[1] > min_y-150:
                player_pos[1] -= vel_y
            elif player_pos[1] > min_y:
                player_pos[1] -= vel_y

        # If the user moves down, move the character down
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            # Restrict movement if character goes beyond the bottom boundary
            if player_pos[1] < max_y:
                player_pos[1] += vel_y

        # If the user presses x, check if they are in the right position to interact with an object
        if keys[pygame.K_x]:
            font = pygame.font.Font("assets/font/Pixeloid_Font.ttf", 36)
            if player_pos[0] >= 480 and player_pos[0] <= 520 and player_pos[1] >= 320 and player_pos[1] <= 360:
                # Checks if the user can add the key to their inventory
                if "key" not in inventory:
                    if len(inventory) > 4:
                        too_many = font.render("You can only carry 4 items!", True, (255, 255, 255))
                        screen.blit(too_many, (20, 750))
                    else:
                        inventory.append("key")

            # Checks if the user can add the first jar to their inventory
            elif (player_pos[0] >= 210 and player_pos[0] <= 250 and player_pos[1] >= 420 and player_pos[1] <= 500):
                if "jar1" not in inventory:
                    if len(inventory) > 4:
                        too_many = font.render("You can only carry 4 items!", True, (255, 255, 255))
                        screen.blit(too_many, (20, 750))
                    else:
                        inventory.append("jar1")

            # Checks if the user can add the second jar to their inventory
            elif (player_pos[0] >= 810 and player_pos[0] <= 850 and player_pos[1] >= 420 and player_pos[1] <= 500):
                if "jar2" not in inventory:
                    if len(inventory) > 4:
                        too_many = font.render("You can only carry 4 items!", True, (255, 255, 255))
                        screen.blit(too_many, (20, 750))
                    else:
                        inventory.append("jar2")

        # User begins to jump
        if jump is False and keys[pygame.K_SPACE]:
            jump = True

        # If the user is jumping, move the character in the parabolic path
        if jump is True:
            player_pos[1] -= jump_y * 4.2
            jump_y -= 1
            if jump_y < -10:
                jump = False
                jump_y = 10

        # Show the inventory if the backpack is clicked
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if mouse_x >= 1100 and mouse_x <= 1200 and mouse_y >= 700 and mouse_y <= 800:
                    inventoryRender = True

        # If the inventory is open, show the inventory
        while inventoryRender:
            # Displays inventory background
            screen.blit(inventory_image, (10, 720))

            # Displays torch, if user has it
            if "torch" in inventory:
                screen.blit(inventory_torch, (30, 720))
                screen.blit(torch_number,(50, 742))

            # Displays book, if user has it
            if "book" in inventory:
                screen.blit(inventory_book, (70, 723))
                screen.blit(book_number,(110, 742))

            # Displays jars, if user has them
            if ("jar1" in inventory) and ("jar2" in inventory):
                jar_counter = 2
                jar_number = inventory_font.render(str(jar_counter), True, (0, 0, 0))
                screen.blit(inventory_jar, (120, 723))
                screen.blit(jar_number,(150, 742))
            elif ("jar1" in inventory) or ("jar2" in inventory):
                jar_counter = 1
                jar_number = inventory_font.render(str(jar_counter), True, (0, 0, 0))
                screen.blit(inventory_jar, (120, 723))
                screen.blit(jar_number,(150, 742))

            # Displays key, if user has it
            if "key" in inventory:
                screen.blit(inventory_key, (170, 730))
                screen.blit(key_number,(220, 742))

            # Displays character and backpack images
            screen.blit(character_img, (player_pos[0], player_pos[1]))
            screen.blit(backpack, (backpack_x, backpack_y))

            for event in pygame.event.get():
                # If the user quits, close the window
                if event.type == pygame.QUIT:
                    pygame.quit()
                    break

                # If the user clicks the backpack, close the inventory
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if mouse_x >= 1100 and mouse_x <= 1200 and mouse_y >= 700 and mouse_y <= 800:
                        inventoryRender = False

            # Update the screen
            pygame.display.update()

        # Draw the character image
        screen.blit(character_img, (player_pos[0], player_pos[1]))

        # Add text to pick up key
        font = pygame.font.Font("assets/font/Pixeloid_Font.ttf", 36)
        if "key" not in inventory:
            if player_pos[0] >= 480 and player_pos[0] <= 520 and player_pos[1] >= 320 and player_pos[1] <= 360:
                pick_up = font.render("You found a key! Press X to pick it up", True, (255, 255, 255))
                screen.blit(pick_up, (20, 750))
                
                # Draw the image of the key on screen
                key = pygame.image.load("assets/img/key.png")
                key = pygame.transform.scale(key, (int(key.get_width()/2), int(key.get_height()/2)))
                screen.blit(key, (510, 250))

        # Add text to pick up jar
        if ("jar1" not in inventory) or ("jar2" not in inventory):
            if (player_pos[0] >= 210 and player_pos[0] <= 250 and player_pos[1] >= 420 and player_pos[1] <= 500) or (player_pos[0] >= 810 and player_pos[0] <= 850 and player_pos[1] >= 420 and player_pos[1] <= 500):
                pick_up = font.render("Press X to pick up the jar", True, (255, 255, 255))
                screen.blit(pick_up, (20, 750))

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

        # If the user quits, close the window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                sys.exit()

        # Delay each frame by 30 milliseconds
        pygame.time.delay(30)

        # If the screen changes, exit the loop
        if current_screen != "temple":
            break

        # If the user ran out of times or lives, exit the loop
        if pygame.time.get_ticks() - start_time >= 180000 or lives <= 0:
            current_screen = "end"
            break

    return inventory, is_flip, time, current_screen, player_pos