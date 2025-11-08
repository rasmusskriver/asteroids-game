import random

import pygame

from circleshape import CircleShape
from constants import ASTEROID_MIN_RADIUS
from logger import log_event


class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)

    def draw(self, screen):
        pygame.draw.circle(screen, "white", self.position, self.radius, width=2)

    def update(self, dt):
        self.position += self.velocity * dt

    def get_score_value(self):
        from constants import (ASTEROID_MAX_RADIUS, SCORE_LARGE_ASTEROID, 
                             SCORE_MEDIUM_ASTEROID, SCORE_SMALL_ASTEROID)
        if self.radius >= ASTEROID_MAX_RADIUS:
            return SCORE_LARGE_ASTEROID
        elif self.radius >= ASTEROID_MIN_RADIUS * 2:
            return SCORE_MEDIUM_ASTEROID
        else:
            return SCORE_SMALL_ASTEROID

    def split(self):
        self.kill()

        if self.radius <= ASTEROID_MIN_RADIUS:
            return

        log_event("asteroid_split")

        random_angle = random.uniform(20, 50)

        a = self.velocity.rotate(random_angle)
        b = self.velocity.rotate(-random_angle)

        new_radius = self.radius - ASTEROID_MIN_RADIUS
        asteroid = Asteroid(self.position.x, self.position.y, new_radius)
        asteroid.velocity = a * 1.2
        asteroid = Asteroid(self.position.x, self.position.y, new_radius)
        asteroid.velocity = b * 1.2
