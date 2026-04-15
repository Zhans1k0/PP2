import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Движущийся мяч")

class Ball:
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = (255, 0, 0)  # Красный
        self.speed = 20  # Шаг движения
    
    def move_up(self):
        """Движение вверх с проверкой границы"""
        if self.y - self.speed - self.radius >= 0:
            self.y -= self.speed
            return True
        return False
    
    def move_down(self):
        """Движение вниз с проверкой границы"""
        if self.y + self.speed + self.radius <= HEIGHT:
            self.y += self.speed
            return True
        return False
    
    def move_left(self):
        """Движение влево с проверкой границы"""
        if self.x - self.speed - self.radius >= 0:
            self.x -= self.speed
            return True
        return False
    
    def move_right(self):
        """Движение вправо с проверкой границы"""
        if self.x + self.speed + self.radius <= WIDTH:
            self.x += self.speed
            return True
        return False
    
    def draw(self, screen):
        """Рисование мяча"""
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)
        # Добавляем блик для красоты
        pygame.draw.circle(screen, (255, 100, 100), 
                          (self.x - 8, self.y - 8), 8)

# Создаем мяч в центре экрана
ball = Ball(WIDTH//2, HEIGHT//2, 25)

# Главный цикл
running = True
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

while running:
    screen.fill((255, 255, 255))  # Белый фон
    
    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                ball.move_up()
            elif event.key == pygame.K_DOWN:
                ball.move_down()
            elif event.key == pygame.K_LEFT:
                ball.move_left()
            elif event.key == pygame.K_RIGHT:
                ball.move_right()
            elif event.key == pygame.K_ESCAPE:
                running = False
    
    # Рисуем мяч
    ball.draw(screen)
    
    # Показываем позицию
    pos_text = font.render(f"Позиция: ({ball.x}, {ball.y})", True, (0, 0, 0))
    screen.blit(pos_text, (10, 10))
    
    # Показываем управление
    controls = [
        "Управление:",
        "↑ - Вверх",
        "↓ - Вниз",
        "← - Влево",
        "→ - Вправо",
        "ESC - Выход"
    ]
    
    y = HEIGHT - 150
    for text in controls:
        control_text = font.render(text, True, (100, 100, 100))
        screen.blit(control_text, (10, y))
        y += 30
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()