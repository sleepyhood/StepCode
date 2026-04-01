import sys
import pygame
from pygame.locals import QUIT

pygame.init()
SURFACE = pygame.display.set_mode((500, 220))
pygame.display.set_caption("mission05 fps test")
FPSCLOCK = pygame.time.Clock()
FONT = pygame.font.SysFont(None, 36)


def main():
    xpos = 0

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        xpos += 4
        if xpos > 540:
            xpos = -40

        SURFACE.fill((250, 250, 250))
        pygame.draw.rect(SURFACE, (50, 120, 255), (xpos, 90, 40, 40))

        info = FONT.render("Change tick(60) to 1, 10, 60, 120", True, (30, 30, 30))
        SURFACE.blit(info, (40, 30))

        pygame.display.update()

        # 실험 미션: tick 숫자를 바꿔 속도를 비교해 보세요.
        FPSCLOCK.tick(60)


if __name__ == "__main__":
    main()
