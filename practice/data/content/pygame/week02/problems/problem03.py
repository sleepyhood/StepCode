import sys
import pygame
from pygame.locals import QUIT

pygame.init()
SURFACE = pygame.display.set_mode((520, 320))
pygame.display.set_caption("week02 problem03")
FPSCLOCK = pygame.time.Clock()


def make_sprite():
    sprite = pygame.Surface((140, 80), pygame.SRCALPHA)
    pygame.draw.rect(sprite, (255, 140, 120), (10, 10, 120, 60), border_radius=12)
    pygame.draw.circle(sprite, (255, 230, 90), (35, 40), 14)
    pygame.draw.circle(sprite, (90, 180, 255), (105, 40), 14)
    return sprite


def main():
    sprite = make_sprite()
    theta = 0

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        theta += 3
        SURFACE.fill((25, 25, 30))
        rotated = pygame.transform.rotate(sprite, theta)

        # BLOCK_A_START
        rotated_rect = rotated.get_rect()
        # 문제 3.1, 3.4: 중심 좌표를 올바르게 고치세요.
        rotated_rect.center = (180, 120)
        SURFACE.blit(rotated, rotated_rect)
        # BLOCK_A_END

        pygame.display.update()
        FPSCLOCK.tick(60)


if __name__ == "__main__":
    main()
