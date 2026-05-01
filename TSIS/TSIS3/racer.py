import pygame
import random
import time

from ui import draw_background, draw_text_left, draw_text
from persistence import save_score

WIDTH, HEIGHT = 500, 700
LANES = [145, 245, 345]

WHITE = (255, 255, 255)
BLACK = (20, 20, 20)
PINK = (255, 120, 180)
RED = (230, 60, 80)
BLUE = (70, 130, 255)
GREEN = (70, 220, 120)
YELLOW = (255, 220, 70)
PURPLE = (170, 90, 230)
ORANGE = (250, 150, 70)


def get_color(name):
    colors = {
        "pink": PINK,
        "blue": BLUE,
        "green": GREEN,
        "purple": PURPLE
    }
    return colors.get(name, PINK)


class Player:
    def __init__(self, color):
        self.w = 46
        self.h = 72
        self.x = LANES[1] - self.w // 2
        self.y = 580
        self.speed = 6
        self.color = color
        self.shield = False

    def rect(self):
        return pygame.Rect(self.x, self.y, self.w, self.h)

    def move(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and self.x > 90:
            self.x -= self.speed

        if keys[pygame.K_RIGHT] and self.x + self.w < 410:
            self.x += self.speed

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect(), border_radius=12)
        pygame.draw.rect(screen, WHITE, (self.x + 10, self.y + 10, 26, 16), border_radius=5)
        pygame.draw.circle(screen, BLACK, (self.x + 8, self.y + 58), 7)
        pygame.draw.circle(screen, BLACK, (self.x + 38, self.y + 58), 7)

        if self.shield:
            pygame.draw.circle(screen, YELLOW, self.rect().center, 48, 4)


class EnemyCar:
    def __init__(self, speed):
        self.w = 46
        self.h = 72
        self.x = random.choice(LANES) - self.w // 2
        self.y = -160
        self.speed = speed
        self.color = random.choice([RED, PURPLE, ORANGE])

    def rect(self):
        return pygame.Rect(self.x, self.y, self.w, self.h)

    def update(self):
        self.y += self.speed

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect(), border_radius=12)
        pygame.draw.rect(screen, WHITE, (self.x + 10, self.y + 10, 26, 16), border_radius=5)
        pygame.draw.circle(screen, BLACK, (self.x + 8, self.y + 58), 7)
        pygame.draw.circle(screen, BLACK, (self.x + 38, self.y + 58), 7)


class Obstacle:
    def __init__(self, speed):
        self.w = 52
        self.h = 38
        self.x = random.choice(LANES) - self.w // 2
        self.y = -120
        self.speed = speed
        self.kind = random.choice(["oil", "cone", "heart_block"])

    def rect(self):
        return pygame.Rect(self.x, self.y, self.w, self.h)

    def update(self):
        self.y += self.speed

    def draw(self, screen):
        if self.kind == "oil":
            pygame.draw.ellipse(screen, BLACK, self.rect())
            draw_text(screen, "oil", self.x + 26, self.y + 19, color=WHITE)

        elif self.kind == "cone":
            pygame.draw.polygon(
                screen,
                ORANGE,
                [(self.x + 26, self.y), (self.x, self.y + 38), (self.x + 52, self.y + 38)]
            )
            draw_text(screen, "!", self.x + 26, self.y + 25, color=BLACK)

        else:
            pygame.draw.rect(screen, (255, 170, 210), self.rect(), border_radius=10)
            draw_text(screen, "X", self.x + 26, self.y + 19, color=BLACK)


class Coin:
    def __init__(self, speed):
        self.r = 15
        self.x = random.choice(LANES)
        self.y = -80
        self.speed = speed
        self.value = random.choice([1, 2, 5])

    def rect(self):
        return pygame.Rect(self.x - self.r, self.y - self.r, self.r * 2, self.r * 2)

    def update(self):
        self.y += self.speed

    def draw(self, screen):
        pygame.draw.circle(screen, YELLOW, (self.x, self.y), self.r)
        draw_text(screen, str(self.value), self.x, self.y, color=BLACK)


class PowerUp:
    def __init__(self, speed):
        self.size = 38
        self.x = random.choice(LANES) - self.size // 2
        self.y = -90
        self.speed = speed
        self.kind = random.choice(["nitro", "shield", "repair"])
        self.created = time.time()

    def rect(self):
        return pygame.Rect(self.x, self.y, self.size, self.size)

    def update(self):
        self.y += self.speed

    def expired(self):
        return time.time() - self.created > 7

    def draw(self, screen):
        if self.kind == "nitro":
            color = BLUE
            label = "N"
        elif self.kind == "shield":
            color = YELLOW
            label = "S"
        else:
            color = GREEN
            label = "R"

        pygame.draw.rect(screen, color, self.rect(), border_radius=12)
        draw_text(screen, label, self.x + 19, self.y + 19, color=BLACK)


def run_game(screen, username, settings):
    clock = pygame.time.Clock()

    player = Player(get_color(settings["car_color"]))

    enemies = []
    obstacles = []
    coins = []
    powerups = []

    score = 0
    distance = 0
    coin_count = 0

    active_power = None
    power_end = 0

    start_time = time.time()

    if settings["difficulty"] == "easy":
        enemy_spawn = 80
        obstacle_spawn = 130
    elif settings["difficulty"] == "hard":
        enemy_spawn = 45
        obstacle_spawn = 75
    else:
        enemy_spawn = 60
        obstacle_spawn = 100

    while True:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        game_seconds = time.time() - start_time

        speed = 5 + distance // 900

        if active_power == "nitro":
            speed += 4

        if active_power and time.time() > power_end:
            if active_power == "shield":
                player.shield = False
            active_power = None

        draw_background(screen, WIDTH, HEIGHT)

        player.move()
        player.draw(screen)

        # первые 2 секунды ничего опасного не появляется
        if game_seconds > 2:
            if random.randint(1, max(25, enemy_spawn - distance // 600)) == 1:
                enemies.append(EnemyCar(speed))

            if random.randint(1, max(35, obstacle_spawn - distance // 700)) == 1:
                obstacles.append(Obstacle(speed))

        if random.randint(1, 50) == 1:
            coins.append(Coin(speed))

        if game_seconds > 3 and random.randint(1, 320) == 1 and active_power is None:
            powerups.append(PowerUp(speed))

        for enemy in enemies[:]:
            enemy.update()
            enemy.draw(screen)

            if enemy.y > HEIGHT:
                enemies.remove(enemy)

            elif enemy.rect().colliderect(player.rect()):
                if player.shield:
                    player.shield = False
                    active_power = None
                    enemies.remove(enemy)
                else:
                    save_score(username, score, distance, coin_count)
                    return score, distance, coin_count

        for obstacle in obstacles[:]:
            obstacle.update()
            obstacle.draw(screen)

            if obstacle.y > HEIGHT:
                obstacles.remove(obstacle)

            elif obstacle.rect().colliderect(player.rect()):
                if active_power == "repair":
                    obstacles.remove(obstacle)
                    active_power = None
                elif player.shield:
                    player.shield = False
                    active_power = None
                    obstacles.remove(obstacle)
                else:
                    save_score(username, score, distance, coin_count)
                    return score, distance, coin_count

        for coin in coins[:]:
            coin.update()
            coin.draw(screen)

            if coin.y > HEIGHT:
                coins.remove(coin)

            elif coin.rect().colliderect(player.rect()):
                coin_count += coin.value
                score += coin.value * 10
                coins.remove(coin)

        for powerup in powerups[:]:
            powerup.update()
            powerup.draw(screen)

            if powerup.y > HEIGHT or powerup.expired():
                powerups.remove(powerup)

            elif powerup.rect().colliderect(player.rect()):
                active_power = powerup.kind

                if active_power == "nitro":
                    power_end = time.time() + 5

                elif active_power == "shield":
                    player.shield = True
                    power_end = time.time() + 8

                elif active_power == "repair":
                    power_end = time.time() + 5

                score += 50
                powerups.remove(powerup)

        score += 1
        distance += 1

        draw_text_left(screen, f"Player: {username}", 15, 15)
        draw_text_left(screen, f"Score: {score}", 15, 40)
        draw_text_left(screen, f"Coins: {coin_count}", 15, 65)
        draw_text_left(screen, f"Distance: {distance}m", 15, 90)

        if game_seconds < 2:
            draw_text(screen, "GET READY!", WIDTH // 2, HEIGHT // 2, color=YELLOW)

        if active_power:
            left = max(0, int(power_end - time.time()))
            draw_text_left(screen, f"Power: {active_power} {left}s", 300, 15)

        pygame.display.update()