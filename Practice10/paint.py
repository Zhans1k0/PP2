import pygame

pygame.init()

# Screen setup
WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint")

clock = pygame.time.Clock()

# Canvas (where drawing happens)
canvas = pygame.Surface((WIDTH, HEIGHT))
canvas.fill((255, 255, 255))  # white background

# Drawing settings
drawing = False
tool = "pen"   # pen, rect, circle, eraser
color = (0, 0, 0)
start_pos = (0, 0)

# Color palette
colors = [
    (255, 0, 0),   # red
    (0, 255, 0),   # green
    (0, 0, 255),   # blue
    (0, 0, 0)      # black
]

running = True
while running:
    # Show canvas
    screen.blit(canvas, (0, 0))
    mouse_pos = pygame.mouse.get_pos()

    # Draw color palette buttons
    for i, c in enumerate(colors):
        rect = pygame.Rect(10 + i*40, 10, 30, 30)
        pygame.draw.rect(screen, c, rect)

        # Change color on click
        if rect.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0]:
            color = c

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Tool selection via keyboard
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                tool = "rect"
            if event.key == pygame.K_c:
                tool = "circle"
            if event.key == pygame.K_e:
                tool = "eraser"
            if event.key == pygame.K_p:
                tool = "pen"

        # Start drawing
        if event.type == pygame.MOUSEBUTTONDOWN:
            drawing = True
            start_pos = event.pos

        # Finish shape drawing
        if event.type == pygame.MOUSEBUTTONUP:
            drawing = False
            end_pos = event.pos

            # Draw rectangle
            if tool == "rect":
                pygame.draw.rect(
                    canvas,
                    color,
                    (start_pos[0],
                     start_pos[1],
                     end_pos[0] - start_pos[0],
                     end_pos[1] - start_pos[1]),
                    2
                )

            # Draw circle (FIXED VERSION)
            if tool == "circle":
                dx = end_pos[0] - start_pos[0]
                dy = end_pos[1] - start_pos[1]
                radius = int((dx**2 + dy**2) ** 0.5)

                pygame.draw.circle(canvas, color, start_pos, radius, 2)

    # Continuous drawing (pen / eraser)
    if drawing:
        if tool == "pen":
            pygame.draw.circle(canvas, color, mouse_pos, 3)

        if tool == "eraser":
            pygame.draw.circle(canvas, (255, 255, 255), mouse_pos, 10)

    pygame.display.update()
    clock.tick(60)

pygame.quit()