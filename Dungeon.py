# File Name: Dungeon.py
# Team Members: Nikhil Osuri, Ayush Bobra, Ranvith Adulla, Varun Gabbita
# Date: 06/09/23
# Description: Creates environment for dungeon and monster that shoots fireballs

# Import necessary libraries
import pygame
import sys

# Initialize inventory to not show
inventoryRender = False

# Defines dungeon function
def dungeon(current_screen, screen, character, inventory, is_flip, player_pos, movement_speed, start_time, lives, time):
    # Sets up variables for jumping
    vel_x = movement_speed * 2
    vel_y = movement_speed * 2
    jump_y = 10
    jump = False

    # Sets up variables for monster
    direction = "up"
    monster_pos = [800, 500]

    # Sets up variables for fireball
    fireball_present = False
    fireball_pos = [0, 0]

    # Sets up inventory
    global inventoryRender

    # Loops while the player is in the dungeon room
    run = True
    while run:
        # Clear the screen
        screen.fill((255,255,255))

        # Draw the background image
        background = pygame.image.load("assets/img/dungeon.jpg").convert_alpha()
        screen.blit(background, (0, 0))

        # Draw a heart for each life the player has
        if lives > 0:
            heart = pygame.image.load("assets/img/heart.png").convert_alpha()
            screen.blit(heart, (screen.get_width() - heart.get_width() - 20, 20))
        if lives > 1:
            screen.blit(heart, (screen.get_width() - heart.get_width()*2 - 40, 20))
        if lives > 2:
            screen.blit(heart, (screen.get_width() - heart.get_width()*3 - 60, 20))

        # Loads the sphinx image
        monster = pygame.image.load("assets/img/sphinx.png").convert_alpha()
        monster = pygame.transform.flip(monster, True, False)
        monster = pygame.transform.scale(monster, (monster.get_width()//3.5, monster.get_height()//3.5))

        # Moves sphinx up or down, depending on current position
        if direction == "up":
            monster_pos[1] -= movement_speed
            if monster_pos[1] <= 450:
                direction = "down"
        elif direction == "down":
            monster_pos[1] += movement_speed
            if monster_pos[1] >= 640:
                direction = "up"

        # Draws the monster on the screen
        screen.blit(monster, (monster_pos[0], monster_pos[1]))

        # If a fireball is not present, create one
        if fireball_present is False:
            fireball_present = True
            fireball = pygame.image.load("assets/img/fireball.png").convert_alpha()
            fireball = pygame.transform.flip(fireball, True, False)
            fireball = pygame.transform.scale(fireball, (fireball.get_width()//5, fireball.get_height()//5))
            fireball_pos = [monster_pos[0] - fireball.get_width(), monster_pos[1] + 35]
            screen.blit(fireball, (fireball_pos[0], fireball_pos[1]))

        # If a fireball is present, move it across the screen
        else:
            fireball_pos[0] -= movement_speed * 5
            screen.blit(fireball, (fireball_pos[0], fireball_pos[1]))

        # If a fireball makes it across the screen, reset it
        if fireball_pos[0] <= 0:
            fireball_present = False

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

        #Set up key image for the inventory
        inventory_key = pygame.image.load("assets/img/key.png")
        inventory_key = pygame.transform.scale(inventory_key, (int(inventory_key.get_width()/5), int(inventory_key.get_height()/5)))
        key_number = inventory_font.render("1", True, (0, 0, 0))

        #set up torch image for the inventory
        inventory_torch = pygame.image.load("assets/img/torch.png")
        inventory_torch = pygame.transform.scale(inventory_torch, (int(inventory_torch.get_width()/6.1), int(inventory_torch.get_height()/6.1)))
        torch_number = inventory_font.render("1", True, (0, 0, 0))

        # Load the character image
        character_img = pygame.image.load(f"assets/img/{character}{is_flip}.png").convert_alpha()

        # Set the maximum boundaries of the screen
        screen_width = screen.get_width()
        screen_height = screen.get_height()
        min_y = screen.get_rect().centery + 75
        max_x = screen_width - character_img.get_width()
        max_y = screen_height - character_img.get_height()

        # Checks if user has pressed any keys
        keys = pygame.key.get_pressed()

        # If user moved left, move the character left
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            # Change character image to face left
            is_flip = ""

            # Restrict movement if character goes beyond the left boundary
            if player_pos[0] > 0:
                player_pos[0] -= vel_x
            else:
                player_pos = [screen_width - character_img.get_width(), screen.get_rect().centery + 75]
                current_screen = "entrance"             # Switch screen to entrance if character goes beyond left boundary

        # If user moved right, move the character right
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            # Change character image to face right
            is_flip = "_flip"

            # Restrict movement if character goes beyond the right boundary
            if player_pos[0] < max_x:
                player_pos[0] += vel_x
            else:
                player_pos = [0, screen.get_rect().centery + 75]
                current_screen = "library"              # Switch screen to library if character goes beyond right boundary

        # If user moved up, move the character up
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            # Restrict movement if character goes beyond the top boundary
            if player_pos[1] > min_y:
                player_pos[1] -= vel_y

        # If user moved down, move the character down
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            # Restrict movement if character goes beyond the bottom boundary
            if player_pos[1] < max_y:
                player_pos[1] += vel_y

        # If user pressed spacebar, jump
        if jump is False and keys[pygame.K_SPACE]:
            jump = True

        # If user is jumping, move the character along the parabolic path
        if jump is True:
            player_pos[1] -= jump_y * 4.2
            jump_y -= 1
            if jump_y < -10:
                jump = False
                jump_y = 10

        # If the user clicks the backpack, render the inventory
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if mouse_x >= 1100 and mouse_x <= 1200 and mouse_y >= 700 and mouse_y <= 800:
                    inventoryRender = True

        # If the inventory is opened, show the inventory
        while inventoryRender:
            # Displays the inventory background
            screen.blit(inventory_image, (10, 720))

            # Displays the torch, if the user has it
            if "torch" in inventory:
                screen.blit(inventory_torch, (30, 720))
                screen.blit(torch_number, (50, 742))

            # Displays the book, if the user has it
            if "book" in inventory:
                screen.blit(inventory_book, (70, 723))
                screen.blit(book_number, (100, 742))

            # Displays the jars, if the user has them
            if ("jar1" in inventory) and ("jar2" in inventory):
                jar_counter = 2
                jar_number = inventory_font.render(str(jar_counter), True, (0, 0, 0))
                screen.blit(inventory_jar, (120, 723))
                screen.blit(jar_number, (170, 742))
            elif ("jar1" in inventory) or ("jar2" in inventory):
                jar_counter = 1
                jar_number = inventory_font.render(str(jar_counter), True, (0, 0, 0))
                screen.blit(inventory_jar, (120, 723))
                screen.blit(jar_number, (170, 742))

            # Displays the key, if the user has it
            if "key" in inventory:
                screen.blit(inventory_key, (170, 730))
                screen.blit(key_number,(170, 742))

            # Show the character and backpack on the screen
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

        # Draw the character on the screen
        screen.blit(character_img, (player_pos[0], player_pos[1]))

        # If the player contacts the monster, they lose a life and are reset to the starting position
        if (player_pos[0] >= 700 and player_pos[0] <= 830) and player_pos[1] >= 400 and (player_pos[1] - monster_pos[1] < 150):
            lives -= 1
            player_pos = [0, screen.get_rect().centery + 75]

        # IF the player contacts the fireball, they lose a life and are reset to the starting position
        if (player_pos[0] + character_img.get_width() >= fireball_pos[0] and player_pos[0] <= fireball_pos[0] + fireball.get_width()) and (fireball_pos[1] + 3*fireball.get_height()//4 >= player_pos[1] and fireball_pos[1] + 3*fireball.get_height()//4 <= player_pos[1] + character_img.get_height()):
            lives -= 1
            player_pos = [0, screen.get_rect().centery + 75]
            fireball_present = False        # Reset the fireball

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

        # Update the screen
        pygame.display.update()

        # If the user quits, close the window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                sys.exit()

        # Delay each frame by 30 milliseconds
        pygame.time.delay(30)

        # Exits the loop if the screen has changed
        if current_screen != "dungeon":
            break

        # Exits the loop if the time has run out or the player has lost all their lives
        if pygame.time.get_ticks() - start_time >= 180000 or lives <= 0:
            current_screen = "end"
            break

    return is_flip, time, current_screen, inventory, player_pos, lives