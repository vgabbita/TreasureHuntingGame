# File Name: Library.py
# Team Members: Nikhil Osuri, Ayush Bobra, Ranvith Adulla, Varun Gabbita
# Date: 06/09/23
# Description: Creates library room that requires torch to properly see

# Import necessary library
import pygame

# Initializes inventory to not show
inventoryRender = False

# Defines library function
def library(inventory, screen, character, is_flip, player_pos, movement_speed, start_time, current_screen, lives):
    # Initializes inventory
    global inventoryRender

    # Clear the screen
    screen.fill((255,255,255))

    # Load the background image
    library_background = pygame.image.load("assets/img/library.png").convert()
    screen.blit(library_background, (0, 0))

    # Load the character image
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

    # If the player does not have the book, draw the book
    if "book" not in inventory:
        book = pygame.image.load("assets/img/book.png").convert_alpha()
        screen.blit(book, (1062, 274))

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

    # If the player does not have the torch, the entire screen except a small area around the character is dark
    if "torch" not in inventory:
        # Fill the screen with a black surface
        dark = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        dark.fill((0, 0, 0))

        # Draw a transparent circle, centered on the character
        circle_center = (player_pos[0] + character_img.get_width() // 2, player_pos[1] + character_img.get_height() // 2)
        pygame.draw.circle(dark, (0, 0, 0, 200), circle_center, 80, 0)

        # Add the dark surface to the screen
        screen.blit(dark, (0, 0))

    # Adds a heart for each life the player has
    if lives > 0:
        heart = pygame.image.load("assets/img/heart.png").convert_alpha()
        screen.blit(heart, (screen.get_width() - heart.get_width() - 20, 20))
    if lives > 1:
        screen.blit(heart, (screen.get_width() - heart.get_width()*2 - 40, 20))
    if lives > 2:
        screen.blit(heart, (screen.get_width() - heart.get_width()*3 - 60, 20))

    # Checks if the user has pressed any keys
    keys = pygame.key.get_pressed()
    font = pygame.font.Font("assets/font/Pixeloid_Font.ttf", 36)

    # If the user moves left, move the character left
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        # Change character image to face left
        is_flip = ""

        # Restrict movement if character goes beyond the left boundary
        if player_pos[1] >= 475:
            if player_pos[0] > 0:
                player_pos[0] -= movement_speed
            else:
                player_pos = [screen_width - character_img.get_width(), screen.get_rect().centery + 75]
                current_screen = "dungeon"          # Change the screen to the dungeon if player goes beyond the left boundary

        # Allows character to move on bookshelves
        else:
            if player_pos[0] > 0 and player_pos[0] <= 330:
                if player_pos[1] <= 78:
                    player_pos[1] = 78
                    player_pos[0] -= movement_speed
                if player_pos[1] >= 245 and player_pos[1] <= 293:
                    player_pos[1] = 293
                    player_pos[0] -= movement_speed
            elif player_pos[0] > 760:
                player_pos[0] -= movement_speed

    # If the user moves right, move the character right
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        # Change character image to face right
        is_flip = "_flip"

        # Restrict movement if character goes beyond the right boundary
        if player_pos[1] >= 475:
            if player_pos[0] < max_x:
                player_pos[0] += movement_speed
            else:
                player_pos = [0, screen.get_rect().centery + 75]
                current_screen = "temple"       # Change the screen to the temple if player goes beyond the right boundary

        # Allows character to move on bookshelves
        else:
            if player_pos[0] < 330:
                player_pos[0] += movement_speed
            elif player_pos[0] < max_x and player_pos[0] >= 760:
                if player_pos[1] <= 78:
                    player_pos[1] = 78
                    player_pos[0] += movement_speed
                if player_pos[1] >= 245 and player_pos[1] <= 293:
                    player_pos[1] = 293
                    player_pos[0] += movement_speed

    # If the user moves up, move the character up
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        # Restrict movement if character goes beyond the top boundary
        if player_pos[1] > min_y:
            player_pos[1] -= movement_speed
        
        # Allows character to move on ladder
        elif player_pos[1] > 0:
            if player_pos[0] >= 285 and player_pos[0] <= 330 or player_pos[0] >= 760 and player_pos[0] <= 805:
                player_pos[1] -= movement_speed

    # If the user moves down, move the character down
    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        # Restrict movement if character goes beyond the bottom boundary
        if player_pos[1] < max_y and player_pos[1] >= 475:
            player_pos[1] += movement_speed
        
        # Allows character to move on ladder
        else:
            if player_pos[0] >= 285 and player_pos[0] <= 330 or player_pos[0] >= 760 and player_pos[0] <= 805:
                player_pos[1] += movement_speed

    # If the user presses X, check if they are in the right position to pick up the book
    if keys[pygame.K_x]:
        if player_pos[0] >= 955 and player_pos[0] <= 1085 and player_pos[1] >= 245 and player_pos[1] <= 293:
            if "book" not in inventory:
                # Checks if the inventory is full
                if len(inventory) > 4:
                    too_many = font.render("You can only carry 4 items!", True, (255, 255, 255))
                    screen.blit(too_many, (20, 750))

                # Adds the book to the inventory
                else:
                    inventory.append("book")

    # If the user presses the backpack, open the inventory
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if mouse_x >= 1100 and mouse_x <= 1200 and mouse_y >= 700 and mouse_y <= 800:
                inventoryRender = True

    # If the inventory is open, show the inventory
    while inventoryRender:
        # Displays the inventory background
        screen.blit(inventory_image, (10, 720))

        # Displays the torch, if the user has it
        if "torch" in inventory:
            screen.blit(inventory_torch, (30, 720))
            screen.blit(torch_number,(50, 742))

        # Displays the book, if the user has it
        if "book" in inventory:
            screen.blit(inventory_book, (70, 723))
            screen.blit(book_number,(110, 742))

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

        # Displays the character and backpack
        screen.blit(character_img, (player_pos[0], player_pos[1]))
        screen.blit(backpack, (backpack_x, backpack_y))

        for event in pygame.event.get():
            # If the user quits, close the window
            if event.type == pygame.QUIT:
                pygame.quit()
                break

            # If the user presses the backpack, close the inventory
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if mouse_x >= 1100 and mouse_x <= 1200 and mouse_y >= 700 and mouse_y <= 800:
                    inventoryRender = False

        # Update the display
        pygame.display.update()

    # Displays the character image
    screen.blit(character_img, (player_pos[0], player_pos[1]))

    # Displays the text to pick up the book if the user is in the right position
    font = pygame.font.Font("assets/font/Pixeloid_Font.ttf", 36)
    if "book" not in inventory:
        if player_pos[0] >= 955 and player_pos[0] <= 1085 and player_pos[1] >= 245 and player_pos[1] <= 293:
            pick_up = font.render("Press X to pick up book", True, (255, 255, 255))
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

    return inventory, is_flip, time, current_screen, player_pos