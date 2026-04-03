import pygame

pygame.init()

WIDTH, HEIGHT = 640, 480
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

x = 320
y = 240
speed = 5
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        x -= speed
    if keys[pygame.K_RIGHT]:
        x += speed
    if keys[pygame.K_UP]:
        y -= speed
    if keys[pygame.K_DOWN]:
        y += speed

    x = max(20, min(WIDTH - 20, x))
    y = max(20, min(HEIGHT - 20, y))

    screen.fill("black")
    pygame.draw.circle(screen, "dodgerblue", (x, y), 20)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()