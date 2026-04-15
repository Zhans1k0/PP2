import pygame
import sys
from ball import Ball

def main():
    """Главная функция для запуска игры с движущимся мячом"""
    pygame.init()
    
    # Настройки окна
    WIDTH, HEIGHT = 800, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Движущийся мяч")
    
    # Создаем мяч в центре экрана
    ball = Ball(WIDTH//2, HEIGHT//2, 25, WIDTH, HEIGHT)
    
    # Частота кадров
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)
    
    # Главный игровой цикл
    running = True
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
        
        # Показываем позицию мяча
        pos_text = font.render(f"Позиция: ({ball.x}, {ball.y})", True, (0, 0, 0))
        screen.blit(pos_text, (10, 10))
        
        # Показываем границы экрана
        bounds_text = font.render(f"Границы: 0-{WIDTH}, 0-{HEIGHT}", True, (100, 100, 100))
        screen.blit(bounds_text, (10, 50))
        
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
        
        # Обновляем экран
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()