import sys
import pygame
from pygame.locals import MOUSEBUTTONDOWN, MOUSEBUTTONUP, MOUSEMOTION, QUIT

pygame.init()
SURFACE = pygame.display.set_mode((620, 420))
pygame.display.set_caption("week03 problem03")
FPSCLOCK = pygame.time.Clock()


def main():
    trail_points = []
    is_drawing = False

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                is_drawing = True
            elif event.type == MOUSEBUTTONUP:
                is_drawing = False
            elif event.type == MOUSEMOTION and is_drawing:
                trail_points.append(event.pos)

        SURFACE.fill((28, 39, 64))
        pygame.draw.rect(SURFACE, (238, 242, 250), (58, 34, 504, 332), border_radius=18)
        pygame.draw.rect(SURFACE, (80, 104, 142), (58, 34, 504, 18), border_radius=8)

        for point in trail_points:
            pygame.draw.circle(SURFACE, (255, 196, 79), point, 4)

        if trail_points:
            pygame.draw.circle(SURFACE, (77, 170, 255), trail_points[-1], 9, 2)

        pygame.display.update()
        FPSCLOCK.tick(60)


if __name__ == "__main__":
    main()
