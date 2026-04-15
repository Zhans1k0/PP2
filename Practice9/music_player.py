import pygame
import sys
import os

pygame.init()
pygame.mixer.init()

# Настройки
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Музыкальный плеер")

# Создаем плейлист (для демо создаем простые звуки)
class MusicPlayer:
    def __init__(self):
        self.playlist = []
        self.current_track = 0
        self.is_playing = False
        self.load_tracks()
    
    def create_beep(self, frequency, duration):
        """Создает простой звук заданной частоты"""
        sample_rate = 44100
        samples = int(sample_rate * duration)
        
        import numpy as np
        t = np.linspace(0, duration, samples)
        wave = np.sin(2 * np.pi * frequency * t)
        
        # Конвертируем в формат pygame
        wave = (wave * 32767).astype(np.int16)
        stereo = np.zeros((samples, 2), dtype=np.int16)
        stereo[:, 0] = wave
        stereo[:, 1] = wave
        
        return pygame.sndarray.make_sound(stereo)
    
    def load_tracks(self):
        """Загружает треки в плейлист"""
        tracks = [
            ("Трек 1 - До мажор", 261.63, 3),
            ("Трек 2 - Ре мажор", 293.66, 3),
            ("Трек 3 - Ми мажор", 329.63, 3),
            ("Трек 4 - Фа мажор", 349.23, 3),
            ("Трек 5 - Соль мажор", 392.00, 3)
        ]
        
        for name, freq, duration in tracks:
            sound = self.create_beep(freq, duration)
            self.playlist.append({
                'name': name,
                'sound': sound,
                'duration': duration
            })
    
    def play(self):
        """Воспроизвести текущий трек"""
        if self.playlist and not self.is_playing:
            self.playlist[self.current_track]['sound'].play()
            self.is_playing = True
    
    def stop(self):
        """Остановить воспроизведение"""
        if self.is_playing:
            self.playlist[self.current_track]['sound'].stop()
            self.is_playing = False
    
    def next_track(self):
        """Следующий трек"""
        self.stop()
        self.current_track = (self.current_track + 1) % len(self.playlist)
        self.play()
    
    def previous_track(self):
        """Предыдущий трек"""
        self.stop()
        self.current_track = (self.current_track - 1) % len(self.playlist)
        self.play()

# Создаем плеер
player = MusicPlayer()

# Клавиши управления
CONTROLS = {
    pygame.K_p: 'play',
    pygame.K_s: 'stop',
    pygame.K_n: 'next',
    pygame.K_b: 'previous',
    pygame.K_q: 'quit'
}

# Главный цикл
running = True
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

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
    
    # Отображение информации
    y = 50
    title = font.render("МУЗЫКАЛЬНЫЙ ПЛЕЕР", True, (0, 0, 255))
    screen.blit(title, (WIDTH//2 - 150, y))
    y += 50
    
    if player.playlist:
        current = player.playlist[player.current_track]
        track_text = font.render(f"Сейчас играет: {current['name']}", 
                                 True, (0, 0, 0))
        screen.blit(track_text, (50, y))
        y += 50
        
        status = "ИГРАЕТ" if player.is_playing else "ОСТАНОВЛЕН"
        color = (0, 255, 0) if player.is_playing else (255, 0, 0)
        status_text = font.render(f"Статус: {status}", True, color)
        screen.blit(status_text, (50, y))
        y += 100
    
    # Отображение управления
    controls_text = [
        "УПРАВЛЕНИЕ:",
        "P - Play (Воспроизвести)",
        "S - Stop (Остановить)",
        "N - Next (Следующий)",
        "B - Previous (Предыдущий)",
        "Q - Quit (Выйти)"
    ]
    
    for i, text in enumerate(controls_text):
        control = font.render(text, True, (100, 100, 100))
        screen.blit(control, (WIDTH - 250, 50 + i * 30))
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()