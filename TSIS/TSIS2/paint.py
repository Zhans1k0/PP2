import pygame
from datetime import datetime
import tools

pygame.init()

WIDTH = 1000
HEIGHT = 700
TOOLBAR = 90

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TSIS2 Paint")

canvas = pygame.Surface((WIDTH, HEIGHT - TOOLBAR))
canvas.fill((255, 255, 255))

font = pygame.font.SysFont("Arial", 22)
text_font = pygame.font.SysFont("Arial", 30)

tool = "pencil"
color = (0, 0, 0)
size = 5

drawing = False
start_pos = None
last_pos = None

text_mode = False
text_pos = None
text_value = ""

colors = [
    (0, 0, 0),
    (255, 0, 0),
    (0, 180, 0),
    (0, 0, 255),
    (255, 255, 0),
    (255, 120, 0),
    (150, 0, 200),
    (255, 255, 255)
]


def get_canvas_pos(pos):
    return pos[0], pos[1] - TOOLBAR


def save_canvas():
    filename = datetime.now().strftime("painting_%Y%m%d_%H%M%S.png")
    pygame.image.save(canvas, filename)
    print("Saved:", filename)


def draw_toolbar():
    pygame.draw.rect(screen, (220, 220, 220), (0, 0, WIDTH, TOOLBAR))

    title = font.render(
        "P Pencil | L Line | R Rect | C Circle | E Eraser | F Fill | T Text | 1/2/3 Size | Ctrl+S Save",
        True,
        (0, 0, 0)
    )
    screen.blit(title, (10, 10))

    status = font.render(f"Current tool: {tool} | Brush size: {size}", True, (0, 0, 0))
    screen.blit(status, (10, 55))

    x = 650
    y = 50

    for c in colors:
        pygame.draw.rect(screen, c, (x, y, 30, 30))
        pygame.draw.rect(screen, (0, 0, 0), (x, y, 30, 30), 2)

        if c == color:
            pygame.draw.rect(screen, (255, 0, 0), (x - 3, y - 3, 36, 36), 3)

        x += 40


running = True

while running:
    screen.fill((255, 255, 255))
    screen.blit(canvas, (0, TOOLBAR))
    draw_toolbar()

    mouse_pos = pygame.mouse.get_pos()

    if drawing and start_pos is not None:
        preview = canvas.copy()
        end_pos = get_canvas_pos(mouse_pos)

        if tool == "line":
            tools.draw_line(preview, color, start_pos, end_pos, size)

        elif tool == "rect":
            tools.draw_rect(preview, color, start_pos, end_pos, size)

        elif tool == "circle":
            tools.draw_circle(preview, color, start_pos, end_pos, size)

        screen.blit(preview, (0, TOOLBAR))

    if text_mode and text_pos is not None:
        preview_text = text_font.render(text_value + "|", True, color)
        screen.blit(preview_text, (text_pos[0], text_pos[1] + TOOLBAR))

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if text_mode:
                if event.key == pygame.K_RETURN:
                    final_text = text_font.render(text_value, True, color)
                    canvas.blit(final_text, text_pos)

                    text_mode = False
                    text_pos = None
                    text_value = ""

                elif event.key == pygame.K_BACKSPACE:
                    text_value = text_value[:-1]

                elif event.key == pygame.K_ESCAPE:
                    text_mode = False
                    text_pos = None
                    text_value = ""

                else:
                    text_value += event.unicode

            else:
                if event.key == pygame.K_p:
                    tool = "pencil"

                elif event.key == pygame.K_l:
                    tool = "line"

                elif event.key == pygame.K_r:
                    tool = "rect"

                elif event.key == pygame.K_c:
                    tool = "circle"

                elif event.key == pygame.K_e:
                    tool = "eraser"

                elif event.key == pygame.K_f:
                    tool = "fill"

                elif event.key == pygame.K_t:
                    tool = "text"

                elif event.key == pygame.K_1:
                    size = 2

                elif event.key == pygame.K_2:
                    size = 5

                elif event.key == pygame.K_3:
                    size = 10

                elif event.key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_CTRL:
                    save_canvas()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if event.pos[1] < TOOLBAR:
                    x, y = event.pos

                    if 650 <= x <= 650 + len(colors) * 40 and 50 <= y <= 80:
                        index = (x - 650) // 40
                        if 0 <= index < len(colors):
                            color = colors[index]

                    continue

                pos = get_canvas_pos(event.pos)

                if tool == "fill":
                    tools.flood_fill(canvas, pos, color)

                elif tool == "text":
                    text_mode = True
                    text_pos = pos
                    text_value = ""

                else:
                    drawing = True
                    start_pos = pos
                    last_pos = pos

        elif event.type == pygame.MOUSEMOTION:
            if drawing:
                pos = get_canvas_pos(event.pos)

                if tool == "pencil":
                    tools.draw_pencil(canvas, color, last_pos, pos, size)
                    last_pos = pos

                elif tool == "eraser":
                    tools.draw_eraser(canvas, last_pos, pos, size)
                    last_pos = pos

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and drawing:
                pos = get_canvas_pos(event.pos)

                if tool == "line":
                    tools.draw_line(canvas, color, start_pos, pos, size)

                elif tool == "rect":
                    tools.draw_rect(canvas, color, start_pos, pos, size)

                elif tool == "circle":
                    tools.draw_circle(canvas, color, start_pos, pos, size)

                drawing = False
                start_pos = None
                last_pos = None

pygame.quit()