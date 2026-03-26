import sys
import pygame
from pygame.locals import QUIT

pygame.init()
SURFACE = pygame.display.set_mode((400, 300))
pygame.display.set_caption("round01 problem03")


def main():
    while True:
        # BLOCK_A_START
        SURFACE.fill((20, 20, 20))
        pygame.draw.circle(SURFACE, (255, 210, 80), (200, 150), 60)

        # 문제 3.1, 3.2: X 버튼으로 창이 닫히도록 고치세요.
        if False:
            pygame.quit()
            sys.exit()
        # BLOCK_A_END

        pygame.display.update()


if __name__ == "__main__":
    main()
