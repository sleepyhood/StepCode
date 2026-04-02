import sys
import pygame
from pygame.locals import QUIT

pygame.init()
SURFACE = pygame.display.set_mode((520, 320))
pygame.display.set_caption("week02 problem02")
FPSCLOCK = pygame.time.Clock()


def make_badge():
    badge = pygame.Surface((140, 140), pygame.SRCALPHA)
    pygame.draw.circle(badge, (255, 210, 90), (70, 70), 60)
    pygame.draw.circle(badge, (250, 120, 120), (70, 70), 38)
    pygame.draw.rect(badge, (255, 245, 210), (62, 15, 16, 42), border_radius=8)
    pygame.draw.rect(badge, (255, 245, 210), (62, 83, 16, 42), border_radius=8)
    pygame.draw.rect(badge, (255, 245, 210), (15, 62, 42, 16), border_radius=8)
    pygame.draw.rect(badge, (255, 245, 210), (83, 62, 42, 16), border_radius=8)
    return badge


def main():
    badge = make_badge()
    theta = 0

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        theta += 3
        SURFACE.fill((28, 30, 40))
        rotated = pygame.transform.rotate(badge, theta)
        rotated_rect = rotated.get_rect(center=(260, 160))
        SURFACE.blit(rotated, rotated_rect)

        pygame.display.update()
        FPSCLOCK.tick(60)


if __name__ == "__main__":
    main()
