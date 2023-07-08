import pygame
import random

width = 800
height = 600
white = (255, 255, 255)

game_over = False

# pygame setup
pygame.init()
pygame.mixer.init()

window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Chicken Invaders: Ike Edition")

# Set up the sounds
bullet_sound = pygame.mixer.Sound("bullet_sound.mp3")
explosion_sound = pygame.mixer.Sound("explosion_sound.wav")

# Player metrics
player_image = pygame.image.load("player.png")
player_width, player_height = 64, 64
player_x, player_y = (width - player_width) / 2, height - player_height - 10
player_image = pygame.transform.scale(player_image, (player_width, player_height))

# Chicken metrics
chicken_image = pygame.image.load("alien.png")
chicken_width, chicken_height = 32, 32
chicken_x, chicken_y = random.randint(0, width - chicken_width), random.randint(50, height / 2)
chicken_image = pygame.transform.scale(chicken_image, (chicken_width, chicken_height))
chicken_speed = .5

# Bullet metrics
# Set up the bullets
bullet_image = pygame.image.load("bomb.png")
bullet_width, bullet_height = 32, 32
bullet_image = pygame.transform.scale(bullet_image, (bullet_width, bullet_height))
bullet_x, bullet_y = 0, height - player_height - 10
bullet_speed = 6
bullet_state = "ready"  # "ready" -> ready to fire, "fire" -> bullet is moving


running = True

level = 1
level_font = pygame.font.Font(None, 36)

# Set up scoring
score = 0
score_font = pygame.font.Font(None, 24)

# menu_font = pygame.font.Font(None, 48)
# # Set up the menu options
# menu_options = ["Play", "Quit"]


# # Function to handle the menu
# def show_menu(selected_option):
#     menu_running = True

#     while menu_running:
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 pygame.quit()
#                 quit()

#             if event.type == pygame.KEYDOWN:
#                 if event.key == pygame.K_UP:
#                     selected_option = (selected_option - 1) % len(menu_options)
#                 elif event.key == pygame.K_DOWN:
#                     selected_option = (selected_option + 1) % len(menu_options)

#             if event.type == pygame.KEYUP:
#                 if event.key == pygame.K_RETURN:
#                     if selected_option == 0:
#                         menu_running = False
#                     elif selected_option == 1:
#                         pygame.quit()
#                         quit()

#         window.fill('sky blue')

#         for i, option in enumerate(menu_options):
#             if i == selected_option:
#                 text = menu_font.render("> " + option, True, white)
#             else:
#                 text = menu_font.render(option, True, white)

#             window.blit(text, (width // 2 - 75, height // 2 + i * 50))

#         pygame.display.update()

#     return selected_option


# Set up the timer
timer_value = 15  # in seconds
timer_font = pygame.font.Font(None, 24)
timer_started = False
timer_paused = False
timer_event = pygame.USEREVENT + 1


# Function to play bullet sound
def play_bullet_sound():
    bullet_sound.play()

# Function to play explosion sound
def play_explosion_sound():
    explosion_sound.play()

# Function to draw the level on the screen
def draw_level():
    level_text = level_font.render("Level: " + str(level), True, white)
    window.blit(level_text, (10, 10))


# Function to draw the score on the screen
def draw_score():
    score_text = score_font.render("Score: " + str(score), True, white)
    window.blit(score_text, (10, 40))


# Function to draw the timer on the screen
def draw_timer():
    timer_text = timer_font.render("Time: " + str(timer_value), True, white)
    window.blit(timer_text, (10, 70))


# Check if timer is zero
def is_timer_zero(timer_value):
    if timer_value == 0:
        return True
    return False


# Function to draw the chicken
def draw_chicken(x, y):
    window.blit(chicken_image, (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    window.blit(bullet_image, (x + player_width / 2 - bullet_width / 2, y - bullet_height))


# Function to check collision between bullet and chicken
def is_collision(chicken_x, chicken_y, bullet_x, bullet_y):
    if bullet_x < chicken_x + chicken_width and bullet_x + bullet_width > chicken_x and bullet_y < chicken_y + chicken_height and bullet_y + bullet_height > chicken_y:
        return True
    return False


# Create a list of chickens
chickens = []
num_chickens = 2 * level
for i in range(num_chickens):
    chicken_x = random.randint(0, width - chicken_width)
    chicken_y = random.randint(50, height / 2)
    chicken = {"x": chicken_x, "y": chicken_y, "speed": chicken_speed}
    chickens.append(chicken)

# selected_option = 0
while running:
    
    # Show the menu and get the selected option
    # selected_option = show_menu(selected_option)

    # Check the selected option and take appropriate action
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL:
                    if bullet_state == "ready":
                        bullet_x = player_x
                        fire_bullet(bullet_x, bullet_y)
                        play_bullet_sound()

        # Start the timer when the game starts
        if event.type == pygame.KEYDOWN and event.key == pygame.K_LCTRL or event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT or event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
            if not timer_started:
                pygame.time.set_timer(timer_event, 1000)
                timer_started = True

        # Handle the timer event
        if event.type == timer_event:
            if timer_value > 0 and not timer_paused:
                timer_value -= 1

    window.fill('sky blue')

    # Draw the player
    window.blit(player_image, (player_x, player_y))

    # Move the player
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= 5
    if keys[pygame.K_RIGHT] and player_x < width - player_width:
        player_x += 5

    # Draw the bullet
    if bullet_state == "fire":
        fire_bullet(bullet_x, bullet_y)
        bullet_y -= bullet_speed

    # Check collision between bullet and chickens
    for chicken in chickens:
        chicken_x = chicken["x"]
        chicken_y = chicken["y"]
        if is_collision(chicken_x, chicken_y, bullet_x, bullet_y):
            bullet_state = "ready"
            bullet_y = height - player_height - 10
            chickens.remove(chicken)
            score += 1
            play_explosion_sound()

    # Reset the bullet when it goes off the screen
    if bullet_y <= 0:
        bullet_state = "ready"
        bullet_y = height - player_height - 10

    # Draw the chickens
    for chicken in chickens:
        chicken_x = chicken["x"]
        chicken_y = chicken["y"]
        draw_chicken(chicken_x, chicken_y)

    # Check collision between bullet and chicken
    if is_collision(chicken_x, chicken_y, bullet_x, bullet_y):
        bullet_state = "ready"
        bullet_y = height - player_height - 10
        chicken_x = random.randint(0, width - chicken_width)
        chicken_y = random.randint(50, height / 2)

    # Move the chickens
    for chicken in chickens:
        chicken_x = chicken["x"]
        chicken_y = chicken["y"]
        chicken_speed = chicken["speed"]
        chicken_x += chicken_speed
        if chicken_x <= 0 or chicken_x >= width - chicken_width:
            chicken_speed *= -1
        chicken["x"] = chicken_x
        chicken["y"] = chicken_y
        chicken["speed"] = chicken_speed

    # Draw the level
    draw_level()

    # Draw the score
    draw_score()

    # Draw the timer
    draw_timer()

    # Check if all chickens are destroyed and increase the level
    if len(chickens) == 0:
        level += 1
        num_chickens = 2 * level
        for i in range(num_chickens):
            chicken_x = random.randint(0, width - chicken_width)
            chicken_y = random.randint(50, height / 2)
            chicken = {"x": chicken_x, "y": chicken_y, "speed": chicken_speed}
            chickens.append(chicken)

        # Reset the timer
        timer_value = 15
        timer_started = False
        pygame.time.set_timer(timer_event, 0)

    if is_timer_zero(timer_value):
        game_over = True

    if game_over:
        # Display "Game Over" message
        game_over_text = level_font.render("Game Over", True, white)
        window.blit(game_over_text, (width // 2 - 50, height // 2))
        pygame.display.update()

        # Wait for a brief moment
        pygame.time.delay(5000)

        # Quit the game
        running = False

    pygame.display.update()

pygame.quit()