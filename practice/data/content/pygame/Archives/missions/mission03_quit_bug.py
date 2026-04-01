import sys
import pygame
from pygame.locals import QUIT

pygame.init()
SURFACE = pygame.display.set_mode((400, 300))
pygame.display.set_caption("mission03 quit bug")


def main():
    while True:
        SURFACE.fill((20, 20, 20))
        pygame.draw.circle(SURFACE, (255, 210, 80), (200, 150), 60)

        # 수정 미션: X 버튼으로 창이 닫히도록 이벤트 처리 코드를 고치세요.
        if False:
            pygame.quit()
            sys.exit()

        pygame.display.update()


if __name__ == "__main__":
    main()
