import sys
import pygame
from pygame.locals import QUIT

pygame.init()
SURFACE = pygame.display.set_mode((400, 300))
pygame.display.set_caption("mission01 window")


def main():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        # 실험 1: 창 크기 숫자를 바꿔 보세요.
        # 실험 2: fill의 RGB 숫자를 바꿔 보세요.
        SURFACE.fill((255, 255, 255))
        pygame.display.update()


if __name__ == "__main__":
    main()
