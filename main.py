# main.py
import pygame
from game.game_engine import GameEngine

# Initialize pygame/Start application
pygame.init()
pygame.mixer.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ping Pong - Pygame Version")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Clock
clock = pygame.time.Clock()
FPS = 60

# Game loop
engine = GameEngine(WIDTH, HEIGHT)

def main():
    running = True
    while running:
        SCREEN.fill(BLACK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # --- New Logic for Task 3: Replay Input ---
            if engine.game_over and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False # Exit the game
                elif event.key == pygame.K_3:
                    engine.set_winning_score(3)
                    engine.reset_game()
                elif event.key == pygame.K_5:
                    engine.set_winning_score(5)
                    engine.reset_game()
                elif event.key == pygame.K_7:
                    engine.set_winning_score(7)
                    engine.reset_game()
            # -------------------------------------------

        engine.handle_input()
        engine.update()
        engine.render(SCREEN)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
