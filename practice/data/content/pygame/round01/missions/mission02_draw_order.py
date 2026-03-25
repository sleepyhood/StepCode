import sys
import pygame
from pygame.locals import QUIT

pygame.init()
SURFACE = pygame.display.set_mode((500, 350))
pygame.display.set_caption("mission02 draw order")


def main():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        SURFACE.fill((245, 245, 245))

        # 실험 1: 두 도형의 좌표를 바꿔 완전히 겹치게 해 보세요.
        # 실험 2: 아래 두 draw 줄의 순서를 바꿔 보세요.
        pygame.draw.rect(SURFACE, (255, 120, 120), (140, 90, 170, 130))
        pygame.draw.circle(SURFACE, (80, 140, 255), (250, 170), 85)

        pygame.display.update()


if __name__ == "__main__":
    main()
