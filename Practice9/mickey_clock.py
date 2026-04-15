import pygame
import datetime
import sys
import math

pygame.init()

# Настройки окна
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Часы Микки Мауса")

def draw_mickey_hand(surface, angle, length, is_right=True):
    """Рисует перчатку Микки Мауса"""
    center_x = WIDTH // 2
    center_y = HEIGHT // 2
    
    # Конвертируем угол в радианы
    rad = math.radians(angle - 90)
    
    # Конец руки
    end_x = center_x + length * math.cos(rad)
    end_y = center_y + length * math.sin(rad)
    
    # Рисуем палку-руку (черную)
    pygame.draw.line(surface, (0, 0, 0), (center_x, center_y), (end_x, end_y), 12)
    
    # Рисуем перчатку (белый овал)
    glove_rect = pygame.Rect(0, 0, 40, 50)
    glove_rect.center = (int(end_x), int(end_y))
    pygame.draw.ellipse(surface, (255, 255, 255), glove_rect)
    pygame.draw.ellipse(surface, (0, 0, 0), glove_rect, 2)
    
    # Рисуем 3 пальца (как у Микки)
    finger_offsets = [-25, 0, 25] if is_right else [-25, 0, 25]
    for offset in finger_offsets:
        finger_rad = math.radians(angle + offset)
        finger_x = end_x + 20 * math.cos(finger_rad)
        finger_y = end_y + 20 * math.sin(finger_rad)
        
        finger_rect = pygame.Rect(0, 0, 20, 20)
        finger_rect.center = (int(finger_x), int(finger_y))
        pygame.draw.ellipse(surface, (255, 255, 255), finger_rect)
        pygame.draw.ellipse(surface, (0, 0, 0), finger_rect, 1)

def draw_mickey_head(surface):
    """Рисует симпатичную голову Микки Мауса"""
    center_x = WIDTH // 2
    center_y = HEIGHT // 2
    
    # Уши (большие черные круги)
    pygame.draw.circle(surface, (0, 0, 0), (center_x - 45, center_y - 45), 35)
    pygame.draw.circle(surface, (0, 0, 0), (center_x + 45, center_y - 45), 35)
    
    # Голова (черный круг)
    pygame.draw.circle(surface, (0, 0, 0), (center_x, center_y), 50)
    
    # Белая мордочка
    pygame.draw.ellipse(surface, (255, 255, 255), (center_x - 25, center_y - 10, 50, 40))
    
    # Глаза (белые с черными зрачками)
    pygame.draw.circle(surface, (255, 255, 255), (center_x - 20, center_y - 10), 10)
    pygame.draw.circle(surface, (255, 255, 255), (center_x + 20, center_y - 10), 10)
    pygame.draw.circle(surface, (0, 0, 0), (center_x - 20, center_y - 10), 5)
    pygame.draw.circle(surface, (0, 0, 0), (center_x + 20, center_y - 10), 5)
    
    # Блики в глазах (чтобы были живые)
    pygame.draw.circle(surface, (255, 255, 255), (center_x - 22, center_y - 12), 2)
    pygame.draw.circle(surface, (255, 255, 255), (center_x + 18, center_y - 12), 2)
    
    # Нос (черный овал)
    pygame.draw.ellipse(surface, (0, 0, 0), (center_x - 8, center_y - 2, 16, 12))
    
    # Улыбка (широкая и дружелюбная)
    pygame.draw.arc(surface, (0, 0, 0), 
                   (center_x - 25, center_y - 5, 50, 35), 
                   0, math.pi, 3)
    
    # Ямочки на щеках
    pygame.draw.circle(surface, (255, 200, 200), (center_x - 30, center_y + 5), 5)
    pygame.draw.circle(surface, (255, 200, 200), (center_x + 30, center_y + 5), 5)

def draw_clock_face(surface):
    """Рисует красивый циферблат"""
    center_x = WIDTH // 2
    center_y = HEIGHT // 2
    
    # Внешний круг циферблата
    pygame.draw.circle(surface, (255, 248, 220), (center_x, center_y), 280)
    pygame.draw.circle(surface, (139, 69, 19), (center_x, center_y), 280, 5)
    
    # Внутренний круг
    pygame.draw.circle(surface, (255, 255, 255), (center_x, center_y), 270)
    pygame.draw.circle(surface, (139, 69, 19), (center_x, center_y), 270, 2)
    
    # Цифры
    font = pygame.font.Font(None, 50)
    for i in range(1, 13):
        angle = math.radians(i * 30 - 90)
        x = center_x + 230 * math.cos(angle)
        y = center_y + 230 * math.sin(angle)
        number = font.render(str(i), True, (139, 69, 19))
        number_rect = number.get_rect(center=(x, y))
        surface.blit(number, number_rect)
    
    # Деления (минуты)
    for i in range(60):
        angle = math.radians(i * 6 - 90)
        if i % 5 == 0:
            # Часовые деления (жирные)
            start_x = center_x + 250 * math.cos(angle)
            start_y = center_y + 250 * math.sin(angle)
            end_x = center_x + 265 * math.cos(angle)
            end_y = center_y + 265 * math.sin(angle)
            pygame.draw.line(surface, (139, 69, 19), (start_x, start_y), (end_x, end_y), 4)
        else:
            # Минутные деления (тонкие)
            start_x = center_x + 255 * math.cos(angle)
            start_y = center_y + 255 * math.sin(angle)
            end_x = center_x + 262 * math.cos(angle)
            end_y = center_y + 262 * math.sin(angle)
            pygame.draw.line(surface, (139, 69, 19), (start_x, start_y), (end_x, end_y), 2)

# Главный игровой цикл
clock = pygame.time.Clock()
running = True

while running:
    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
    
    # Получаем текущее время
    now = datetime.datetime.now()
    minutes = now.minute
    seconds = now.second
    
    # Рассчитываем углы
    # Правая рука = минуты (6 градусов на минуту)
    right_angle = minutes * 6
    # Левая рука = секунды (6 градусов на секунду)  
    left_angle = seconds * 6
    
    # Отрисовка
    screen.fill((255, 255, 255))  # Белый фон
    
    # Рисуем циферблат
    draw_clock_face(screen)
    
    # Рисуем руки Микки Мауса
    # Правая рука (минуты) - длиннее
    draw_mickey_hand(screen, right_angle, 200, True)
    # Левая рука (секунды) - короче
    draw_mickey_hand(screen, left_angle, 170, False)
    
    # Рисуем голову Микки в центре
    draw_mickey_head(screen)
    
    # Показываем цифровое время
    font = pygame.font.Font(None, 48)
    time_text = font.render(f"{now.hour:02d}:{minutes:02d}:{seconds:02d}", 
                           True, (139, 69, 19))
    text_rect = time_text.get_rect(center=(WIDTH//2, HEIGHT - 50))
    screen.blit(time_text, text_rect)
    
    # Надпись "Mickey's Clock"
    title_font = pygame.font.Font(None, 36)
    title = title_font.render("Mickey's Clock", True, (139, 69, 19))
    title_rect = title.get_rect(center=(WIDTH//2, 30))
    screen.blit(title, title_rect)
    
    # Обновляем экран
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()