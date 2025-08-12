# File Name: Embalming.py
# Team Members: Nikhil Osuri, Ayush Bobra, Ranvith Adulla, Varun Gabbita
# Date: 06/09/23
# Description: Creates environment for embalming room with laid down sarcophogus

# Import necessary libraries
import pygame 
import sys

# Initialize necessary variables
dropped = False
inventoryRender = False

def embalming(screen, current_screen, inventory, start_time, character, is_flip, player_pos, movement_speed, lives):
    # Initialize necessary variables
    global dropped, inventoryRender

    # Set up jar image for the inventory
    jar_counter = 0
    jar = pygame.image.load("assets/img/jar.png")
    inventory_jar = pygame.transform.scale(jar, (int(jar.get_width()/5), int(jar.get_height()/5)))

    # Initialize variables needed for jumping
    vel_x = movement_speed * 3
    vel_y = movement_speed * 3
    jump_y = 10
    jump = False

    # Initialize variables needed for mummy
    mummy_pos = [570, 475]
    mummy_speed = movement_speed
    mummy_flip = ""

    # Run loop while user is in embalming room
    run = True
    while run:
        # Clear the screen
        screen.fill((255, 255, 255))

        # Load the background image
        background = pygame.image.load('assets/img/embalming.png').convert()
        background = pygame.transform.scale(background, (screen.get_width(), screen.get_height()))
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

        # Load the table image
        jar = pygame.image.load("assets/img/jar.png").convert_alpha()
        table_jar = pygame.transform.scale(jar, (int(jar.get_width()/2), int(jar.get_height()/2)))


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

        # Load the inventory background
        inventory_image = pygame.image.load("assets/img/Inventory.png").convert_alpha()

        # Set up book image for the inventory
        inventory_book = pygame.image.load("assets/img/inventory_book.png").convert_alpha() 
        inventory_book = pygame.transform.scale(inventory_book, (int(inventory_book.get_width()/5), int(inventory_book.get_height()/5)))
        inventory_font = pygame.font.Font("assets/font/Pixeloid_Font.ttf", 16)
        book_number = inventory_font.render("1", True, (0, 0, 0))        

        # Set up key image for the inventory
        inventory_key = pygame.image.load("assets/img/key.png")
        inventory_key = pygame.transform.scale(inventory_key, (int(inventory_key.get_width()/5), int(inventory_key.get_height()/5)))
        key_number = inventory_font.render("1", True, (0, 0, 0))

        # Set up torch image for the inventory
        inventory_torch = pygame.image.load("assets/img/torch.png")
        inventory_torch = pygame.transform.scale(inventory_torch, (int(inventory_torch.get_width()/6.1), int(inventory_torch.get_height()/6.1)))
        torch_number = inventory_font.render("1", True, (0, 0, 0))  

        # Check if any keys have been pressed
        keys = pygame.key.get_pressed()
        font = pygame.font.Font("assets/font/Pixeloid_Font.ttf", 36)

        # If the user moves left, move the character to the left
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            # Change character image to face left
            is_flip = ""

            # Restrict movement if character goes beyond the left boundary
            if (player_pos[1] >= min_y and player_pos[0] >= 0) or (player_pos[1] < min_y and player_pos[0] >= 70 and player_pos[0] <= 500) or jump:
                player_pos[0] -= vel_x
            elif (player_pos[0] <= 0):
                current_screen = "snake"            # Change the current screen to the snake room if the user passes the left boundary
                player_pos[0] = screen_width - character_img.get_width()

        # If the user moves right, move the character to the right
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            # Change character image to face right
            is_flip = "_flip"

            # Restrict movement if character goes beyond the right boundary
            if (player_pos[1] >= min_y and player_pos[0] <= max_x) or (player_pos[1] < min_y and player_pos[0] >= 60 and player_pos[0] <= 480) or jump:
                player_pos[0] += vel_x
            
            # If the user has dropped off the two jars, move the character to the next room
            elif (player_pos[0] >= max_x) and ('jar1' in inventory or 'jar2' in inventory):
                font = pygame.font.Font("assets/font/Pixeloid_Font.ttf", 30)
                pick_up = font.render("Drop off the two jars in order to leave the room.", True, (255, 255, 255))
                screen.blit(pick_up, (20, 750))
            elif (player_pos[0] >= max_x):
                player_pos = [0, screen.get_rect().centery + 75]
                current_screen = "puzzle"           # Move the character to the puzzle room if the user passes the right boundary

        # If the user moves up, move the character up
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            # Check if the character is within the climbing area
            if player_pos[1] > min_y or (player_pos[1] > 400 and player_pos[0] > 70 and player_pos[0] < 480):
                player_pos[1] -= vel_y

        # If the user moves down, move the character down
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            # Restrict movement if character goes beyond the bottom boundary
            if player_pos[1] < max_y:
                player_pos[1] += vel_y

        # If the user presses P, drop the jars onto the table
        if keys[pygame.K_p]:
            if player_pos[0] > 700 and player_pos[0] < 1000 and player_pos[1] < 620:
                if 'jar1' in inventory:
                    inventory.remove('jar1')
                if 'jar2' in inventory:
                    inventory.remove('jar2')
            dropped = True

        # If the user presses space, begin jumping
        if jump is False and keys[pygame.K_SPACE]:
            jump = True

        # If the user is jumping, move the character along the parabolic path
        if jump is True:
            player_pos[1] -= jump_y * 6
            jump_y -= 1
            if jump_y < -10:
                jump = False
                jump_y = 10

        # Move the mummy towards the player in both the x and y directions
        if player_pos[0] < mummy_pos[0] and jump is False:
            mummy_flip = ""
            mummy_pos[0] -= mummy_speed
        elif player_pos[0] > mummy_pos[0] and jump is False:
            mummy_flip = "_flip"
            mummy_pos[0] += mummy_speed
        if player_pos[1] < mummy_pos[1] and jump is False:
            mummy_pos[1] -= mummy_speed
        elif player_pos[1] > mummy_pos[1] and jump is False:
            mummy_pos[1] += mummy_speed

        # Load the mummy image
        mummy = pygame.image.load(f"assets/img/mummy{mummy_flip}.png").convert_alpha()

        # Restrict the mummy's movement to the visible floor area
        if mummy_pos[0] < 0:
            mummy_pos[0] = 0
        elif mummy_pos[0] > screen_width - mummy.get_width():
            mummy_pos[0] = screen_width - mummy.get_width()
        if mummy_pos[1] < 475:
            mummy_pos[1] = 475

        # If the mummy touches the player, the player loses a life and is reset to the starting position
        if (mummy_pos[0] >= player_pos[0] and mummy_pos[0] < (player_pos[0] + character_img.get_width())) or (player_pos[0] >= mummy_pos[0] and player_pos[0] < (mummy_pos[0] + mummy.get_width())):
            if (mummy_pos[1] >= player_pos[1] and mummy_pos[1] < (player_pos[1] + character_img.get_height())) or (player_pos[1] >= mummy_pos[1] and player_pos[1] < (mummy_pos[1] + mummy.get_height())):
                lives -= 1
                player_pos = [0, screen.get_rect().centery + 75]
                mummy_pos = [570, 475]

        # Draw the mummy on the screen
        screen.blit(mummy, (mummy_pos[0], mummy_pos[1]))

        # Place jars on the table
        if 'jar1' not in inventory and dropped == True:
            screen.blit(table_jar, (740, 380))
        if 'jar2' not in inventory and dropped == True:
            screen.blit(table_jar, (940, 380))

        # If the user clicks on the backpack, open the inventory
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if mouse_x >= 1100 and mouse_x <= 1200 and mouse_y >= 700 and mouse_y <= 800:
                    inventoryRender = True

        # If the inventory is open, display the inventory
        while inventoryRender:
            # Display the inventory background
            screen.blit(inventory_image, (10, 720))

            # If the user has the torch, display the torch
            if "torch" in inventory:
                screen.blit(inventory_torch, (30, 720))
                screen.blit(torch_number,(50, 742))

            # If the user has the book, display the book
            if "book" in inventory:
                screen.blit(inventory_book, (70, 723))
                screen.blit(book_number,(110, 742))

            # If the user has the jars, display the jars
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

            # If the user has the key, display the key
            if "key" in inventory:
                screen.blit(inventory_key, (170, 730))
                screen.blit(key_number,(220, 742))

            # Draw the character image and backpack on the screen
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
        
        # Draw the character image and backpack on the screen
        screen.blit(character_img, (player_pos[0], player_pos[1]))
        screen.blit(backpack, (backpack_x, backpack_y))

        # Drop the jars on the table
        if player_pos[0] > 700 and player_pos[0] < 1000 and player_pos[1] < 620 and 'jar1' in inventory and 'jar2' in inventory:
            drop_jar = font.render("Press P to drop the two jars", True, (255, 255, 255))
            screen.blit(drop_jar, (20, 750))
        
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

        # Delay each frame by 30 milliseconds
        pygame.time.delay(30)

        # Exit the loop if the screen changes
        if current_screen != "embalming":
            break

        # Exit the loop if the time runs out or the player loses all their lives
        if pygame.time.get_ticks() - start_time >= 180000 or lives <= 0:
            current_screen = "end"
            break

    return inventory, is_flip, current_screen, player_pos, lives