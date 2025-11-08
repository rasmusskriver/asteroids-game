import random

import pygame

from constants import SCREEN_WIDTH, SCREEN_HEIGHT


class Starfield:
    def __init__(self, star_count=100):
        self.stars = []
        for _ in range(star_count):
            x = random.randint(0, SCREEN_WIDTH)
            y = random.randint(0, SCREEN_HEIGHT)
            brightness = random.uniform(0.3, 1.0)
            size = random.randint(1, 2)
            self.stars.append((x, y, brightness, size))

    def draw(self, screen):
        for x, y, brightness, size in self.stars:
            color = int(255 * brightness)
            pygame.draw.circle(screen, (color, color, color), (x, y), size)
