import pygame

pygame.init()

WIDTH, HEIGHT = 600, 600
TILE_SIZE = 20

COLOR_SCENE = (0,103,79)
COLOR_SNAKE = (0, 200, 0)

snake_x = WIDTH // TILE_SIZE // 2
snake_y = HEIGHT // TILE_SIZE // 2

dir_x = 1
dir_y = 0

move_delay = 8
move_counter = 0

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
running = True

def draw_scene():
    for y in range(0, HEIGHT, TILE_SIZE):
        for x in range(0, WIDTH, TILE_SIZE):
            pygame.draw.rect(
                screen,
                COLOR_SCENE,
                (x, y, TILE_SIZE, TILE_SIZE),
                1
            )

def draw_snake():
    rect = (
        snake_x * TILE_SIZE,
        snake_y * TILE_SIZE,
        TILE_SIZE,
        TILE_SIZE
    )
    pygame.draw.rect(screen, COLOR_SNAKE, rect)


def move_snake():
    global snake_x, snake_y

    snake_x += dir_x
    snake_y += dir_y

    max_x = WIDTH // TILE_SIZE
    max_y = HEIGHT // TILE_SIZE

    snake_x %= max_x
    snake_y %= max_y

while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    move_counter += 1
    if move_counter >= move_delay:
        move_counter = 0
        move_snake()

    pygame.display.flip()
    screen.fill((0, 0, 0))

    draw_scene()
    draw_snake()


pygame.quit()


