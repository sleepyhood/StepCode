import sys
import pygame
from pygame.locals import QUIT

pygame.init()
SURFACE = pygame.display.set_mode((500, 240))
pygame.display.set_caption("round01 problem04")
FPSCLOCK = pygame.time.Clock()


def main():
    xpos = 0
    color_value = 0

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        # BLOCK_A_START
        xpos += 4
        if xpos > 540:
            xpos = -40

        color_value += 3
        if color_value > 255:
            color_value = 0

        SURFACE.fill((color_value, 100, 255 - color_value))
        pygame.draw.rect(SURFACE, (50, 120, 255), (xpos, 120, 40, 40))
        # BLOCK_A_END

        # 문제 3.1: 화면 변화가 보이도록 빠진 한 줄을 넣으세요.
        # 문제 3.2, 3.3: tick 값을 바꿔 움직임을 비교하세요.
        FPSCLOCK.tick(60)


if __name__ == "__main__":
    main()
