import pygame

pygame.init()

WIDTH, HEIGHT = 600, 600
TILE_SIZE = 20

COLOR_SCENE = (0,103,79)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
running = True

def scene():
    for y in range(0, HEIGHT, TILE_SIZE):
        for x in range(0, WIDTH, TILE_SIZE):
            pygame.draw.rect(
                screen,
                COLOR_SCENE,
                (x, y, TILE_SIZE, TILE_SIZE),
                1
            )

while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()
    screen.fill((0, 0, 0))

    scene()


pygame.quit()


