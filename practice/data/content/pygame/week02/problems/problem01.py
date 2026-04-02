import sys
import pygame
from pygame.locals import QUIT

pygame.init()
SURFACE = pygame.display.set_mode((560, 340))
pygame.display.set_caption("week02 problem01")


def make_salmon_sticker():
    sticker = pygame.Surface((150, 110), pygame.SRCALPHA)
    pygame.draw.rect(sticker, (255, 180, 155), (0, 0, 150, 110), border_radius=18)
    pygame.draw.circle(sticker, (255, 245, 225), (45, 38), 16)
    pygame.draw.circle(sticker, (255, 245, 225), (105, 38), 16)
    pygame.draw.rect(sticker, (255, 235, 210), (28, 66, 94, 18), border_radius=9)
    return sticker


def make_blue_sticker():
    sticker = pygame.Surface((130, 130), pygame.SRCALPHA)
    pygame.draw.circle(sticker, (120, 180, 255), (65, 65), 60)
    pygame.draw.circle(sticker, (235, 245, 255), (65, 65), 32)
    pygame.draw.circle(sticker, (120, 180, 255), (65, 65), 14)
    return sticker


def main():
    salmon_sticker = make_salmon_sticker()
    blue_sticker = make_blue_sticker()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        SURFACE.fill((245, 238, 220))
        pygame.draw.rect(SURFACE, (225, 212, 188), (30, 24, 500, 270), border_radius=16)
        SURFACE.blit(salmon_sticker, (120, 120))
        SURFACE.blit(blue_sticker, (360, 110))

        pygame.display.update()


if __name__ == "__main__":
    main()
