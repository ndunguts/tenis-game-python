import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the screen
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("War Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Player settings
player_width = 50
player_height = 50
player_speed = 5
player_x = screen_width // 2 - player_width // 2
player_y = screen_height - player_height - 20

# Enemy settings
enemy_width = 50
enemy_height = 50
enemy_speed = 3

# Bullet settings
bullet_width = 5
bullet_height = 15
bullet_speed = 7

# Fonts
font = pygame.font.Font(None, 36)

# Function to draw text on screen
def draw_text(text, color, x, y):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

# Function to draw player
def draw_player(x, y):
    pygame.draw.rect(screen, WHITE, (x, y, player_width, player_height))

# Function to draw enemy
def draw_enemy(x, y):
    pygame.draw.rect(screen, RED, (x, y, enemy_width, enemy_height))

# Function to draw bullets
def draw_bullet(x, y):
    pygame.draw.rect(screen, WHITE, (x, y, bullet_width, bullet_height))

# Main game loop
game_over = False
while not game_over:
    # Reset game variables
    bullets = []
    enemies = []

    # Main game loop
    running = True
    while running:
        screen.fill(BLACK)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                game_over = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bullets.append([player_x + player_width // 2 - bullet_width // 2, player_y])

        # Player movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] and player_x < screen_width - player_width:
            player_x += player_speed

        # Enemy spawning
        if len(enemies) < 5:
            enemy_x = random.randint(0, screen_width - enemy_width)
            enemy_y = random.randint(-500, -enemy_height)
            enemies.append([enemy_x, enemy_y])

        # Update and draw enemies
        for enemy in enemies:
            enemy[1] += enemy_speed
            draw_enemy(enemy[0], enemy[1])

            # Collision detection
            enemy_rect = pygame.Rect(enemy[0], enemy[1], enemy_width, enemy_height)
            player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
            if enemy_rect.colliderect(player_rect):
                draw_text("Game Over. Press R to restart.", RED, screen_width // 2 - 200, screen_height // 2)
                pygame.display.update()
                running = False

        # Update and draw bullets
        for bullet in bullets:
            bullet[1] -= bullet_speed
            draw_bullet(bullet[0], bullet[1])

            # Remove bullets when they go off-screen
            if bullet[1] < 0:
                bullets.remove(bullet)

        # Check for bullet-enemy collision
        for bullet in bullets:
            bullet_rect = pygame.Rect(bullet[0], bullet[1], bullet_width, bullet_height)
            for enemy in enemies:
                enemy_rect = pygame.Rect(enemy[0], enemy[1], enemy_width, enemy_height)
                if bullet_rect.colliderect(enemy_rect):
                    bullets.remove(bullet)
                    enemies.remove(enemy)

        # Update the display
        draw_player(player_x, player_y)
        pygame.display.update()

        # FPS
        pygame.time.Clock().tick(60)

        # Check for restart
        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            break

# Quit Pygame
pygame.quit()
