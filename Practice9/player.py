import pygame
import os

class MusicPlayer:
    """Класс музыкального плеера с управлением плейлистом"""
    
    def __init__(self, screen, width, height):
        self.screen = screen
        self.width = width
        self.height = height
        self.playlist = []
        self.current_track = 0
        self.is_playing = False
        
        # Шрифты
        self.font_large = pygame.font.Font(None, 48)
        self.font_medium = pygame.font.Font(None, 36)
        self.font_small = pygame.font.Font(None, 24)
        
        # Загружаем треки
        self.load_tracks()
    
    def load_tracks(self):
        """Загружает треки из папки music или создает демо-треки"""
        music_folder = "music"
        
        # Проверяем, есть ли папка с музыкой
        if os.path.exists(music_folder):
            # Загружаем реальные .wav файлы
            wav_files = [f for f in os.listdir(music_folder) if f.endswith('.wav')]
            if wav_files:
                for wav_file in wav_files:
                    try:
                        sound = pygame.mixer.Sound(os.path.join(music_folder, wav_file))
                        self.playlist.append({
                            'name': wav_file.replace('.wav', ''),
                            'sound': sound,
                            'duration': 0
                        })
                        print(f"Загружен трек: {wav_file}")
                    except:
                        print(f"Не удалось загрузить: {wav_file}")
        
        # Если нет треков, создаем демо-треки
        if not self.playlist:
            print("Реальные треки не найдены, создаю демо-треки...")
            self.create_demo_tracks()
    
    def create_beep(self, frequency, duration):
        """Создает простой звук заданной частоты"""
        sample_rate = 44100
        samples = int(sample_rate * duration)
        
        import numpy as np
        t = np.linspace(0, duration, samples)
        wave = np.sin(2 * np.pi * frequency * t)
        
        # Добавляем гармоники для лучшего звучания
        wave += 0.5 * np.sin(2 * np.pi * 2 * frequency * t)
        wave += 0.25 * np.sin(2 * np.pi * 3 * frequency * t)
        
        # Нормализуем
        wave = wave / np.max(np.abs(wave))
        
        # Конвертируем в формат pygame
        wave = (wave * 32767).astype(np.int16)
        stereo = np.zeros((samples, 2), dtype=np.int16)
        stereo[:, 0] = wave
        stereo[:, 1] = wave
        
        return pygame.sndarray.make_sound(stereo)
    
    def create_demo_tracks(self):
        """Создает демо-треки (разные ноты)"""
        demo_tracks = [
            ("Трек 1 - До мажор", 261.63, 3),
            ("Трек 2 - Ре мажор", 293.66, 3),
            ("Трек 3 - Ми мажор", 329.63, 3),
            ("Трек 4 - Фа мажор", 349.23, 3),
            ("Трек 5 - Соль мажор", 392.00, 3),
            ("Трек 6 - Ля мажор", 440.00, 3),
            ("Трек 7 - Си мажор", 493.88, 3)
        ]
        
        for name, freq, duration in demo_tracks:
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
        if self.is_playing and self.playlist:
            self.playlist[self.current_track]['sound'].stop()
            self.is_playing = False
    
    def next_track(self):
        """Переключить на следующий трек"""
        if self.playlist:
            self.stop()
            self.current_track = (self.current_track + 1) % len(self.playlist)
            self.play()
    
    def previous_track(self):
        """Переключить на предыдущий трек"""
        if self.playlist:
            self.stop()
            self.current_track = (self.current_track - 1) % len(self.playlist)
            self.play()
    
    def draw(self):
        """Отрисовка интерфейса плеера"""
        # Заголовок
        title = self.font_large.render("МУЗЫКАЛЬНЫЙ ПЛЕЕР", True, (0, 0, 255))
        title_rect = title.get_rect(center=(self.width//2, 50))
        self.screen.blit(title, title_rect)
        
        if self.playlist:
            # Текущий трек
            current = self.playlist[self.current_track]
            track_text = self.font_medium.render(
                f"Сейчас играет: {current['name']}", 
                True, (0, 0, 0)
            )
            self.screen.blit(track_text, (50, 150))
            
            # Статус
            status = "▶ ИГРАЕТ" if self.is_playing else "⏹ ОСТАНОВЛЕН"
            color = (0, 255, 0) if self.is_playing else (255, 0, 0)
            status_text = self.font_medium.render(status, True, color)
            self.screen.blit(status_text, (50, 200))
            
            # Номер трека
            track_num = self.font_small.render(
                f"Трек {self.current_track + 1} из {len(self.playlist)}", 
                True, (100, 100, 100)
            )
            self.screen.blit(track_num, (50, 250))
            
            # Список воспроизведения
            playlist_title = self.font_medium.render("Плейлист:", True, (0, 0, 0))
            self.screen.blit(playlist_title, (50, 320))
            
            y_offset = 370
            for i, track in enumerate(self.playlist):
                if i == self.current_track:
                    # Текущий трек - красный с указателем
                    prefix = "▶ " if self.is_playing else "⏸ "
                    color = (255, 0, 0)
                else:
                    prefix = "  "
                    color = (0, 0, 0)
                
                track_text = self.font_small.render(
                    f"{prefix}{i+1}. {track['name']}", 
                    True, color
                )
                self.screen.blit(track_text, (70, y_offset))
                y_offset += 30
                
                # Ограничиваем количество отображаемых треков
                if y_offset > self.height - 50:
                    break
        
        # Отображение управления
        controls = [
            "УПРАВЛЕНИЕ:",
            "",
            "P - Play (Воспроизвести)",
            "S - Stop (Остановить)",
            "N - Next (Следующий)",
            "B - Previous (Предыдущий)",
            "",
            "Q - Quit (Выйти)"
        ]
        
        for i, text in enumerate(controls):
            if text == "":
                continue
            color = (0, 0, 255) if text == "УПРАВЛЕНИЕ:" else (100, 100, 100)
            control = self.font_small.render(text, True, color)
            self.screen.blit(control, (self.width - 220, 50 + i * 25))