import pygame

from circleshape import CircleShape
from constants import *
from shot import Shot


class Player(CircleShape):
    def __init__(self, x, y, game_state=None):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.shoot_timer = 0
        self.invulnerable_timer = PLAYER_INVULNERABILITY_TIME
        self.game_state = game_state
        self.thruster_on = False

    def draw(self, screen):
        # Blink when invulnerable
        if self.invulnerable_timer > 0 and int(self.invulnerable_timer * 10) % 2 == 0:
            return
        
        # Draw shield if active
        if self.game_state and self.game_state.has_shield():
            pygame.draw.circle(screen, "cyan", self.position, self.radius + 8, width=2)
        
        # Draw ship
        pygame.draw.polygon(screen, "white", self.triangle(), 2)
        
        # Draw thruster
        if self.thruster_on:
            self.draw_thruster(screen)

    def draw_thruster(self, screen):
        import random
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        back = self.position - forward * self.radius
        flame_length = self.radius * random.uniform(0.5, 1.0)
        flame_point = back - forward * flame_length
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 3
        
        flame_points = [
            back + right,
            flame_point,
            back - right
        ]
        pygame.draw.polygon(screen, "orange", flame_points)

    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    def update(self, dt):
        self.shoot_timer -= dt
        self.invulnerable_timer -= dt
        self.thruster_on = False
        
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            self.thruster_on = True
            self.move(dt)
        if keys[pygame.K_s]:
            self.move(-dt)
        if keys[pygame.K_a]:
            self.rotate(-dt)
        if keys[pygame.K_d]:
            self.rotate(dt)
        if keys[pygame.K_SPACE]:
            self.shoot()
        
        # Wrap around screen
        if self.position.x < 0:
            self.position.x = SCREEN_WIDTH
        if self.position.x > SCREEN_WIDTH:
            self.position.x = 0
        if self.position.y < 0:
            self.position.y = SCREEN_HEIGHT
        if self.position.y > SCREEN_HEIGHT:
            self.position.y = 0

    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt

    def move(self, dt):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.position += forward * PLAYER_SPEED * dt

    def shoot(self):
        if self.shoot_timer > 0:
            return
        
        # Rapid fire power-up reduces cooldown
        cooldown = PLAYER_SHOOT_COOLDOWN_SECONDS
        if self.game_state and self.game_state.has_rapid_fire():
            cooldown *= 0.5
        
        self.shoot_timer = cooldown
        
        # Triple shot power-up
        if self.game_state and self.game_state.has_triple_shot():
            self.shoot_triple()
        else:
            shot = Shot(self.position.x, self.position.y)
            shot.velocity = pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_SHOOT_SPEED
    
    def shoot_triple(self):
        # Center shot
        shot = Shot(self.position.x, self.position.y)
        shot.velocity = pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_SHOOT_SPEED
        
        # Left shot
        shot = Shot(self.position.x, self.position.y)
        shot.velocity = pygame.Vector2(0, 1).rotate(self.rotation - 15) * PLAYER_SHOOT_SPEED
        
        # Right shot
        shot = Shot(self.position.x, self.position.y)
        shot.velocity = pygame.Vector2(0, 1).rotate(self.rotation + 15) * PLAYER_SHOOT_SPEED
    
    def is_invulnerable(self):
        return self.invulnerable_timer > 0
    
    def respawn(self):
        self.position.x = SCREEN_WIDTH / 2
        self.position.y = SCREEN_HEIGHT / 2
        self.velocity = pygame.Vector2(0, 0)
        self.rotation = 0
        self.invulnerable_timer = PLAYER_INVULNERABILITY_TIME

