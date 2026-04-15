import pygame
import datetime
import math

class MickeyClock:
    """Класс для управления часами Микки Мауса"""
    
    def __init__(self, screen, width, height):
        self.screen = screen
        self.width = width
        self.height = height
        self.center_x = width // 2
        self.center_y = height // 2
        
        # Загружаем изображения рук (если есть)
        self.right_hand_img = None
        self.left_hand_img = None
        self.load_images()
        
    def load_images(self):
        """Загружает изображения рук Микки, если они есть"""
        try:
            self.right_hand_img = pygame.image.load('images/right_hand.png')
            self.left_hand_img = pygame.image.load('images/left_hand.png')
            print("Изображения рук загружены")
        except:
            print("Изображения не найдены, использую встроенную отрисовку")
            self.right_hand_img = None
            self.left_hand_img = None
    
    def draw_mickey_hand(self, angle, length, is_right=True):
        """Рисует перчатку Микки Мауса"""
        # Конец руки
        rad = math.radians(angle - 90)
        end_x = self.center_x + length * math.cos(rad)
        end_y = self.center_y + length * math.sin(rad)
        
        # Рисуем палку-руку (черную)
        pygame.draw.line(self.screen, (0, 0, 0), 
                        (self.center_x, self.center_y), 
                        (end_x, end_y), 12)
        
        # Рисуем перчатку (белый овал)
        glove_rect = pygame.Rect(0, 0, 40, 50)
        glove_rect.center = (int(end_x), int(end_y))
        pygame.draw.ellipse(self.screen, (255, 255, 255), glove_rect)
        pygame.draw.ellipse(self.screen, (0, 0, 0), glove_rect, 2)
        
        # Рисуем 3 пальца
        finger_offsets = [-25, 0, 25]
        for offset in finger_offsets:
            finger_rad = math.radians(angle + offset)
            finger_x = end_x + 20 * math.cos(finger_rad)
            finger_y = end_y + 20 * math.sin(finger_rad)
            
            finger_rect = pygame.Rect(0, 0, 20, 20)
            finger_rect.center = (int(finger_x), int(finger_y))
            pygame.draw.ellipse(self.screen, (255, 255, 255), finger_rect)
            pygame.draw.ellipse(self.screen, (0, 0, 0), finger_rect, 1)
    
    def draw_mickey_head(self):
        """Рисует голову Микки Мауса"""
        # Уши
        pygame.draw.circle(self.screen, (0, 0, 0), 
                          (self.center_x - 45, self.center_y - 45), 35)
        pygame.draw.circle(self.screen, (0, 0, 0), 
                          (self.center_x + 45, self.center_y - 45), 35)
        
        # Голова
        pygame.draw.circle(self.screen, (0, 0, 0), 
                          (self.center_x, self.center_y), 50)
        
        # Белая мордочка
        pygame.draw.ellipse(self.screen, (255, 255, 255), 
                           (self.center_x - 25, self.center_y - 10, 50, 40))
        
        # Глаза
        pygame.draw.circle(self.screen, (255, 255, 255), 
                          (self.center_x - 20, self.center_y - 10), 10)
        pygame.draw.circle(self.screen, (255, 255, 255), 
                          (self.center_x + 20, self.center_y - 10), 10)
        pygame.draw.circle(self.screen, (0, 0, 0), 
                          (self.center_x - 20, self.center_y - 10), 5)
        pygame.draw.circle(self.screen, (0, 0, 0), 
                          (self.center_x + 20, self.center_y - 10), 5)
        
        # Блики в глазах
        pygame.draw.circle(self.screen, (255, 255, 255), 
                          (self.center_x - 22, self.center_y - 12), 2)
        pygame.draw.circle(self.screen, (255, 255, 255), 
                          (self.center_x + 18, self.center_y - 12), 2)
        
        # Нос
        pygame.draw.ellipse(self.screen, (0, 0, 0), 
                           (self.center_x - 8, self.center_y - 2, 16, 12))
        
        # Улыбка
        pygame.draw.arc(self.screen, (0, 0, 0), 
                       (self.center_x - 25, self.center_y - 5, 50, 35), 
                       0, math.pi, 3)
        
        # Ямочки на щеках
        pygame.draw.circle(self.screen, (255, 200, 200), 
                          (self.center_x - 30, self.center_y + 5), 5)
        pygame.draw.circle(self.screen, (255, 200, 200), 
                          (self.center_x + 30, self.center_y + 5), 5)
    
    def draw_clock_face(self):
        """Рисует циферблат часов"""
        # Внешний круг
        pygame.draw.circle(self.screen, (255, 248, 220), 
                          (self.center_x, self.center_y), 280)
        pygame.draw.circle(self.screen, (139, 69, 19), 
                          (self.center_x, self.center_y), 280, 5)
        
        # Внутренний круг
        pygame.draw.circle(self.screen, (255, 255, 255), 
                          (self.center_x, self.center_y), 270)
        pygame.draw.circle(self.screen, (139, 69, 19), 
                          (self.center_x, self.center_y), 270, 2)
        
        # Цифры
        font = pygame.font.Font(None, 50)
        for i in range(1, 13):
            angle = math.radians(i * 30 - 90)
            x = self.center_x + 230 * math.cos(angle)
            y = self.center_y + 230 * math.sin(angle)
            number = font.render(str(i), True, (139, 69, 19))
            number_rect = number.get_rect(center=(x, y))
            self.screen.blit(number, number_rect)
        
        # Деления
        for i in range(60):
            angle = math.radians(i * 6 - 90)
            if i % 5 == 0:
                start_x = self.center_x + 250 * math.cos(angle)
                start_y = self.center_y + 250 * math.sin(angle)
                end_x = self.center_x + 265 * math.cos(angle)
                end_y = self.center_y + 265 * math.sin(angle)
                pygame.draw.line(self.screen, (139, 69, 19), 
                                (start_x, start_y), (end_x, end_y), 4)
            else:
                start_x = self.center_x + 255 * math.cos(angle)
                start_y = self.center_y + 255 * math.sin(angle)
                end_x = self.center_x + 262 * math.cos(angle)
                end_y = self.center_y + 262 * math.sin(angle)
                pygame.draw.line(self.screen, (139, 69, 19), 
                                (start_x, start_y), (end_x, end_y), 2)
    
    def update(self):
        """Обновляет состояние часов (углы поворота стрелок)"""
        now = datetime.datetime.now()
        self.minutes = now.minute
        self.seconds = now.second
        
        # Рассчитываем углы
        self.right_angle = self.minutes * 6    # Правая рука - минуты
        self.left_angle = self.seconds * 6      # Левая рука - секунды
    
    def draw(self):
        """Рисует все компоненты часов"""
        # Рисуем циферблат
        self.draw_clock_face()
        
        # Рисуем руки Микки (если есть изображения, используем их)
        if self.right_hand_img and self.left_hand_img:
            # Поворачиваем и рисуем изображения
            rotated_right = pygame.transform.rotate(self.right_hand_img, -self.right_angle + 90)
            rotated_left = pygame.transform.rotate(self.left_hand_img, -self.left_angle + 90)
            right_rect = rotated_right.get_rect(center=(self.center_x, self.center_y))
            left_rect = rotated_left.get_rect(center=(self.center_x, self.center_y))
            self.screen.blit(rotated_right, right_rect)
            self.screen.blit(rotated_left, left_rect)
        else:
            # Рисуем руки программно
            self.draw_mickey_hand(self.right_angle, 200, True)   # Правая рука (минуты)
            self.draw_mickey_hand(self.left_angle, 170, False)    # Левая рука (секунды)
        
        # Рисуем голову Микки
        self.draw_mickey_head()
        
        # Показываем цифровое время
        font = pygame.font.Font(None, 48)
        now = datetime.datetime.now()
        time_text = font.render(f"{now.hour:02d}:{self.minutes:02d}:{self.seconds:02d}", 
                               True, (139, 69, 19))
        text_rect = time_text.get_rect(center=(self.width//2, self.height - 50))
        self.screen.blit(time_text, text_rect)
        
        # Надпись "Mickey's Clock"
        title_font = pygame.font.Font(None, 36)
        title = title_font.render("Mickey's Clock", True, (139, 69, 19))
        title_rect = title.get_rect(center=(self.width//2, 30))
        self.screen.blit(title, title_rect)