import pygame
import sys
from player import MusicPlayer

def main():
    """Главная функция для запуска музыкального плеера"""
    pygame.init()
    pygame.mixer.init()
    
    # Настройки окна
    WIDTH, HEIGHT = 800, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Музыкальный плеер")
    
    # Создаем плеер
    player = MusicPlayer(screen, WIDTH, HEIGHT)
    
    # Главный цикл
    clock = pygame.time.Clock()
    running = True
    
    while running:
        screen.fill((255, 255, 255))
        
        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    player.play()
                elif event.key == pygame.K_s:
                    player.stop()
                elif event.key == pygame.K_n:
                    player.next_track()
                elif event.key == pygame.K_b:
                    player.previous_track()
                elif event.key == pygame.K_q:
                    running = False
        
        # Отрисовка интерфейса
        player.draw()
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()