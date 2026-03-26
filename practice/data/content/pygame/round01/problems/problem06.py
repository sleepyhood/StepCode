import sys
import pygame
from pygame.locals import QUIT, MOUSEMOTION

pygame.init()
SURFACE = pygame.display.set_mode((600, 420))
pygame.display.set_caption("round01 problem06")
FPSCLOCK = pygame.time.Clock()


def main():
    mouse_positions = []

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            # BLOCK_A_START
            elif event.type == MOUSEMOTION:
                # 문제 6.2: 클릭한 상태에서만 점이 그려지도록 고치세요.
                mouse_positions.append(event.pos)
            # BLOCK_A_END

        SURFACE.fill((255, 255, 255))

        # BLOCK_B_START
        for pos in mouse_positions:
            pygame.draw.circle(SURFACE, (20, 20, 20), pos, 5)
        # BLOCK_B_END

        pygame.display.update()
        FPSCLOCK.tick(60)


if __name__ == "__main__":
    main()
