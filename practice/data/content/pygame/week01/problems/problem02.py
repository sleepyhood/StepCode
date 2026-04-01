import sys
import pygame
from pygame.locals import QUIT

pygame.init()
SURFACE = pygame.display.set_mode((500, 350))
pygame.display.set_caption("round01 problem02")


def main():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        # BLOCK_A_START
        SURFACE.fill((245, 245, 245))
        pygame.draw.rect(SURFACE, (255, 120, 120), (140, 90, 170, 130))
        pygame.draw.circle(SURFACE, (80, 140, 255), (250, 170), 85)
        # BLOCK_A_END
        pygame.display.update()


if __name__ == "__main__":
    main()
