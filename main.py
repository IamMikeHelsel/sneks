import pygame
import sys
import time
from snake_game.core.game import Game
from snake_game.core.config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, GREEN
from ui.renderer import SnakeRenderer
from ui.screens import MenuScreen, GameScreen, ScreenManager


def main():
    """
    Main entry point for the Snake Game
    """
    # Initialize Pygame with better graphics options
    pygame.init()
    pygame.display.set_caption("sneks")

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
    screen_manager = ScreenManager(
        SCREEN_WIDTH, SCREEN_HEIGHT
    )  # Function to start the game from menu

    def start_game():
        # Set GPS for classic mode if needed
        if selected_mode["mode"] == "classic":
            game_screen.set_gps(classic_gps["value"])
        else:
            game_screen.set_gps(FPS)
        screen_manager.set_current_screen("game")
        nonlocal game_accumulator
        game_accumulator = 0.0

    # Function to return to menu from game
    def return_to_menu():
        screen_manager.set_current_screen("menu")
        game.reset()  # Reset game state

    # Placeholder function for options menu (not implemented yet)
    def open_options():
        pass  # This can be implemented later when options menu is added

    # Track selected mode
    selected_mode = {"mode": "normal"}
    classic_gps = {"value": 10}

    def set_mode(mode):
        selected_mode["mode"] = mode
        if mode == "classic":
            import random
            classic_gps["value"] = random.randint(8, 12)
        else:
            classic_gps["value"] = FPS

    # Create screens
    menu_screen = MenuScreen(
        SCREEN_WIDTH, SCREEN_HEIGHT, start_game, open_options, set_mode_callback=set_mode
    )
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
    game_accumulator = 0.0

    # Main game loop
    while True:
        # Calculate delta time for smooth animations
        current_time = time.time()
        dt = (current_time - last_time)
        last_time = current_time

        # Cap dt to prevent physics issues on lag
        dt = min(dt, 0.05)

        # Get events once per frame
        events = pygame.event.get()

        # Check for quit
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Update current screen events
        screen_manager.handle_events(events)

        # --- Game logic update at GPS (classic mode) ---
        if screen_manager.current_screen == "game":
            gps = classic_gps["value"] if selected_mode["mode"] == "classic" else FPS
            game_step = 1.0 / gps
            game_accumulator += dt
            while game_accumulator >= game_step:
                screen_manager.update(game_step * 1000.0)  # dt in ms for update()
                game_accumulator -= game_step
        else:
            screen_manager.update(dt * 1000.0)

        # Render current screen to the display
        screen.fill((20, 20, 40))  # Clear screen with dark background
        screen_manager.render(screen)

        # Update display with hardware acceleration if available
        pygame.display.flip()

        # Control render speed (locked to 60 FPS)
        clock.tick(60)


if __name__ == "__main__":
    main()
