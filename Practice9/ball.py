import pygame

class Ball:
    """Класс мяча с движением и проверкой границ"""
    
    def __init__(self, x, y, radius, screen_width, screen_height):
        """
        Инициализация мяча
        
        Args:
            x: начальная X координата
            y: начальная Y координата
            radius: радиус мяча
            screen_width: ширина экрана
            screen_height: высота экрана
        """
        self.x = x
        self.y = y
        self.radius = radius
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.color = (255, 0, 0)  # Красный
        self.speed = 20  # Шаг движения в пикселях
        
        # Дополнительные цвета для эффектов
        self.highlight_color = (255, 100, 100)  # Светло-красный для блика
    
    def move_up(self):
        """
        Движение мяча вверх
        Returns: True если движение выполнено, False если достигнута граница
        """
        new_y = self.y - self.speed
        if new_y - self.radius >= 0:
            self.y = new_y
            return True
        return False
    
    def move_down(self):
        """
        Движение мяча вниз
        Returns: True если движение выполнено, False если достигнута граница
        """
        new_y = self.y + self.speed
        if new_y + self.radius <= self.screen_height:
            self.y = new_y
            return True
        return False
    
    def move_left(self):
        """
        Движение мяча влево
        Returns: True если движение выполнено, False если достигнута граница
        """
        new_x = self.x - self.speed
        if new_x - self.radius >= 0:
            self.x = new_x
            return True
        return False
    
    def move_right(self):
        """
        Движение мяча вправо
        Returns: True если движение выполнено, False если достигнута граница
        """
        new_x = self.x + self.speed
        if new_x + self.radius <= self.screen_width:
            self.x = new_x
            return True
        return False
    
    def draw(self, screen):
        """
        Рисование мяча на экране
        
        Args:
            screen: поверхность pygame для рисования
        """
        # Рисуем основной круг
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)
        
        # Добавляем 3D эффект (блик)
        highlight_x = self.x - self.radius // 3
        highlight_y = self.y - self.radius // 3
        highlight_radius = self.radius // 3
        pygame.draw.circle(screen, self.highlight_color, 
                          (highlight_x, highlight_y), highlight_radius)
        
        # Рисуем контур мяча (для лучшей видимости)
        pygame.draw.circle(screen, (200, 0, 0), (self.x, self.y), self.radius, 2)
    
    def get_position(self):
        """
        Получить текущую позицию мяча
        
        Returns: tuple (x, y)
        """
        return (self.x, self.y)
    
    def set_position(self, x, y):
        """
        Установить новую позицию мяча с проверкой границ
        
        Args:
            x: новая X координата
            y: новая Y координата
        
        Returns: True если позиция установлена, False если вне границ
        """
        # Проверяем, что мяч не выходит за границы
        if (self.radius <= x <= self.screen_width - self.radius and
            self.radius <= y <= self.screen_height - self.radius):
            self.x = x
            self.y = y
            return True
        return False
    
    def reset_position(self):
        """Сбросить позицию мяча в центр экрана"""
        self.x = self.screen_width // 2
        self.y = self.screen_height // 2
    
    def change_color(self, color):
        """
        Изменить цвет мяча
        
        Args:
            color: tuple (R, G, B)
        """
        self.color = color
    
    def change_speed(self, speed):
        """
        Изменить скорость движения мяча
        
        Args:
            speed: новая скорость в пикселях
        """
        if speed > 0:
            self.speed = speed