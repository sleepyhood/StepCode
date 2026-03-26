from __future__ import annotations

import os
from pathlib import Path

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")

import imageio.v2 as imageio
import pygame


ROOT = Path(__file__).resolve().parent
OUT_DIR = ROOT / "reference_images"


def save_problem01():
    surface = pygame.display.set_mode((400, 300))
    surface.fill((0, 255, 0))
    pygame.draw.rect(surface, (255, 120, 120), (120, 105, 160, 90))
    pygame.image.save(surface, OUT_DIR / "problem01_correct.png")


def save_problem04():
    surface = pygame.display.set_mode((500, 240))
    surface.fill((160, 100, 95))
    pygame.draw.rect(surface, (50, 120, 255), (180, 120, 40, 40))
    pygame.image.save(surface, OUT_DIR / "problem04_correct.png")


def make_sprite():
    sprite = pygame.Surface((140, 80), pygame.SRCALPHA)
    pygame.draw.rect(sprite, (255, 140, 120), (10, 10, 120, 60), border_radius=12)
    pygame.draw.circle(sprite, (255, 230, 90), (35, 40), 14)
    pygame.draw.circle(sprite, (90, 180, 255), (105, 40), 14)
    return sprite


def save_problem05():
    surface = pygame.display.set_mode((520, 320))
    surface.fill((25, 25, 30))
    rotated = pygame.transform.rotate(make_sprite(), 35)
    rotated_rect = rotated.get_rect(center=(260, 160))
    surface.blit(rotated, rotated_rect)
    pygame.image.save(surface, OUT_DIR / "problem05_correct.png")


def save_problem06():
    surface = pygame.display.set_mode((600, 420))
    surface.fill((255, 255, 255))
    mouse_positions = [(120, 120), (160, 150), (210, 180), (260, 210), (310, 240)]
    for pos in mouse_positions:
        pygame.draw.circle(surface, (255, 80, 80), pos, 8)
    pygame.image.save(surface, OUT_DIR / "problem06_correct.png")


def surface_to_frame(surface: pygame.Surface):
    return pygame.surfarray.array3d(surface).swapaxes(0, 1)


def save_problem05_gif():
    surface = pygame.display.set_mode((520, 320))
    sprite = make_sprite()
    frames = []

    for theta in range(0, 200, 20):
        surface.fill((25, 25, 30))
        rotated = pygame.transform.rotate(sprite, theta)
        rotated_rect = rotated.get_rect(center=(260, 160))
        surface.blit(rotated, rotated_rect)
        frames.append(surface_to_frame(surface).copy())

    imageio.mimsave(OUT_DIR / "problem05_correct.gif", frames, duration=0.12, loop=0)


def save_problem06_gif():
    surface = pygame.display.set_mode((600, 420))
    path = [(120, 120), (160, 150), (210, 180), (260, 210), (310, 240), (360, 270)]
    frames = []

    for count in range(0, len(path) + 2):
        surface.fill((255, 255, 255))

        if count >= 2:
            for pos in path[: count - 1]:
                pygame.draw.circle(surface, (255, 80, 80), pos, 8)

        frames.append(surface_to_frame(surface).copy())

    imageio.mimsave(OUT_DIR / "problem06_correct.gif", frames, duration=0.16, loop=0)


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    pygame.init()
    save_problem01()
    save_problem04()
    save_problem05()
    save_problem06()
    save_problem05_gif()
    save_problem06_gif()
    pygame.quit()
    print(f"saved: {OUT_DIR}")


if __name__ == "__main__":
    main()
