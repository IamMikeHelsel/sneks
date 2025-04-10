import pygame
import sys
import time
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
from ui.renderer import SnakeRenderer
from ui.screens import MenuScreen, GameScreen, ScreenManager
from ui.effects import ParticleSystem, AnimationManager


def main():
    """
    Main entry point for the Snake Game
    """
    # Initialize Pygame with better graphics options
    pygame.init()
    pygame.display.set_caption("Modern Snake Game")

    # Set icon
    icon = pygame.Surface((32, 32))
    icon.fill((20, 20, 40))
    pygame.draw.rect(icon, GREEN, (8, 8, 16, 16), border_radius=4)
    pygame.display.set_icon(icon)

    # Create screen with modern rendering flags
    screen = pygame.display.set_mode(
        (SCREEN_WIDTH, SCREEN_HEIGHT), pygame.HWSURFACE | pygame.DOUBLEBUF
    )

    # Create clock for controlling game speed and timing
    clock = pygame.time.Clock()

    # Create enhanced renderer
    renderer = SnakeRenderer(SCREEN_WIDTH, SCREEN_HEIGHT)

    # Create game instance
    game = Game(SCREEN_WIDTH, SCREEN_HEIGHT)

    # Create screen manager for handling different screens
    screen_manager = ScreenManager(SCREEN_WIDTH, SCREEN_HEIGHT)

    # Function to start the game from menu
    def start_game():
        screen_manager.set_current_screen("game")

    # Function to return to menu from game
    def return_to_menu():
        screen_manager.set_current_screen("menu")
        game.reset()  # Reset game state

    # Create screens
    menu_screen = MenuScreen(SCREEN_WIDTH, SCREEN_HEIGHT, start_game)
    game_screen = GameScreen(
        SCREEN_WIDTH, SCREEN_HEIGHT, game, renderer, return_to_menu
    )

    # Add screens to manager
    screen_manager.add_screen("menu", menu_screen)
    screen_manager.add_screen("game", game_screen)

    # Start with menu screen
    screen_manager.set_current_screen("menu")

    # Track time for smooth animations
    last_time = time.time()

    # Main game loop
    while True:
        # Calculate delta time for smooth animations
        current_time = time.time()
        dt = (current_time - last_time) * 1000.0  # Convert to milliseconds
        last_time = current_time

        # Cap dt to prevent physics issues on lag
        dt = min(dt, 50)

        # Get events once per frame
        events = pygame.event.get()

        # Check for quit
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Update current screen
        screen_manager.handle_events(events)
        screen_manager.update(dt)

        # Render current screen to the display
        screen.fill((5, 5, 30))  # Clear screen with dark background
        screen_manager.render(screen)

        # Update display with hardware acceleration if available
        pygame.display.flip()

        # Control game speed with consistent timing
        clock.tick(FPS)


if __name__ == "__main__":
    main()
