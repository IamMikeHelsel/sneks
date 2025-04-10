import pygame
import sys
from snake_game.core.game import Game
from snake_game.core.config import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    GRID_SIZE,
    FPS,
    BLACK,
    WHITE,
    GREEN,
    RED,
    BLUE,
    UP,
    DOWN,
    LEFT,
    RIGHT,
)


def main():
    """
    Main entry point for the Snake Game
    """
    # Initialize Pygame
    pygame.init()
    pygame.display.set_caption("Python Snake Game")

    # Create screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    # Create clock for controlling game speed
    clock = pygame.time.Clock()

    # Create game instance
    game = Game(SCREEN_WIDTH, SCREEN_HEIGHT)

    # Font for displaying score and game over
    font = pygame.font.SysFont(None, 36)

    # Main game loop
    while True:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                # Key mapping
                if event.key == pygame.K_UP:
                    game.handle_input(UP)
                elif event.key == pygame.K_DOWN:
                    game.handle_input(DOWN)
                elif event.key == pygame.K_LEFT:
                    game.handle_input(LEFT)
                elif event.key == pygame.K_RIGHT:
                    game.handle_input(RIGHT)
                elif event.key == pygame.K_r and game.is_game_over:
                    game.reset()

        # Update game state (if game is not over)
        if not game.is_game_over:
            game.update()

        # Draw everything
        screen.fill(BLACK)  # Clear screen

        # Draw grid (optional)
        for x in range(0, SCREEN_WIDTH, GRID_SIZE):
            pygame.draw.line(screen, (50, 50, 50), (x, 0), (x, SCREEN_HEIGHT))
        for y in range(0, SCREEN_HEIGHT, GRID_SIZE):
            pygame.draw.line(screen, (50, 50, 50), (0, y), (SCREEN_WIDTH, y))

        # Draw snake
        for segment in game.snake.body:
            pygame.draw.rect(
                screen, GREEN, pygame.Rect(segment[0], segment[1], GRID_SIZE, GRID_SIZE)
            )

        # Draw food
        food_rect = pygame.Rect(game.food.x, game.food.y, GRID_SIZE, GRID_SIZE)
        pygame.draw.rect(screen, RED, food_rect)

        # Draw score
        score_text = font.render(f"Score: {game.score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        # Draw game over message if game is over
        if game.is_game_over:
            game_over_text = font.render("Game Over! Press 'R' to restart", True, WHITE)
            text_rect = game_over_text.get_rect(
                center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
            )
            screen.blit(game_over_text, text_rect)

        # Update display
        pygame.display.flip()

        # Control game speed
        clock.tick(FPS)


if __name__ == "__main__":
    main()
