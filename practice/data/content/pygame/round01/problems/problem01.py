import sys
import pygame
from pygame.locals import QUIT

pygame.init()
SURFACE = pygame.display.set_mode((400, 300))
pygame.display.set_caption("round01 problem01")


def main():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        # BLOCK_A_START
        # 문제 1.1: 왜 실행 오류가 나는지 찾고 고치세요.
        SURFACE.fill((255, 255))

        # 문제 1.2: 사각형이 화면 중앙에 오도록 좌표를 수정하세요.
        pygame.draw.rect(SURFACE, (255, 120, 120), (0, 0, 160, 90))
        # BLOCK_A_END
        pygame.display.update()


if __name__ == "__main__":
    main()
