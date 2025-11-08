import random

import pygame

from circleshape import CircleShape
from constants import POWERUP_RADIUS, POWERUP_SPEED


class PowerUp(CircleShape):
    TYPES = ["rapid_fire", "shield", "triple_shot"]
    COLORS = {
        "rapid_fire": "yellow",
        "shield": "cyan",
        "triple_shot": "magenta"
    }

    def __init__(self, x, y):
        super().__init__(x, y, POWERUP_RADIUS)
        self.type = random.choice(self.TYPES)
        self.velocity = pygame.Vector2(
            random.uniform(-POWERUP_SPEED, POWERUP_SPEED),
            random.uniform(-POWERUP_SPEED, POWERUP_SPEED)
        )

    def draw(self, screen):
        color = self.COLORS[self.type]
        pygame.draw.circle(screen, color, self.position, self.radius, width=3)
        # Draw inner star
        points = []
        for i in range(5):
            angle = i * 72 - 90
            x = self.position.x + pygame.math.Vector2(0, self.radius * 0.5).rotate(angle).x
            y = self.position.y + pygame.math.Vector2(0, self.radius * 0.5).rotate(angle).y
            points.append((x, y))
        pygame.draw.polygon(screen, color, points, width=2)

    def update(self, dt):
        self.position += self.velocity * dt
        # Wrap around screen
        from constants import SCREEN_WIDTH, SCREEN_HEIGHT
        if self.position.x < 0:
            self.position.x = SCREEN_WIDTH
        if self.position.x > SCREEN_WIDTH:
            self.position.x = 0
        if self.position.y < 0:
            self.position.y = SCREEN_HEIGHT
        if self.position.y > SCREEN_HEIGHT:
            self.position.y = 0
