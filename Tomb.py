# File Name: Tomb.py
# Team Members: Nikhil Osuri, Ayush Bobra, Ranvith Adulla, Varun Gabbita
# Date: 06/09/23
# Description: Creates final tomb room with animated chest gif and trophy

# Import necessary libraries
import pygame
import sys

# Initialize global variable
chest_opened = False

# Define tomb funciton
def tomb(screen, current_screen, inventory, start_time, character, is_flip, player_pos, movement_speed, lives):
    # Initialize global variable
    global chest_opened

    # Initialize variables for jumping
    movement_speed = movement_speed * 2
    movement_speed = movement_speed * 2
    jump_y = 10
    jump = False

    # Loop while the user is in the tomb room
    run = True
    while run:
        # Clear the screen
        screen.fill((255, 255, 255))

        # Set up for chest animation
        frame_delay = 200
        chest_x = 475
        chest_y = 350
        chest_frames = []

        # Load the background onto the screen
        background = pygame.image.load('assets/img/tombroom.png').convert()
        background = pygame.transform.scale(background, (screen.get_width(), screen.get_height()))
        screen.blit(background, (0, 0))

        # Display a heart for every life the player has
        if lives > 0:
            heart = pygame.image.load("assets/img/heart.png").convert_alpha()
            screen.blit(heart, (screen.get_width() - heart.get_width() - 20, 20))
        if lives > 1:
            screen.blit(heart, (screen.get_width() - heart.get_width()*2 - 40, 20))
        if lives > 2:
            screen.blit(heart, (screen.get_width() - heart.get_width()*3 - 60, 20))

        # Load the character image
        character_img = pygame.image.load(f"assets/img/{character}{is_flip}.png").convert_alpha()

        # Set the maximum boundaries of the screen
        screen_width = screen.get_width()
        screen_height = screen.get_height()
        min_y = screen.get_rect().centery + 75
        max_x = screen_width - character_img.get_width()
        max_y = screen_height - character_img.get_height()

        #Load the backpack image
        backpack_original = pygame.image.load("assets/img/backpack.png")
        backpack = pygame.transform.scale(backpack_original, (int(backpack_original.get_width()/2), int(backpack_original.get_height()/2)))

        #Get the backpack's dimensions and position
        backpack_width, backpack_height = backpack.get_size()
        backpack_x = screen_width - backpack_width - 10
        backpack_y = screen_height - backpack_height - 10

        # Set the inventory to not show initially
        inventoryRender = False

        #Load the inventory background
        inventory_image = pygame.image.load("assets/img/Inventory.png").convert_alpha()

        # Set up book for the inventory
        inventory_book = pygame.image.load("assets/img/inventory_book.png").convert_alpha() 
        inventory_book = pygame.transform.scale(inventory_book, (int(inventory_book.get_width()/5), int(inventory_book.get_height()/5)))
        inventory_font = pygame.font.Font("assets/font/Pixeloid_Font.ttf", 16)
        book_number = inventory_font.render("1", True, (0, 0, 0))

        # Set up jar for the inventory
        jar_counter = 0
        jar = pygame.image.load("assets/img/jar.png")
        inventory_jar = pygame.transform.scale(jar, (int(jar.get_width()/5), int(jar.get_height()/5)))

        #Set up key for the inventory
        inventory_key = pygame.image.load("assets/img/key.png")
        inventory_key = pygame.transform.scale(inventory_key, (int(inventory_key.get_width()/5), int(inventory_key.get_height()/5)))
        key_number = inventory_font.render("1", True, (0, 0, 0))  

        # Check if any keys have been pressed
        keys = pygame.key.get_pressed()

        # If the player moves left, move the character to the left
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            # Change character image to face left
            is_flip = ""

            # Restrict movement if character goes beyond the left boundary
            if (player_pos[1] >= min_y and player_pos[0] >= 0) or (player_pos[1] < min_y and player_pos[0] >= 70 and player_pos[0] <= 500) or jump:
                player_pos[0] -= movement_speed
            elif (player_pos[0] <= 0):
                current_screen = "puzzle"       # Change the current screen to the puzzle room if the player goes beyond the left boundary
                player_pos[0] = screen_width - character_img.get_width()

        # If the player moves right, move the character to the right
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            # Change character image to face right
            is_flip = "_flip"

            # Restrict movement if character goes beyond the right boundary
            if (player_pos[1] >= min_y and player_pos[0] <= max_x) or (player_pos[1] < min_y and player_pos[0] >= 60 and player_pos[0] <= 480) or jump:
                player_pos[0] += movement_speed
            elif (player_pos[0] >= max_x):
                player_pos = [0, screen.get_rect().centery + 75]
                current_screen = "end"          # Change the current screen to the end screen if the player goes beyond the right boundary

        # If the player moves up, move the character up
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            # Check if the character is within the climbing area
            if player_pos[1] > min_y or (player_pos[1] > 400 and player_pos[0] > 70 and player_pos[0] < 480):
                    player_pos[1] -= movement_speed

        # If the player moves down, move the character down
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            # Restrict movement if character goes beyond the bottom boundary
            if player_pos[1] < max_y:
                player_pos[1] += movement_speed

        # If the player presses the spacebar, make the character jump
        if jump is False and keys[pygame.K_SPACE]:
            jump = True

        # If the character is jumping, move the character along the parabolic path
        if jump is True:
            player_pos[1] -= jump_y * 4.2
            jump_y -= 1
            if jump_y < -10:
                jump = False
                jump_y = 10

        # If the backpack is clicked, show the inventory
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if mouse_x >= 1100 and mouse_x <= 1200 and mouse_y >= 700 and mouse_y <= 800:
                    inventoryRender = True

        # If the inventory is shown, render the inventory
        while inventoryRender:
            # Display the inventory background
            screen.blit(inventory_image, (10, 720))

            # If the user has the book, display the book in the inventory
            if "book" in inventory:
                screen.blit(inventory_book, (12, 723))
                screen.blit(book_number,(60, 742))

            # If the user has the jars, display the jars in the inventory
            if ("jar1" in inventory) and ("jar2" in inventory):
                jar_counter = 2
                jar_number = inventory_font.render(str(jar_counter), True, (0, 0, 0))
                screen.blit(inventory_jar, (70, 723))
                screen.blit(jar_number,(100, 742))
            elif ("jar1" in inventory) or ("jar2" in inventory):
                jar_counter = 1
                jar_number = inventory_font.render(str(jar_counter), True, (0, 0, 0))
                screen.blit(inventory_jar, (70, 723))
                screen.blit(jar_number,(100, 742))

            # If the user has the key, display the key in the inventory
            if "key" in inventory:
                screen.blit(inventory_key, (120, 730))
                screen.blit(key_number,(170, 742))

            # Draw the character and backpack onto the screen
            screen.blit(character_img, (player_pos[0], player_pos[1]))
            screen.blit(backpack, (backpack_x, backpack_y))

            for event in pygame.event.get():
                # If the user quits, close the window
                if event.type == pygame.QUIT:
                    pygame.quit()
                    break

                # If the user clicks on the backpack, close the inventory
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if mouse_x >= 1100 and mouse_x <= 1200 and mouse_y >= 700 and mouse_y <= 800:
                        inventoryRender = False

            # Update the display
            pygame.display.update()

        # Define default chest position
        defaultchest_frame_path = f"assets/img/chestopenframe1.png" 
        defaultchest_frame = pygame.image.load(defaultchest_frame_path).convert_alpha()
        defaultchest_frame = pygame.transform.scale(defaultchest_frame, (int(defaultchest_frame.get_width()*3), int(defaultchest_frame.get_height()*3)))
        screen.blit(defaultchest_frame, (chest_x, chest_y)) 

        # Define chest animation
        if player_pos[0] > 400 and player_pos[0] < 700 and not chest_opened:
            for i in range(1, 5):
                chest_frame_path = f"assets/img/chestopenframe{i}.png"  
                chest_frame = pygame.image.load(chest_frame_path).convert_alpha()
                chest_frame = pygame.transform.scale(chest_frame, (int(chest_frame.get_width()*3), int(chest_frame.get_height()*3)))
                chest_frames.append(chest_frame)

            # Calculate frame index based on time elapsed
            elapsed_time = pygame.time.get_ticks() - start_time
            frame_index = (elapsed_time // frame_delay) % len(chest_frames)

            # Display the current chest frame and trophy onto the screen
            chest_frame = chest_frames[frame_index]
            screen.blit(chest_frame, (chest_x, chest_y))
            trophy_frame_path = "assets/img/trophy.png"  
            trophy_frame = pygame.image.load(trophy_frame_path).convert_alpha()
            trophy_frame = pygame.transform.scale(trophy_frame, (int(trophy_frame.get_width()/2), int(trophy_frame.get_height()/2)))
            screen.blit(trophy_frame,(570, 320)) 

        # Draw the character image and backpack onto the screen
        screen.blit(character_img, (player_pos[0], player_pos[1]))
        screen.blit(backpack, (backpack_x, backpack_y))

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

        # Update the screen
        pygame.display.update()

        # If the user quits, close the window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                sys.exit()

        # Delay frames by 30 milliseconds
        pygame.time.delay(30)

        # Exit the loop if the screen changes
        if current_screen != "tomb":
            break

        # Exit the loop if the time runs out or the user loses all their lives
        if pygame.time.get_ticks() - start_time >= 180000 or lives <= 0:
            current_screen = "end"
            break

    return inventory, is_flip, current_screen, player_pos