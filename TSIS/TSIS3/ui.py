import pygame

WHITE = (255, 255, 255)
BLACK = (25, 20, 30)
PINK = (255, 140, 190)
LIGHT_PINK = (255, 205, 225)
PURPLE = (170, 100, 220)
DARK_PURPLE = (70, 40, 90)

FONT = None
BIG_FONT = None
SMALL_FONT = None


def init_ui():
    global FONT, BIG_FONT, SMALL_FONT
    FONT = pygame.font.SysFont("arial", 26)
    BIG_FONT = pygame.font.SysFont("arial", 42, bold=True)
    SMALL_FONT = pygame.font.SysFont("arial", 18)


def draw_text(screen, text, x, y, font=None, color=WHITE):
    if font is None:
        font = FONT

    surface = font.render(text, True, color)
    rect = surface.get_rect(center=(x, y))
    screen.blit(surface, rect)


def draw_text_left(screen, text, x, y, font=None, color=WHITE):
    if font is None:
        font = SMALL_FONT

    surface = font.render(text, True, color)
    screen.blit(surface, (x, y))


def button(screen, text, x, y, w, h):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    rect = pygame.Rect(x, y, w, h)

    if rect.collidepoint(mouse):
        pygame.draw.rect(screen, LIGHT_PINK, rect, border_radius=18)
        text_color = BLACK

        if click[0]:
            pygame.time.delay(160)
            return True
    else:
        pygame.draw.rect(screen, PINK, rect, border_radius=18)
        text_color = WHITE

    pygame.draw.rect(screen, WHITE, rect, 2, border_radius=18)
    draw_text(screen, text, x + w // 2, y + h // 2, FONT, text_color)
    return False


def draw_background(screen, width, height):
    screen.fill((255, 220, 235))

    for y in range(0, height, 80):
        pygame.draw.circle(screen, (255, 190, 215), (60, y + 30), 25)
        pygame.draw.circle(screen, (235, 210, 255), (width - 70, y + 50), 22)

    pygame.draw.rect(screen, (60, 55, 70), (80, 0, 340, height))

    pygame.draw.line(screen, WHITE, (80, 0), (80, height), 5)
    pygame.draw.line(screen, WHITE, (420, 0), (420, height), 5)

    for y in range(0, height, 80):
        pygame.draw.rect(screen, WHITE, (245, y, 10, 45), border_radius=5)