import pygame
import sys
from clock import MickeyClock

def main():
    """Главная функция для запуска часов Микки Мауса"""
    pygame.init()
    
    # Настройки окна
    WIDTH, HEIGHT = 800, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Часы Микки Мауса")
    
    # Создаем экземпляр часов
    mickey_clock = MickeyClock(screen, WIDTH, HEIGHT)
    
    # Частота кадров
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
        
        # Очищаем экран
        screen.fill((255, 255, 255))
        
        # Обновляем и рисуем часы
        mickey_clock.update()
        mickey_clock.draw()
        
        # Обновляем дисплей
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()