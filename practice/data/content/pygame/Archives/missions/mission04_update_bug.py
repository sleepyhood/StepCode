import sys
import pygame
from pygame.locals import QUIT

pygame.init()
SURFACE = pygame.display.set_mode((420, 320))
pygame.display.set_caption("mission04 update bug")
FPSCLOCK = pygame.time.Clock()


def main():
    color_value = 0

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        color_value += 3
        if color_value > 255:
            color_value = 0

        SURFACE.fill((color_value, 100, 255 - color_value))

        # 수정 미션: 화면 변화가 보이도록 빠진 한 줄을 넣으세요.
        FPSCLOCK.tick(30)


if __name__ == "__main__":
    main()
