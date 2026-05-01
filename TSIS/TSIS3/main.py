import pygame

from ui import init_ui, draw_text, button, BIG_FONT, FONT, SMALL_FONT, draw_background
from racer import run_game
from persistence import load_settings, save_settings, load_leaderboard

pygame.init()
init_ui()

WIDTH, HEIGHT = 500, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TSIS3 Girly Racer")


def get_username():
    name = ""

    while True:
        draw_background(screen, WIDTH, HEIGHT)
        draw_text(screen, "Enter your name", WIDTH // 2, 180, BIG_FONT)
        draw_text(screen, name + "|", WIDTH // 2, 280, FONT)
        draw_text(screen, "Press ENTER to start", WIDTH // 2, 350, SMALL_FONT)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if name.strip() == "":
                        name = "Player"
                    return name

                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]

                else:
                    if len(name) < 12:
                        name += event.unicode


def main_menu():
    while True:
        draw_background(screen, WIDTH, HEIGHT)

        draw_text(screen, "RACER GAME", WIDTH // 2, 120, BIG_FONT)
        draw_text(screen, "TSIS3 Advanced Pygame Project", WIDTH // 2, 165, SMALL_FONT)

        if button(screen, "Play", 150, 240, 200, 55):
            settings = load_settings()
            username = get_username()
            score, distance, coins = run_game(screen, username, settings)
            game_over_screen(score, distance, coins)

        if button(screen, "Leaderboard", 150, 315, 200, 55):
            leaderboard_screen()

        if button(screen, "Settings", 150, 390, 200, 55):
            settings_screen()

        if button(screen, "Quit", 150, 465, 200, 55):
            pygame.quit()
            exit()

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()


def game_over_screen(score, distance, coins):
    while True:
        draw_background(screen, WIDTH, HEIGHT)

        draw_text(screen, "GAME OVER", WIDTH // 2, 130, BIG_FONT)
        draw_text(screen, f"Score: {score}", WIDTH // 2, 230, FONT)
        draw_text(screen, f"Distance: {distance}m", WIDTH // 2, 270, FONT)
        draw_text(screen, f"Coins: {coins}", WIDTH // 2, 310, FONT)

        if button(screen, "Leaderboard", 150, 400, 200, 55):
            leaderboard_screen()

        if button(screen, "Main Menu", 150, 475, 200, 55):
            return

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()


def leaderboard_screen():
    while True:
        draw_background(screen, WIDTH, HEIGHT)
        leaderboard = load_leaderboard()

        draw_text(screen, "TOP 10 LEADERS", WIDTH // 2, 80, BIG_FONT)

        if not leaderboard:
            draw_text(screen, "No results yet", WIDTH // 2, 190, FONT)
        else:
            y = 145
            for i, item in enumerate(leaderboard, start=1):
                text = f"{i}. {item['name']} | Score: {item['score']} | {item['distance']}m | Coins: {item['coins']}"
                draw_text(screen, text, WIDTH // 2, y, SMALL_FONT)
                y += 38

        if button(screen, "Back", 150, 610, 200, 55):
            return

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()


def settings_screen():
    settings = load_settings()

    colors = ["pink", "blue", "green", "purple"]
    difficulties = ["easy", "normal", "hard"]

    while True:
        draw_background(screen, WIDTH, HEIGHT)

        draw_text(screen, "SETTINGS", WIDTH // 2, 100, BIG_FONT)

        sound_text = "Sound: ON" if settings["sound"] else "Sound: OFF"
        color_text = f"Car Color: {settings['car_color']}"
        difficulty_text = f"Difficulty: {settings['difficulty']}"

        if button(screen, sound_text, 105, 210, 290, 55):
            settings["sound"] = not settings["sound"]
            save_settings(settings)

        if button(screen, color_text, 105, 290, 290, 55):
            index = colors.index(settings["car_color"])
            settings["car_color"] = colors[(index + 1) % len(colors)]
            save_settings(settings)

        if button(screen, difficulty_text, 105, 370, 290, 55):
            index = difficulties.index(settings["difficulty"])
            settings["difficulty"] = difficulties[(index + 1) % len(difficulties)]
            save_settings(settings)

        if button(screen, "Back", 150, 530, 200, 55):
            return

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()


main_menu()