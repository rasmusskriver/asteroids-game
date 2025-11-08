import random
import sys

import pygame

from asteroid import Asteroid
from asteroidfield import AsteroidField
from constants import *
from gamestate import GameState
from logger import log_event, log_state
from particle import Particle
from player import Player
from powerup import PowerUp
from shot import Shot
from starfield import Starfield


def main():
    pygame.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Asteroids - Enhanced Edition")
    clock = pygame.time.Clock()

    # Create sprite groups
    drawable = pygame.sprite.Group()
    updatable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    powerups = pygame.sprite.Group()
    particles = pygame.sprite.Group()

    # Set up containers
    Asteroid.containers = (asteroids, updatable, drawable)
    Shot.containers = (shots, updatable, drawable)
    PowerUp.containers = (powerups, updatable, drawable)
    Particle.containers = (particles, updatable, drawable)

    # Initialize game state
    game_state = GameState()
    game_state.init_fonts()  # Initialize fonts after pygame.init()

    # Create starfield background
    starfield = Starfield(150)

    AsteroidField.containers = updatable
    asteroidfield = AsteroidField(game_state)

    Player.containers = (drawable, updatable)
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, game_state)

    dt = 0

    while True:
        log_state()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_state.paused = not game_state.paused
                if event.key == pygame.K_r and game_state.game_over:
                    # Restart game
                    return main()

        # Don't update game if paused or game over
        if game_state.paused:
            screen.fill("black")
            starfield.draw(screen)
            for obj in drawable:
                obj.draw(screen)
            game_state.draw_hud(screen)
            game_state.draw_pause(screen)
            pygame.display.flip()
            dt = clock.tick(60) / 1000
            continue

        if game_state.game_over:
            screen.fill("black")
            starfield.draw(screen)
            game_state.draw_hud(screen)
            game_state.draw_game_over(screen)
            pygame.display.flip()
            dt = clock.tick(60) / 1000
            continue

        # Update game state
        game_state.update(dt)

        # Check for level up
        if game_state.check_level_up():
            log_event("level_up")

        # Apply screen shake
        screen_offset = pygame.Vector2(0, 0)
        if game_state.screen_shake > 0:
            screen_offset.x = random.uniform(-10, 10)
            screen_offset.y = random.uniform(-10, 10)

        screen.fill("black")
        starfield.draw(screen)

        # Create temporary surface for shake effect
        if game_state.screen_shake > 0:
            temp_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            temp_surface.fill("black")
            starfield.draw(temp_surface)
            for obj in drawable:
                obj.draw(temp_surface)
            screen.blit(temp_surface, screen_offset)
        else:
            for obj in drawable:
                obj.draw(screen)

        # Check collisions with asteroids
        for obj in asteroids:
            # Player collision
            if obj.check_collision(player) and not player.is_invulnerable():
                if not game_state.has_shield():
                    log_event("player_hit")
                    game_state.lose_life()

                    # Create explosion particles
                    for _ in range(PARTICLE_COUNT):
                        Particle(player.position.x, player.position.y, "orange")

                    if game_state.lives > 0:
                        player.respawn()
                else:
                    # Shield absorbed hit, destroy asteroid without damage
                    log_event("shield_blocked")
                    score = obj.get_score_value()
                    game_state.add_score(score)

                    # Create particles
                    for _ in range(PARTICLE_COUNT // 2):
                        Particle(obj.position.x, obj.position.y, "cyan")

                    obj.split()

            # Shot collision
            for shot in shots:
                if obj.check_collision(shot):
                    log_event("asteroid_shot")
                    shot.kill()

                    # Add score
                    score = obj.get_score_value()
                    game_state.add_score(score)

                    # Create explosion particles
                    for _ in range(PARTICLE_COUNT // 2):
                        Particle(obj.position.x, obj.position.y, "orange")

                    # Chance to spawn power-up
                    if random.random() < POWERUP_SPAWN_CHANCE:
                        PowerUp(obj.position.x, obj.position.y)

                    obj.split()

        # Check power-up collection
        for powerup in powerups:
            if powerup.check_collision(player):
                log_event(f"powerup_{powerup.type}")
                game_state.activate_powerup(powerup.type)

                # Create particles
                for _ in range(PARTICLE_COUNT // 2):
                    Particle(powerup.position.x, powerup.position.y, PowerUp.COLORS[powerup.type])

                powerup.kill()

        updatable.update(dt)

        # Draw HUD
        game_state.draw_hud(screen)

        pygame.display.flip()

        # limit the framerate to 60 FPS
        dt = clock.tick(60) / 1000


if __name__ == "__main__":
    main()
