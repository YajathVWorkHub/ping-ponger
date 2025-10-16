# ball.py
import pygame
import random

class Ball:
    def __init__(self, x, y, width, height, screen_width, screen_height, paddle_sound=None):
        self.original_x = x
        self.original_y = y
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.velocity_x = random.choice([-5, 5])
        self.velocity_y = random.choice([-3, 3])

        self.paddle_sound = paddle_sound

        try:
            self.wall_sound = pygame.mixer.Sound('wall_bounce.mp3')
        except pygame.error as e:
            print(f"Could not load wall sound: {e}")
            self.wall_sound = None

    def move(self):
        self.x += self.velocity_x
        self.y += self.velocity_y

        if self.y <= 0 or self.y + self.height >= self.screen_height:
            self.velocity_y *= -1
            if self.wall_sound:
                self.wall_sound.play()

    def check_collision(self, player, ai):
        ball_rect = self.rect()

        collision_detected = False

        # Check collision with player paddle (left side)
        if self.velocity_x < 0 and ball_rect.colliderect(player.rect()):
            self.velocity_x *= -1
            self.x = player.x + player.width
            collision_detected = True
            
        # Check collision with AI paddle (right side)
        elif self.velocity_x > 0 and ball_rect.colliderect(ai.rect()):
            self.velocity_x *= -1
            self.x = ai.x - self.width
            collision_detected = True
        
        # PLAY PADDLE HIT SOUND
        if collision_detected and self.paddle_sound:
            self.paddle_sound.play()

    def reset(self):
        # Used after a score
        self.x = self.original_x
        self.y = self.original_y
        self.velocity_x *= -1
        self.velocity_y = random.choice([-3, 3])

    def reset_full(self):
        self.x = self.original_x
        self.y = self.original_y
        self.velocity_x = random.choice([-5, 5])
        self.velocity_y = random.choice([-3, 3])
    
    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)
