import pygame


class GameState:
    def __init__(self):
        self.score = 0
        self.high_score = self.load_high_score()
        self.lives = 3
        self.level = 1
        self.paused = False
        self.game_over = False
        self.screen_shake = 0
        
        # Power-up timers
        self.rapid_fire_timer = 0
        self.shield_timer = 0
        self.triple_shot_timer = 0
        
        # Cache fonts (will be initialized later)
        self.font_small = None
        self.font_medium = None
        self.font_large = None
    
    def init_fonts(self):
        """Initialize fonts after pygame is ready"""
        if self.font_small is None:
            self.font_small = pygame.font.Font(None, 36)
            self.font_medium = pygame.font.Font(None, 48)
            self.font_large = pygame.font.Font(None, 72)

    def load_high_score(self):
        try:
            with open("high_score.txt", "r") as f:
                return int(f.read().strip())
        except:
            return 0

    def save_high_score(self):
        if self.score > self.high_score:
            self.high_score = self.score
            try:
                with open("high_score.txt", "w") as f:
                    f.write(str(self.high_score))
            except:
                pass

    def add_score(self, points):
        self.score += points
        if self.score > self.high_score:
            self.high_score = self.score

    def check_level_up(self):
        from constants import LEVEL_SCORE_THRESHOLD
        new_level = 1 + (self.score // LEVEL_SCORE_THRESHOLD)
        if new_level > self.level:
            self.level = new_level
            return True
        return False

    def lose_life(self):
        self.lives -= 1
        self.screen_shake = 0.5  # Half second of screen shake
        if self.lives <= 0:
            self.game_over = True
            self.save_high_score()

    def has_shield(self):
        return self.shield_timer > 0

    def has_rapid_fire(self):
        return self.rapid_fire_timer > 0

    def has_triple_shot(self):
        return self.triple_shot_timer > 0

    def update(self, dt):
        self.rapid_fire_timer = max(0, self.rapid_fire_timer - dt)
        self.shield_timer = max(0, self.shield_timer - dt)
        self.triple_shot_timer = max(0, self.triple_shot_timer - dt)
        self.screen_shake = max(0, self.screen_shake - dt)

    def activate_powerup(self, powerup_type):
        from constants import POWERUP_DURATION
        if powerup_type == "rapid_fire":
            self.rapid_fire_timer = POWERUP_DURATION
        elif powerup_type == "shield":
            self.shield_timer = POWERUP_DURATION
        elif powerup_type == "triple_shot":
            self.triple_shot_timer = POWERUP_DURATION

    def draw_hud(self, screen):
        self.init_fonts()
        
        # Score
        score_text = self.font_small.render(f"Score: {self.score}", True, "white")
        screen.blit(score_text, (10, 10))
        
        # High score
        high_score_text = self.font_small.render(f"High: {self.high_score}", True, "yellow")
        screen.blit(high_score_text, (10, 50))
        
        # Lives
        lives_text = self.font_small.render(f"Lives: {self.lives}", True, "red")
        screen.blit(lives_text, (10, 90))
        
        # Level
        level_text = self.font_small.render(f"Level: {self.level}", True, "cyan")
        screen.blit(level_text, (10, 130))
        
        # Power-ups
        y_offset = 170
        if self.has_rapid_fire():
            powerup_text = self.font_small.render(f"Rapid Fire: {self.rapid_fire_timer:.1f}s", True, "yellow")
            screen.blit(powerup_text, (10, y_offset))
            y_offset += 40
        if self.has_shield():
            powerup_text = self.font_small.render(f"Shield: {self.shield_timer:.1f}s", True, "cyan")
            screen.blit(powerup_text, (10, y_offset))
            y_offset += 40
        if self.has_triple_shot():
            powerup_text = self.font_small.render(f"Triple Shot: {self.triple_shot_timer:.1f}s", True, "magenta")
            screen.blit(powerup_text, (10, y_offset))

    def draw_game_over(self, screen):
        self.init_fonts()
        from constants import SCREEN_WIDTH, SCREEN_HEIGHT
        
        game_over_text = self.font_large.render("GAME OVER", True, "red")
        screen.blit(game_over_text, 
                   (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, 
                    SCREEN_HEIGHT // 2 - 100))
        
        score_text = self.font_medium.render(f"Final Score: {self.score}", True, "white")
        screen.blit(score_text, 
                   (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 
                    SCREEN_HEIGHT // 2))
        
        if self.score >= self.high_score:
            high_text = self.font_medium.render("NEW HIGH SCORE!", True, "yellow")
            screen.blit(high_text, 
                       (SCREEN_WIDTH // 2 - high_text.get_width() // 2, 
                        SCREEN_HEIGHT // 2 + 60))
        
        restart_text = self.font_medium.render("Press R to Restart", True, "white")
        screen.blit(restart_text, 
                   (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, 
                    SCREEN_HEIGHT // 2 + 120))

    def draw_pause(self, screen):
        self.init_fonts()
        from constants import SCREEN_WIDTH, SCREEN_HEIGHT
        pause_text = self.font_large.render("PAUSED", True, "white")
        screen.blit(pause_text, 
                   (SCREEN_WIDTH // 2 - pause_text.get_width() // 2, 
                    SCREEN_HEIGHT // 2 - 36))
