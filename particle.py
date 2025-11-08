import random

import pygame

from circleshape import CircleShape
from constants import PARTICLE_LIFETIME


class Particle(CircleShape):
    def __init__(self, x, y, color="white"):
        super().__init__(x, y, random.uniform(1, 3))
        self.color = color
        self.lifetime = PARTICLE_LIFETIME
        speed = random.uniform(50, 200)
        angle = random.uniform(0, 360)
        self.velocity = pygame.Vector2(0, 1).rotate(angle) * speed

    def draw(self, screen):
        alpha = int(255 * (self.lifetime / PARTICLE_LIFETIME))
        if alpha > 0:
            surface = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(surface, (*self.get_rgb_color(), alpha), 
                             (self.radius, self.radius), self.radius)
            screen.blit(surface, (self.position.x - self.radius, 
                                 self.position.y - self.radius))

    def get_rgb_color(self):
        color_map = {
            "white": (255, 255, 255),
            "orange": (255, 165, 0),
            "red": (255, 0, 0),
            "yellow": (255, 255, 0),
            "cyan": (0, 255, 255),
            "magenta": (255, 0, 255)
        }
        return color_map.get(self.color, (255, 255, 255))

    def update(self, dt):
        self.lifetime -= dt
        if self.lifetime <= 0:
            self.kill()
        self.position += self.velocity * dt
        self.velocity *= 0.98  # Add drag
