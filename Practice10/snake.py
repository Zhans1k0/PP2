import pygame
import random

pygame.init()

WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake")

clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 24)

block = 20

snake = [(100,100)]
dx, dy = block, 0

score = 0
level = 1
speed = 10

# Generate food in safe place
def generate_food():
    while True:
        x = random.randint(0, WIDTH//block-1) * block
        y = random.randint(0, HEIGHT//block-1) * block
        if (x,y) not in snake:
            return (x,y)

food = generate_food()

running = True
while running:
    screen.fill((0,0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                dx, dy = 0, -block
            if event.key == pygame.K_DOWN:
                dx, dy = 0, block
            if event.key == pygame.K_LEFT:
                dx, dy = -block, 0
            if event.key == pygame.K_RIGHT:
                dx, dy = block, 0

    # New head position
    head = (snake[0][0] + dx, snake[0][1] + dy)

    # Wall collision
    if head[0] < 0 or head[0] >= WIDTH or head[1] < 0 or head[1] >= HEIGHT:
        running = False

    # Self collision
    if head in snake:
        running = False

    snake.insert(0, head)

    # Check food
    if head == food:
        score += 1

        # Increase level every 4 points
        if score % 4 == 0:
            level += 1
            speed += 2

        food = generate_food()
    else:
        snake.pop()

    # Draw snake
    for s in snake:
        pygame.draw.rect(screen, (0,255,0), (*s, block, block))

    # Draw food
    pygame.draw.rect(screen, (255,0,0), (*food, block, block))

    # Draw UI
    screen.blit(font.render(f"Score: {score}", True, (255,255,255)), (10,10))
    screen.blit(font.render(f"Level: {level}", True, (255,255,255)), (10,40))

    pygame.display.update()
    clock.tick(speed)

pygame.quit()