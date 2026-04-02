import sys
import pygame
from pygame.locals import MOUSEMOTION, QUIT

pygame.init()
SURFACE = pygame.display.set_mode((600, 420))
pygame.display.set_caption("week03 problem02")
FPSCLOCK = pygame.time.Clock()


def main():
    click_points = []

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEMOTION and event.buttons[0]:
                click_points.append(event.pos)

        SURFACE.fill((248, 250, 242))
        pygame.draw.rect(SURFACE, (227, 238, 214), (42, 34, 516, 292), border_radius=20)
        pygame.draw.rect(SURFACE, (163, 199, 121), (42, 338, 516, 40), border_radius=14)

        for point in click_points:
            pygame.draw.circle(SURFACE, (68, 143, 78), point, 5)

        pygame.display.update()
        FPSCLOCK.tick(60)


if __name__ == "__main__":
    main()
