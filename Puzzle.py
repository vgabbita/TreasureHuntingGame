# File Name: Puzzle.py
# Team Members: Nikhil Osuri, Ayush Bobra, Ranvith Adulla, Varun Gabbita
# Date: 06/09/23
# Description: Creates environment for puzzle room, with hieroglyphics on the wall

# Import necessary library
import pygame

# Initialize global variables
move_room = []
inventoryRender = False
scrollRender = False


def puzzle(screen, current_screen, inventory, start_time, character, is_flip, player_pos, movement_speed, lives):
    # Initialize global variables
    global move_room, inventoryRender, scrollRender
    movement_speed = movement_speed *2

    # Clear the screen
    screen.fill((255,255,255))

    # Load the background image
    background = pygame.image.load("assets/img/puzzleroom.png").convert_alpha()
    screen.blit(background, (0, 0))

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

    # Draw the backpack on the screen
    screen.blit(backpack, (backpack_x, backpack_y))

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

    # Set up scroll image
    scroll = pygame.image.load("assets/img/secret_scroll.png").convert_alpha()

    # Set up puzzle input box
    input_box_width = 200
    input_box_height = 50
    input_box_color = pygame.Color("gray80")
    input_box_text_color = pygame.Color("black")
    input_box_rect = pygame.Rect((screen_width - input_box_width) // 2, (screen_height - input_box_height) // 2,
                                input_box_width, input_box_height)
    input_text = ""
    input_code = 'False'

    # Render and draw the input text
    text_surface = inventory_font.render(input_text, True, input_box_text_color)
    text_rect = text_surface.get_rect(center=input_box_rect.center)
    
    # If the backpack is clicked, render the inventory
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if mouse_x >= 1100 and mouse_x <= 1200 and mouse_y >= 700 and mouse_y <= 800:
                inventoryRender = True

    # If the inventory is rendered, display the inventory
    while inventoryRender:
        # If the scroll is clicked, render the scroll
        if scrollRender:
            screen.blit(scroll, (screen.get_width()//2 - scroll.get_width()//2, screen.get_height()//2 - scroll.get_height()//2))

        # Display the inventory background
        screen.blit(inventory_image, (10, 720))

        # Display the torch, if it is in the inventory
        if "torch" in inventory:
            screen.blit(inventory_torch, (30, 720))
            screen.blit(torch_number,(50, 742))

        # Display the book, if it is in the inventory
        if "book" in inventory:
            screen.blit(inventory_book, (70, 723))
            screen.blit(book_number,(110, 742))

        # Display the jars, if they are in the inventory
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

        # Display the key, if it is in the inventory
        if "key" in inventory:
            screen.blit(inventory_key, (170, 730))
            screen.blit(key_number,(220, 742))

        # Display the character image and backpack
        screen.blit(character_img, (player_pos[0], player_pos[1]))
        screen.blit(backpack, (backpack_x, backpack_y))

        for event in pygame.event.get():
            # If the user quits, close the window
            if event.type == pygame.QUIT:
                pygame.quit()
                break

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                # If the user clicks on the book, render the scroll
                if mouse_x >= 70 and mouse_x <= 110 and mouse_y >= 720 and mouse_y <= 750:
                    scrollRender = not scrollRender

                # If the user clicks on the backpack, unrender the inventory
                if mouse_x >= 1100 and mouse_x <= 1200 and mouse_y >= 700 and mouse_y <= 800:
                    inventoryRender = False
                    scrollRender = False

        # Update the display
        pygame.display.update()

    # Add a heart for each life the player has
    if lives > 0:
        heart = pygame.image.load("assets/img/heart.png").convert_alpha()
        screen.blit(heart, (screen.get_width() - heart.get_width() - 20, 20))
    if lives > 1:
        screen.blit(heart, (screen.get_width() - heart.get_width()*2 - 40, 20))
    if lives > 2:
        screen.blit(heart, (screen.get_width() - heart.get_width()*3 - 60, 20))

    # Checks if any keys are pressed
    keys = pygame.key.get_pressed()
    font = pygame.font.Font("assets/font/Pixeloid_Font.ttf", 36)

    # If the player moves left, move the character left
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        is_flip = ""
        if player_pos[1] >= min_y:
            if player_pos[0] >= 0:
                player_pos[0] -= movement_speed
            else:
                player_pos = [screen_width - character_img.get_width(), screen.get_rect().centery + 75]
                current_screen = "embalming"        # Change the current screen to the embalming room if the player is beyond the left border

    # If the player moves right, move the character right
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        is_flip = "_flip"
        if player_pos[1] >= min_y:
            if player_pos[0] < max_x:
                player_pos[0] += movement_speed
            else:
                if 'passed' in move_room:
                    if 'key' in inventory:
                        player_pos = [0, screen.get_rect().centery + 75]
                        current_screen = "tomb"     # Change the current screen to the tomb room if the player is beyond the right border
                    else:
                        pick_up = font.render("This room is locked.", True, (255, 255, 255))
                        screen.blit(pick_up, (20, 750))     # If the player does not have the key, display a message
                else:
                    pick_up = font.render("Enter the code in order to leave.", True, (255, 255, 255))       # If the player has not passed the room, display a message
                    screen.blit(pick_up, (20, 750))

    # If the player moves up, move the character up
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        if player_pos[1] > min_y:
            player_pos[1] -= movement_speed

    # If the player moves down, move the character down
    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        if player_pos[1] < max_y:
            player_pos[1] += movement_speed

    # If the player presses X, open the input box
    if keys[pygame.K_x]:
        # do the nubmers
        input_code = 'True'

    while input_code == 'True':
        # Draw the input box
        pygame.draw.rect(screen, input_box_color, input_box_rect)
        pygame.draw.rect(screen, input_box_text_color, input_box_rect, 2)

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                # Remove the last character from input_text when backspace is pressed
                if event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]

                # Append the pressed character to input_text
                elif event.unicode.isnumeric():
                    input_text += event.unicode
                elif event.key == pygame.K_RETURN:
                    # If the user has entered the correct code, they can move on
                    if input_text == "149":
                        move_room.append('passed')
                        input_code = 'False'

                    # If the user has entered the incorrect code, they cannot move on
                    else:
                        pick_up = font.render("Incorrect code.", True, (255, 255, 255))
                        screen.blit(pick_up, (20, 750))
                        input_code = 'False'

        # Render and draw the input text
        text_surface = inventory_font.render(input_text, True, input_box_text_color)
        text_rect = text_surface.get_rect(center=input_box_rect.center)
        screen.blit(text_surface, text_rect)

        # Display the character and backpack on the screen
        screen.blit(character_img, (player_pos[0], player_pos[1]))
        screen.blit(backpack, (backpack_x, backpack_y))

        # Update the display
        pygame.display.update()

    # Display a message if the user passes the room
    if 'passed' in move_room and (player_pos[0] < max_x):
        move = font.render("You entered the correct code!", True, (255, 255, 255))
        screen.blit(move, (20, 750))
    else:
        if player_pos[0] >= 510 and player_pos[0] <= 580 and player_pos[1] >= 475 and player_pos[1] <= 500 and 'passed' not in move_room:
            button = font.render("Press X to press the button", True, (255, 255, 255))
            screen.blit(button, (20, 750))

    # Display the character on the screen
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

    # Updates the display
    pygame.display.update()

    return inventory, is_flip, current_screen, player_pos