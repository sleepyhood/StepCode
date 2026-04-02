import sys
import pygame
from pygame.locals import QUIT

pygame.init()
SURFACE = pygame.display.set_mode((520, 320))
pygame.display.set_caption("week02 problem03")
FPSCLOCK = pygame.time.Clock()


def make_logo_card():
    card = pygame.Surface((170, 110), pygame.SRCALPHA)
    pygame.draw.rect(card, (86, 122, 255), (0, 0, 170, 110), border_radius=22)
    pygame.draw.polygon(card, (245, 245, 255), [(84, 20), (128, 55), (84, 90), (40, 55)])
    pygame.draw.circle(card, (255, 214, 90), (84, 55), 12)
    return card


def main():
    logo_card = make_logo_card()
    theta = 0

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        theta += 3
        SURFACE.fill((20, 36, 62))
        rotated = pygame.transform.rotate(logo_card, theta)
        rotated_rect = rotated.get_rect()
        rotated_rect.center = (260, 160)
        SURFACE.blit(rotated, rotated_rect)

        pygame.display.update()
        FPSCLOCK.tick(60)


if __name__ == "__main__":
    main()
