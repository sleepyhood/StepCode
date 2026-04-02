import sys
import pygame
from pygame.locals import QUIT

pygame.init()
SURFACE = pygame.display.set_mode((560, 340))
pygame.display.set_caption("week02 problem04")
FPSCLOCK = pygame.time.Clock()


def make_blades():
    blades = pygame.Surface((180, 180), pygame.SRCALPHA)
    pygame.draw.polygon(blades, (245, 245, 245), [(90, 18), (108, 86), (72, 86)])
    pygame.draw.polygon(blades, (240, 240, 240), [(162, 90), (94, 108), (94, 72)])
    pygame.draw.polygon(blades, (245, 245, 245), [(90, 162), (108, 94), (72, 94)])
    pygame.draw.polygon(blades, (240, 240, 240), [(18, 90), (86, 108), (86, 72)])
    pygame.draw.circle(blades, (110, 110, 110), (90, 90), 12)
    return blades


def main():
    blades = make_blades()
    theta = 0

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        theta += 1
        SURFACE.fill((176, 226, 255))
        pygame.draw.rect(SURFACE, (110, 90, 70), (270, 150, 20, 150))
        rotated = pygame.transform.rotate(blades, theta)
        rotated_rect = rotated.get_rect(center=(280, 170))
        SURFACE.blit(rotated, rotated_rect)

        pygame.display.update()
        FPSCLOCK.tick(60)


if __name__ == "__main__":
    main()
