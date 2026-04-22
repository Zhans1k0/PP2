import pygame
import random

pygame.init()

WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racer")

clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 24)

# Player setup
player = pygame.Rect(WIDTH//2, HEIGHT-80, 40, 60)

# Coin setup
coin_x = random.randint(50, WIDTH-50)
coin_y = -50
coin_speed = 5

coins = 0

running = True
while running:
    screen.fill((30,30,30))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    # Move player left/right
    if keys[pygame.K_LEFT]:
        player.x -= 5
    if keys[pygame.K_RIGHT]:
        player.x += 5

    # Keep player inside screen
    player.x = max(0, min(WIDTH-40, player.x))

    # Move coin down
    coin_y += coin_speed

    # Reset coin when off screen
    if coin_y > HEIGHT:
        coin_y = -50
        coin_x = random.randint(50, WIDTH-50)

    coin_rect = pygame.Rect(coin_x, coin_y, 30, 30)

    # Check collision with player
    if player.colliderect(coin_rect):
        coins += 1
        coin_y = -50
        coin_x = random.randint(50, WIDTH-50)

    # Draw player and coin
    pygame.draw.rect(screen, (0,255,0), player)
    pygame.draw.circle(screen, (255,255,0), (coin_x, coin_y), 15)

    # Draw coin counter (top-right)
    text = font.render(f"Coins: {coins}", True, (255,255,255))
    screen.blit(text, (WIDTH-140, 10))

    pygame.display.update()
    clock.tick(60)

pygame.quit()