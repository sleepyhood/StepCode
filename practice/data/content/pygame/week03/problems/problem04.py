import sys
import pygame
from pygame.locals import MOUSEBUTTONDOWN, MOUSEBUTTONUP, MOUSEMOTION, QUIT

pygame.init()
SURFACE = pygame.display.set_mode((620, 420))
pygame.display.set_caption("week03 problem04")
FPSCLOCK = pygame.time.Clock()


def main():
    stamp_points = []
    is_stamping = False

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                is_stamping = True
            elif event.type == MOUSEBUTTONUP:
                is_stamping = False
            elif event.type == MOUSEMOTION and is_stamping:
                stamp_points.append(event.pos)

        SURFACE.fill((253, 244, 230))
        pygame.draw.rect(SURFACE, (242, 223, 205), (36, 28, 548, 308), border_radius=18)
        pygame.draw.rect(SURFACE, (226, 184, 150), (36, 346, 548, 36), border_radius=12)

        for stamp in stamp_points:
            pygame.draw.rect(SURFACE, (255, 108, 108), (stamp[0] - 8, stamp[1] - 8, 16, 16), border_radius=4)
            pygame.draw.rect(SURFACE, (255, 245, 238), (stamp[0] - 2, stamp[1] - 2, 4, 4), border_radius=2)

        pygame.display.update()
        FPSCLOCK.tick(60)


if __name__ == "__main__":
    main()
