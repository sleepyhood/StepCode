import sys
import pygame
from pygame.locals import QUIT, MOUSEMOTION

pygame.init()
SURFACE = pygame.display.set_mode((600, 420))
pygame.display.set_caption("mission08 paint lab")
FPSCLOCK = pygame.time.Clock()


def main():
    mouse_positions = []

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEMOTION:
                # 수정 미션: 클릭할 때만 그려지도록 조건을 바꿔 보세요.
                mouse_positions.append(event.pos)

        SURFACE.fill((255, 255, 255))

        for pos in mouse_positions:
            pygame.draw.circle(SURFACE, (20, 20, 20), pos, 5)

        pygame.display.update()
        FPSCLOCK.tick(60)


if __name__ == "__main__":
    main()
