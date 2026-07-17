import pygame
import random
import sys

pygame.init()

WIDTH, HEIGHT = 600, 600
TILE_SIZE = 20
GRID_W = WIDTH // TILE_SIZE
GRID_H = HEIGHT // TILE_SIZE

COLOR_BG = (10, 10, 10)
COLOR_SCENE = (0, 103, 79)
COLOR_SNAKE_HEAD = (0, 230, 0)
COLOR_SNAKE_BODY = (0, 160, 0)
COLOR_FOOD = (220, 40, 40)
COLOR_TEXT = (240, 240, 240)
COLOR_SHADOW = (0, 0, 0)

MOVE_DELAY = 8

STATE_MENU = "menu"
STATE_PLAYING = "playing"
STATE_PAUSED = "paused"
STATE_GAMEOVER = "gameover"

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake")
clock = pygame.time.Clock()

font_big = pygame.font.SysFont("arial", 48, bold=True)
font_medium = pygame.font.SysFont("arial", 28, bold=True)
font_small = pygame.font.SysFont("arial", 20)


def draw_text_centered(text, font, color, cy, cx=WIDTH // 2, shadow=True):
    if shadow:
        s = font.render(text, True, COLOR_SHADOW)
        rect = s.get_rect(center=(cx + 2, cy + 2))
        screen.blit(s, rect)
    surface = font.render(text, True, color)
    rect = surface.get_rect(center=(cx, cy))
    screen.blit(surface, rect)


class SnakeGame:
    def __init__(self):
        self.reset()
        self.high_score = 0
        self.state = STATE_MENU

    def reset(self):
        start_x = GRID_W // 2
        start_y = GRID_H // 2

        self.snake = [
            (start_x, start_y),
            (start_x - 1, start_y),
            (start_x - 2, start_y),
        ]
        self.dir_x, self.dir_y = 1, 0
        self.next_dir_x, self.next_dir_y = 1, 0
        self.move_counter = 0
        self.score = 0
        self.food = self.spawn_food()

    def spawn_food(self):
        while True:
            pos = (random.randint(0, GRID_W - 1), random.randint(0, GRID_H - 1))
            if pos not in self.snake:
                return pos

    def set_direction(self, dx, dy):
        if (dx, dy) != (-self.dir_x, -self.dir_y):
            self.next_dir_x, self.next_dir_y = dx, dy

    def move(self):
        self.dir_x, self.dir_y = self.next_dir_x, self.next_dir_y
        head_x, head_y = self.snake[0]
        new_head = ((head_x + self.dir_x) % GRID_W, (head_y + self.dir_y) % GRID_H)

        if new_head in self.snake:
            self.game_over()
            return

        self.snake.insert(0, new_head)

        if new_head == self.food:
            self.score += 1
            self.high_score = max(self.high_score, self.score)
            self.food = self.spawn_food()
        else:
            self.snake.pop()

    def game_over(self):
        self.state = STATE_GAMEOVER

    def update(self):
        if self.state != STATE_PLAYING:
            return
        self.move_counter += 1
        if self.move_counter >= MOVE_DELAY:
            self.move_counter = 0
            self.move()

    def draw_scene(self):
        for y in range(0, HEIGHT, TILE_SIZE):
            for x in range(0, WIDTH, TILE_SIZE):
                pygame.draw.rect(screen, COLOR_SCENE, (x, y, TILE_SIZE, TILE_SIZE), 1)

    def draw_snake(self):
        for i, (x, y) in enumerate(self.snake):
            color = COLOR_SNAKE_HEAD if i == 0 else COLOR_SNAKE_BODY
            rect = (x * TILE_SIZE + 1, y * TILE_SIZE + 1, TILE_SIZE - 2, TILE_SIZE - 2)
            pygame.draw.rect(screen, color, rect)

    def draw_food(self):
        x, y = self.food
        rect = (x * TILE_SIZE + 2, y * TILE_SIZE + 2, TILE_SIZE - 4, TILE_SIZE - 4)
        pygame.draw.rect(screen, COLOR_FOOD, rect)

    def draw_hud(self):
        text = font_small.render(f"Pontos: {self.score}", True, COLOR_TEXT)
        screen.blit(text, (10, 8))
        hint = font_small.render("P - Pausar", True, COLOR_TEXT)
        screen.blit(hint, (WIDTH - hint.get_width() - 10, 8))

    def draw_playing(self):
        self.draw_scene()
        self.draw_food()
        self.draw_snake()
        self.draw_hud()

    def draw_menu(self):
        self.draw_scene()
        draw_text_centered("SNAKE", font_big, COLOR_SNAKE_HEAD, HEIGHT // 2 - 60)
        draw_text_centered("Pressione ENTER para jogar", font_medium, COLOR_TEXT, HEIGHT // 2 + 10)
        draw_text_centered("Setas / WASD para mover  |  P para pausar", font_small, COLOR_TEXT, HEIGHT // 2 + 55)
        if self.high_score > 0:
            draw_text_centered(f"Recorde: {self.high_score}", font_small, COLOR_TEXT, HEIGHT // 2 + 90)

    def draw_paused(self):
        self.draw_playing()
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        screen.blit(overlay, (0, 0))
        draw_text_centered("PAUSADO", font_big, COLOR_TEXT, HEIGHT // 2 - 20)
        draw_text_centered("Pressione P para continuar", font_medium, COLOR_TEXT, HEIGHT // 2 + 30)

    def draw_gameover(self):
        self.draw_scene()
        self.draw_food()
        self.draw_snake()
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 170))
        screen.blit(overlay, (0, 0))
        draw_text_centered("FIM DE JOGO", font_big, (220, 40, 40), HEIGHT // 2 - 60)
        draw_text_centered(f"Pontuação: {self.score}", font_medium, COLOR_TEXT, HEIGHT // 2)
        draw_text_centered(f"Recorde: {self.high_score}", font_small, COLOR_TEXT, HEIGHT // 2 + 35)
        draw_text_centered("ENTER - Jogar novamente   |   ESC - Menu", font_small, COLOR_TEXT, HEIGHT // 2 + 75)

    def draw(self):
        screen.fill(COLOR_BG)
        if self.state == STATE_MENU:
            self.draw_menu()
        elif self.state == STATE_PLAYING:
            self.draw_playing()
        elif self.state == STATE_PAUSED:
            self.draw_paused()
        elif self.state == STATE_GAMEOVER:
            self.draw_gameover()

    def handle_key(self, key):
        if self.state == STATE_MENU:
            if key == pygame.K_RETURN:
                self.reset()
                self.state = STATE_PLAYING

        elif self.state == STATE_PLAYING:
            if key in (pygame.K_UP, pygame.K_w):
                self.set_direction(0, -1)
            elif key in (pygame.K_DOWN, pygame.K_s):
                self.set_direction(0, 1)
            elif key in (pygame.K_LEFT, pygame.K_a):
                self.set_direction(-1, 0)
            elif key in (pygame.K_RIGHT, pygame.K_d):
                self.set_direction(1, 0)
            elif key == pygame.K_p:
                self.state = STATE_PAUSED

        elif self.state == STATE_PAUSED:
            if key == pygame.K_p:
                self.state = STATE_PLAYING

        elif self.state == STATE_GAMEOVER:
            if key == pygame.K_RETURN:
                self.reset()
                self.state = STATE_PLAYING
            elif key == pygame.K_ESCAPE:
                self.state = STATE_MENU


def main():
    snake_game = SnakeGame()
    running = True

    while running:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE and snake_game.state == STATE_PLAYING:
                    snake_game.state = STATE_MENU
                else:
                    snake_game.handle_key(event.key)

        snake_game.update()
        snake_game.draw()
        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()