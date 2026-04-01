import sys
import pygame
from pygame.locals import QUIT, Rect

pygame.init()
SURFACE = pygame.display.set_mode((500, 350))
pygame.display.set_caption("mission06 shape lab")


def main():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        SURFACE.fill((255, 255, 255))

        # 실험 1: 각 도형의 x, y, width, height를 바꿔 보세요.
        # 실험 2: 선 굵기 0과 5를 비교해 보세요.
        pygame.draw.rect(SURFACE, (255, 120, 120), (40, 60, 160, 90))
        pygame.draw.rect(SURFACE, (80, 140, 255), (120, 110, 180, 120), 5)

        rect0 = Rect(290, 40, 120, 80)
        pygame.draw.rect(SURFACE, (110, 210, 140), rect0)
        pygame.draw.circle(SURFACE, (255, 210, 70), (360, 240), 55, 0)

        pygame.display.update()


if __name__ == "__main__":
    main()
