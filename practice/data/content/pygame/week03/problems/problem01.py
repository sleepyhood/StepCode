import sys
import pygame
from pygame.locals import MOUSEMOTION, QUIT

pygame.init()
SURFACE = pygame.display.set_mode((600, 420))
pygame.display.set_caption("week03 problem01")
FPSCLOCK = pygame.time.Clock()


def main():
    hover_points = []

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEMOTION:
                hover_points.append(event.pos)

        SURFACE.fill((232, 241, 255))
        pygame.draw.rect(SURFACE, (207, 223, 247), (28, 24, 544, 320), border_radius=18)
        pygame.draw.rect(SURFACE, (160, 188, 227), (28, 356, 544, 32), border_radius=12)

        for point in hover_points:
            pygame.draw.circle(SURFACE, (70, 126, 214), point, 4)

        pygame.display.update()
        FPSCLOCK.tick(60)


if __name__ == "__main__":
    main()
