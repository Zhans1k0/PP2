import pygame
from collections import deque


def draw_pencil(surface, color, start, end, size):
    pygame.draw.line(surface, color, start, end, size)


def draw_line(surface, color, start, end, size):
    pygame.draw.line(surface, color, start, end, size)


def draw_rect(surface, color, start, end, size):
    x1, y1 = start
    x2, y2 = end
    rect = pygame.Rect(min(x1, x2), min(y1, y2), abs(x2 - x1), abs(y2 - y1))
    pygame.draw.rect(surface, color, rect, size)


def draw_circle(surface, color, start, end, size):
    x1, y1 = start
    x2, y2 = end
    radius = int(((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5)
    pygame.draw.circle(surface, color, start, radius, size)


def draw_eraser(surface, start, end, size):
    pygame.draw.line(surface, (255, 255, 255), start, end, size)


def flood_fill(surface, start, fill_color):
    x, y = start

    if x < 0 or y < 0 or x >= surface.get_width() or y >= surface.get_height():
        return

    target_color = surface.get_at((x, y))

    if target_color == fill_color:
        return

    queue = deque()
    queue.append((x, y))

    while queue:
        px, py = queue.popleft()

        if px < 0 or py < 0 or px >= surface.get_width() or py >= surface.get_height():
            continue

        if surface.get_at((px, py)) != target_color:
            continue

        surface.set_at((px, py), fill_color)

        queue.append((px + 1, py))
        queue.append((px - 1, py))
        queue.append((px, py + 1))
        queue.append((px, py - 1))