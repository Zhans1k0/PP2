import pygame
import random
import json
import os

from db import save_score, get_top_10, get_personal_best


class SnakeGame:
    def __init__(self):
        pygame.init()

        self.WIDTH = 800
        self.HEIGHT = 600
        self.CELL = 20

        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("TSIS4 Snake Game")

        self.clock = pygame.time.Clock()

        self.font = pygame.font.SysFont("arial", 26)
        self.small_font = pygame.font.SysFont("arial", 20)
        self.big_font = pygame.font.SysFont("arial", 46)

        self.BLACK = (18, 18, 24)
        self.WHITE = (245, 245, 245)
        self.GRAY = (120, 120, 120)
        self.DARK = (38, 38, 48)
        self.GREEN = (80, 220, 120)
        self.RED = (230, 70, 70)
        self.DARK_RED = (120, 0, 0)
        self.BLUE = (80, 150, 255)
        self.YELLOW = (240, 220, 80)
        self.PURPLE = (180, 100, 255)
        self.PINK = (255, 160, 200)

        self.username = ""
        self.settings = self.load_settings()

    def load_settings(self):
        if not os.path.exists("settings.json"):
            data = {
                "snake_color": [80, 220, 120],
                "grid": True,
                "sound": True
            }
            self.save_settings(data)
            return data

        with open("settings.json", "r") as file:
            return json.load(file)

    def save_settings(self, data):
        with open("settings.json", "w") as file:
            json.dump(data, file, indent=4)

    def draw_text(self, text, x, y, color=None, font=None):
        if color is None:
            color = self.WHITE
        if font is None:
            font = self.font

        img = font.render(str(text), True, color)
        self.screen.blit(img, (x, y))

    def draw_button(self, text, rect, mouse_pos):
        color = self.PINK if rect.collidepoint(mouse_pos) else self.DARK
        pygame.draw.rect(self.screen, color, rect, border_radius=12)
        pygame.draw.rect(self.screen, self.WHITE, rect, 2, border_radius=12)

        img = self.font.render(text, True, self.WHITE)
        img_rect = img.get_rect(center=rect.center)
        self.screen.blit(img, img_rect)

    def draw_grid(self):
        if not self.settings.get("grid", True):
            return

        for x in range(0, self.WIDTH, self.CELL):
            pygame.draw.line(self.screen, (35, 35, 45), (x, 0), (x, self.HEIGHT))
        for y in range(0, self.HEIGHT, self.CELL):
            pygame.draw.line(self.screen, (35, 35, 45), (0, y), (self.WIDTH, y))

    def get_random_position(self, snake, obstacles, extra=None):
        if extra is None:
            extra = []

        while True:
            x = random.randrange(0, self.WIDTH, self.CELL)
            y = random.randrange(0, self.HEIGHT, self.CELL)
            pos = [x, y]

            if pos not in snake and pos not in obstacles and pos not in extra:
                return pos

    def generate_obstacles(self, level, snake):
        obstacles = []

        if level < 3:
            return obstacles

        count = min(5 + level * 2, 35)
        head = snake[0]

        while len(obstacles) < count:
            pos = self.get_random_position(snake, obstacles)

            distance = abs(pos[0] - head[0]) + abs(pos[1] - head[1])

            if distance > self.CELL * 4:
                obstacles.append(pos)

        return obstacles

    def username_screen(self):
        username = ""

        while True:
            self.screen.fill(self.BLACK)

            self.draw_text("Enter username", 250, 150, self.PINK, self.big_font)

            input_rect = pygame.Rect(250, 250, 300, 55)
            pygame.draw.rect(self.screen, self.DARK, input_rect, border_radius=12)
            pygame.draw.rect(self.screen, self.WHITE, input_rect, 2, border_radius=12)

            self.draw_text(username, 265, 260, self.WHITE)
            self.draw_text("Press ENTER to continue", 270, 340, self.GRAY, self.small_font)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN and username.strip():
                        self.username = username.strip()
                        return

                    elif event.key == pygame.K_BACKSPACE:
                        username = username[:-1]

                    else:
                        if len(username) < 15 and event.unicode.isprintable():
                            username += event.unicode

            pygame.display.update()
            self.clock.tick(30)

    def main_menu(self):
        while True:
            self.screen.fill(self.BLACK)
            mouse_pos = pygame.mouse.get_pos()

            self.draw_text("SNAKE GAME", 260, 90, self.PINK, self.big_font)
            self.draw_text(f"Player: {self.username}", 320, 155, self.WHITE, self.small_font)

            play_btn = pygame.Rect(300, 220, 220, 50)
            leaderboard_btn = pygame.Rect(300, 290, 220, 50)
            settings_btn = pygame.Rect(300, 360, 220, 50)
            quit_btn = pygame.Rect(300, 430, 220, 50)

            self.draw_button("Play", play_btn, mouse_pos)
            self.draw_button("Leaderboard", leaderboard_btn, mouse_pos)
            self.draw_button("Settings", settings_btn, mouse_pos)
            self.draw_button("Quit", quit_btn, mouse_pos)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if play_btn.collidepoint(mouse_pos):
                        self.play_game()
                    elif leaderboard_btn.collidepoint(mouse_pos):
                        self.leaderboard_screen()
                    elif settings_btn.collidepoint(mouse_pos):
                        self.settings_screen()
                    elif quit_btn.collidepoint(mouse_pos):
                        pygame.quit()
                        exit()

            pygame.display.update()
            self.clock.tick(30)

    def leaderboard_screen(self):
        while True:
            self.screen.fill(self.BLACK)
            mouse_pos = pygame.mouse.get_pos()

            self.draw_text("Leaderboard TOP 10", 210, 50, self.PINK, self.big_font)

            try:
                data = get_top_10()
            except Exception:
                data = []
                self.draw_text("Database error. Check config.py", 230, 150, self.RED, self.small_font)

            y = 130
            self.draw_text("Rank   Username        Score    Level    Date", 80, y, self.YELLOW, self.small_font)
            y += 35

            for i, row in enumerate(data, start=1):
                username, score, level, played_at = row
                date_text = played_at.strftime("%Y-%m-%d")
                line = f"{i:<5}  {username:<14}  {score:<7}  {level:<7}  {date_text}"
                self.draw_text(line, 80, y, self.WHITE, self.small_font)
                y += 30

            back_btn = pygame.Rect(300, 520, 220, 45)
            self.draw_button("Back", back_btn, mouse_pos)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if back_btn.collidepoint(mouse_pos):
                        return

            pygame.display.update()
            self.clock.tick(30)

    def settings_screen(self):
        colors = [
            [80, 220, 120],
            [255, 150, 200],
            [90, 170, 255],
            [240, 220, 80],
            [180, 100, 255]
        ]

        while True:
            self.screen.fill(self.BLACK)
            mouse_pos = pygame.mouse.get_pos()

            self.draw_text("Settings", 300, 80, self.PINK, self.big_font)

            grid_btn = pygame.Rect(260, 190, 280, 50)
            sound_btn = pygame.Rect(260, 260, 280, 50)
            color_btn = pygame.Rect(260, 330, 280, 50)
            back_btn = pygame.Rect(260, 450, 280, 50)

            self.draw_button(
                f"Grid: {'ON' if self.settings['grid'] else 'OFF'}",
                grid_btn,
                mouse_pos
            )
            self.draw_button(
                f"Sound: {'ON' if self.settings['sound'] else 'OFF'}",
                sound_btn,
                mouse_pos
            )
            self.draw_button("Change Snake Color", color_btn, mouse_pos)
            self.draw_button("Save and Back", back_btn, mouse_pos)

            pygame.draw.rect(
                self.screen,
                self.settings["snake_color"],
                (560, 337, 40, 30),
                border_radius=8
            )

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if grid_btn.collidepoint(mouse_pos):
                        self.settings["grid"] = not self.settings["grid"]

                    elif sound_btn.collidepoint(mouse_pos):
                        self.settings["sound"] = not self.settings["sound"]

                    elif color_btn.collidepoint(mouse_pos):
                        current = self.settings["snake_color"]
                        index = colors.index(current) if current in colors else 0
                        self.settings["snake_color"] = colors[(index + 1) % len(colors)]

                    elif back_btn.collidepoint(mouse_pos):
                        self.save_settings(self.settings)
                        return

            pygame.display.update()
            self.clock.tick(30)

    def play_game(self):
        snake = [[self.WIDTH // 2, self.HEIGHT // 2]]
        direction = [self.CELL, 0]
        next_direction = direction

        score = 0
        level = 1
        speed = 10

        try:
            personal_best = get_personal_best(self.username)
        except Exception:
            personal_best = 0

        obstacles = self.generate_obstacles(level, snake)

        normal_food = self.get_random_position(snake, obstacles)
        poison_food = self.get_random_position(snake, obstacles, [normal_food])

        power_up = None
        power_type = None
        power_spawn_time = 0
        last_power_spawn = pygame.time.get_ticks()

        active_power = None
        active_power_end = 0
        shield = False

        while True:
            now = pygame.time.get_ticks()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP and direction != [0, self.CELL]:
                        next_direction = [0, -self.CELL]
                    elif event.key == pygame.K_DOWN and direction != [0, -self.CELL]:
                        next_direction = [0, self.CELL]
                    elif event.key == pygame.K_LEFT and direction != [self.CELL, 0]:
                        next_direction = [-self.CELL, 0]
                    elif event.key == pygame.K_RIGHT and direction != [-self.CELL, 0]:
                        next_direction = [self.CELL, 0]

            direction = next_direction
            head = [snake[0][0] + direction[0], snake[0][1] + direction[1]]

            collision = (
                head[0] < 0 or
                head[0] >= self.WIDTH or
                head[1] < 0 or
                head[1] >= self.HEIGHT or
                head in snake or
                head in obstacles
            )

            if collision:
                if shield:
                    shield = False
                    head = snake[0][:]
                else:
                    try:
                        save_score(self.username, score, level)
                    except Exception:
                        pass
                    self.game_over_screen(score, level)
                    return

            snake.insert(0, head)

            ate = False

            if head == normal_food:
                score += 10
                ate = True
                normal_food = self.get_random_position(
                    snake,
                    obstacles,
                    [poison_food]
                )

                if score % 50 == 0:
                    level += 1
                    speed += 1
                    obstacles = self.generate_obstacles(level, snake)

            if head == poison_food:
                if len(snake) <= 2:
                    try:
                        save_score(self.username, score, level)
                    except Exception:
                        pass
                    self.game_over_screen(score, level)
                    return

                snake.pop()
                snake.pop()
                poison_food = self.get_random_position(
                    snake,
                    obstacles,
                    [normal_food]
                )

            if power_up and head == power_up:
                if power_type == "speed":
                    active_power = "speed"
                    active_power_end = now + 5000

                elif power_type == "slow":
                    active_power = "slow"
                    active_power_end = now + 5000

                elif power_type == "shield":
                    shield = True

                power_up = None
                power_type = None

            if not ate:
                snake.pop()

            if active_power and now > active_power_end:
                active_power = None

            if power_up is None and now - last_power_spawn > 7000:
                power_up = self.get_random_position(
                    snake,
                    obstacles,
                    [normal_food, poison_food]
                )
                power_type = random.choice(["speed", "slow", "shield"])
                power_spawn_time = now
                last_power_spawn = now

            if power_up and now - power_spawn_time > 8000:
                power_up = None
                power_type = None

            current_speed = speed

            if active_power == "speed":
                current_speed = speed + 5
            elif active_power == "slow":
                current_speed = max(5, speed - 4)

            self.screen.fill(self.BLACK)
            self.draw_grid()

            pygame.draw.rect(self.screen, self.RED, (*normal_food, self.CELL, self.CELL), border_radius=5)
            pygame.draw.rect(self.screen, self.DARK_RED, (*poison_food, self.CELL, self.CELL), border_radius=5)

            if power_up:
                if power_type == "speed":
                    color = self.BLUE
                elif power_type == "slow":
                    color = self.YELLOW
                else:
                    color = self.PURPLE

                pygame.draw.rect(self.screen, color, (*power_up, self.CELL, self.CELL), border_radius=8)

            for obstacle in obstacles:
                pygame.draw.rect(self.screen, self.GRAY, (*obstacle, self.CELL, self.CELL), border_radius=3)

            for part in snake:
                pygame.draw.rect(
                    self.screen,
                    self.settings["snake_color"],
                    (*part, self.CELL, self.CELL),
                    border_radius=6
                )

            self.draw_text(f"Score: {score}", 20, 15, self.WHITE, self.small_font)
            self.draw_text(f"Level: {level}", 20, 40, self.WHITE, self.small_font)
            self.draw_text(f"Best: {personal_best}", 20, 65, self.YELLOW, self.small_font)

            if active_power:
                self.draw_text(f"Power: {active_power}", 610, 15, self.YELLOW, self.small_font)

            if shield:
                self.draw_text("Shield: ON", 610, 40, self.PURPLE, self.small_font)

            pygame.display.update()
            self.clock.tick(current_speed)

    def game_over_screen(self, score, level):
        try:
            best = get_personal_best(self.username)
        except Exception:
            best = score

        while True:
            self.screen.fill(self.BLACK)
            mouse_pos = pygame.mouse.get_pos()

            self.draw_text("GAME OVER", 260, 100, self.RED, self.big_font)
            self.draw_text(f"Score: {score}", 320, 210, self.WHITE)
            self.draw_text(f"Level: {level}", 320, 250, self.WHITE)
            self.draw_text(f"Personal Best: {best}", 320, 290, self.YELLOW)

            retry_btn = pygame.Rect(300, 380, 220, 50)
            menu_btn = pygame.Rect(300, 450, 220, 50)

            self.draw_button("Retry", retry_btn, mouse_pos)
            self.draw_button("Main Menu", menu_btn, mouse_pos)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if retry_btn.collidepoint(mouse_pos):
                        self.play_game()
                        return

                    elif menu_btn.collidepoint(mouse_pos):
                        return

            pygame.display.update()
            self.clock.tick(30)

    def run(self):
        self.username_screen()
        self.main_menu()