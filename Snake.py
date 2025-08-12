# File Name: Snake.py
# Team Members: Nikhil Osuri, Ayush Bobra, Ranvith Adulla, Varun Gabbita
# Date: 06/09/23
# Description: Creates snake platforming room that forces user to jump over moving snake holes

# Import necessary libraries
import pygame
import sys

# Initializes inventory to not show
inventoryRender = False

# Defines snake function
def snake(current_screen, screen, inventory, character, is_flip, player_pos, movement_speed, start_time, lives):
    # Initialize variables for jumping
    vel_x = movement_speed*2
    vel_y = movement_speed*2
    jump_y = 10
    jump = False

    # Initializes inventory
    global inventoryRender

    # Load background animation frames
    background_frames = [
        pygame.image.load("assets/img/frame0.png").convert(),
        pygame.image.load("assets/img/frame1.png").convert(),
        pygame.image.load("assets/img/frame2.png").convert(),
        pygame.image.load("assets/img/frame3.png").convert()
    ]
    current_frame = 0
    frame_duration = 100  # Duration of each frame in milliseconds
    last_frame_time = pygame.time.get_ticks()

    # Loop while user is in snake room
    run = True
    while run:
        # Clear the screen
        screen.fill((255, 255, 255))

        # Update background animation frame
        if pygame.time.get_ticks() - last_frame_time >= frame_duration:
            current_frame = (current_frame + 1) % len(background_frames)
            last_frame_time = pygame.time.get_ticks()

        # Display the current background frame
        background = background_frames[current_frame]
        screen.blit(background, (0, 0))

        # Draw a heart for each life the user has
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


        # Load the inventory background
        inventory_image = pygame.image.load("assets/img/Inventory.png").convert_alpha()

        # Sets up book image for the inventory
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

        # Checks if any keys were pressed
        keys = pygame.key.get_pressed()

        # Moves the character left if the user moves left
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            # Change character image to face left
            is_flip = ""

            # Restrict movement if character goes beyond the left boundary
            if player_pos[0] > 0:
                player_pos[0] -= vel_x
            else:
                current_screen = "temple"       # Change screen to temple if character goes beyond left boundary
                player_pos[0] = screen_width - character_img.get_width()

        # Moves the character right if the user moves right
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            # Change character image to face right
            is_flip = "_flip"

            # Restrict movement if character goes beyond the right boundary
            if player_pos[0] < max_x:
                player_pos[0] += vel_x
            
            # User needs both jars to enter embalming room
            elif player_pos[0] >= max_x and ('jar1' not in inventory or 'jar2' not in inventory):
                font = pygame.font.Font("assets/font/Pixeloid_Font.ttf", 30)
                pick_up = font.render("Need two jars to enter embalming room.", True, (255, 255, 255))
                screen.blit(pick_up, (20, 750))
            else:
                player_pos = [0, screen.get_rect().centery + 75]
                current_screen = "embalming"        # Change screen to embalming room if character goes beyond right boundary

        # Moves the character up if the user moves up
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            # Restrict movement if character goes beyond the top boundary
            if player_pos[1] > min_y:
                player_pos[1] -= vel_y

        # Moves the character down if the user moves down
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            # Restrict movement if character goes beyond the bottom boundary
            if player_pos[1] < max_y:
                player_pos[1] += vel_y

        # Checks if the user has pressed the space bar to jump
        if jump is False and keys[pygame.K_SPACE]:
            jump = True

        # If the user is jumping, move the character along the parabolic path
        if jump is True:
            player_pos[1] -= jump_y*4.2
            jump_y -= 1
            if jump_y < -10:
                jump = False
                jump_y = 10

        # Checks if the user has pressed the backpack to open the inventory
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if mouse_x >= 1100 and mouse_x <= 1200 and mouse_y >= 700 and mouse_y <= 800:
                    inventoryRender = True

        # If the inventory is open, display the inventory
        while inventoryRender:
            # Display the inventory background
            screen.blit(inventory_image, (10, 720))

            # Display the torch, if the user has it
            if "torch" in inventory:
                screen.blit(inventory_torch, (30, 720))
                screen.blit(torch_number,(50, 742))

            # Display the book, if the user has it
            if "book" in inventory:
                screen.blit(inventory_book, (70, 723))
                screen.blit(book_number,(110, 742))

            # Display the jars, if the user has them
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

            # Display the key, if the user has it
            if "key" in inventory:
                screen.blit(inventory_key, (170, 730))
                screen.blit(key_number,(220, 742))

            # Show the character and backpack on the screen
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

        # If a snake bites the user, the user loses a life and resets to the starting position
        if (player_pos[0] >= 190 and player_pos[0] <= 290 and player_pos[1] >= 400) or (player_pos[0] >= 570 and player_pos[0] <= 660 and player_pos[1] >= 400) or (player_pos[0] >= 880 and player_pos[0] <= 950 and player_pos[1] >= 400):
            player_pos = [0, screen.get_rect().centery + 75]
            lives -= 1

        # Draw the character image
        screen.blit(character_img, (player_pos[0], player_pos[1]))

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

        # Load the backpack image
        backpack_original = pygame.image.load("assets/img/backpack.png")
        backpack = pygame.transform.scale(backpack_original, (int(backpack_original.get_width()/2), int(backpack_original.get_height()/2)))

        # Get the backpack's dimensions and position
        backpack_width, backpack_height = backpack.get_size()
        backpack_x = screen_width - backpack_width - 10
        backpack_y = screen_height - backpack_height - 10

        # Draw the backpack button
        screen.blit(backpack, (backpack_x, backpack_y))

        # Updates the screen
        pygame.display.update()

        # If the user quits, close the window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                sys.exit()

        # Delay each frame by 30 milliseconds
        pygame.time.delay(30)

        # Break out of the loop if the current screen changes
        if current_screen != "snake":
            break

        # Break out of the loop if the user runs out of time or lives
        if pygame.time.get_ticks() - start_time >= 180000 or lives <= 0:
            current_screen = "end"
            break

    return inventory, is_flip, time, current_screen, player_pos, lives