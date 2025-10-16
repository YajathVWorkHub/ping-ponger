import pygame
from .paddle import Paddle
from .ball import Ball

# Game Engine
WHITE = (255, 255, 255)

class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.paddle_width = 10
        self.paddle_height = 100

        self.player = Paddle(10, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ai = Paddle(width - 20, height // 2 - 50, self.paddle_width, self.paddle_height)
        
        # Initialize sound attributes before loading
        self.score_sound = None
        self.paddle_sound = None 

        self.player_score = 0
        self.ai_score = 0
        self.font = pygame.font.SysFont("Arial", 30)
        self.game_over = False
        self.winning_score = 5

        # Load sounds, setting attributes
        try:
            self.score_sound = pygame.mixer.Sound('score.mp3')
            self.paddle_sound = pygame.mixer.Sound('paddle_hit.mp3')
        except pygame.error as e:
            print(f"Could not load sound: {e}. Check if files are present and correct format.")
            # If loading fails, attributes remain None
            
        self.ball = Ball(width // 2, height // 2, 7, 7, width, height, self.paddle_sound)

    # --- New Methods for Task 3 ---
    def set_winning_score(self, score):
        self.winning_score = score

    def reset_game(self):
        # Reset scores
        self.player_score = 0
        self.ai_score = 0
        # Reset ball position and direction
        self.ball.reset_full() # Will need to add reset_full to ball.py
        # Reset game state
        self.game_over = False
        # Center paddles
        self.player.y = self.height // 2 - self.paddle_height // 2
        self.ai.y = self.height // 2 - self.paddle_height // 2
    # -----------------------------

    def handle_input(self):
        keys = pygame.key.get_pressed()
        
        # Player control input
        if not self.game_over:
            if keys[pygame.K_w]:
                self.player.move(-10, self.height)
            if keys[pygame.K_s]:
                self.player.move(10, self.height)


    def update(self):
        if self.game_over:
            return
            
        self.ball.move()
        self.ball.check_collision(self.player, self.ai)

        if self.ball.x <= 0:
            self.ai_score += 1
            self.ball.reset()
            if self.score_sound:
                self.score_sound.play()
        elif self.ball.x >= self.width:
            self.player_score += 1
            self.ball.reset()
            if self.score_sound:
                self.score_sound.play()

        self.ai.auto_track(self.ball, self.height)
        
        # Check for game over condition (using self.winning_score)
        if self.player_score >= self.winning_score or self.ai_score >= self.winning_score:
            self.game_over = True

    def render(self, screen):
        # ... (Draw game elements: paddles, ball, center line) ...
        pygame.draw.rect(screen, WHITE, self.player.rect())
        pygame.draw.rect(screen, WHITE, self.ai.rect())
        pygame.draw.ellipse(screen, WHITE, self.ball.rect())
        pygame.draw.aaline(screen, WHITE, (self.width//2, 0), (self.width//2, self.height))

        # Draw score
        player_text = self.font.render(str(self.player_score), True, WHITE)
        ai_text = self.font.render(str(self.ai_score), True, WHITE)
        screen.blit(player_text, (self.width//4, 20))
        screen.blit(ai_text, (self.width * 3//4, 20))
        
        # Draw game over message and options
        if self.game_over:
            winner = "Player" if self.player_score >= self.winning_score else "AI"
            game_over_text = self.font.render(f"{winner} Wins! (Best of {self.winning_score})", True, WHITE)
            text_rect = game_over_text.get_rect(center=(self.width // 2, self.height // 2 - 50))
            
            replay_text_1 = self.font.render("Play Again:", True, WHITE)
            replay_text_2 = self.font.render("3 (Bo3), 5 (Bo5), 7 (Bo7) or ESC to Exit", True, WHITE)
            
            text_rect_2 = replay_text_1.get_rect(center=(self.width // 2, self.height // 2 + 10))
            text_rect_3 = replay_text_2.get_rect(center=(self.width // 2, self.height // 2 + 50))

            screen.blit(game_over_text, text_rect)
            screen.blit(replay_text_1, text_rect_2)
            screen.blit(replay_text_2, text_rect_3)
