import sys
import pygame
from pygame.locals import QUIT

pygame.init()
SURFACE = pygame.display.set_mode((520, 320))
pygame.display.set_caption("week02 problem01")


def make_sprite():
    sprite = pygame.Surface((140, 80), pygame.SRCALPHA)
    pygame.draw.rect(sprite, (255, 140, 120), (10, 10, 120, 60), border_radius=12)
    pygame.draw.circle(sprite, (255, 230, 90), (35, 40), 14)
    pygame.draw.circle(sprite, (90, 180, 255), (105, 40), 14)
    return sprite


def main():
    sprite = make_sprite()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        SURFACE.fill((25, 25, 30))

        # BLOCK_A_START
        # 문제 1.2: 이미지를 화면 가운데 근처로 옮기세요.
        SURFACE.blit(sprite, (0, 0))
        # BLOCK_A_END

        pygame.display.update()


if __name__ == "__main__":
    main()
