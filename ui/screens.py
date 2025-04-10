import pygame
import sys
import time
import math
from snake_game.core.config import UP, DOWN, LEFT, RIGHT, GRID_SIZE
from ui.components import Button, Panel, ScoreDisplay
from ui.effects import ParticleSystem


class Screen:
    """Base screen class for all game screens"""

    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height

    def handle_events(self, events):
        """Process pygame events"""
        pass

    def update(self, dt):
        """Update screen state"""
        pass

    def render(self, surface):
        """Render the screen"""
        pass


class MenuScreen(Screen):
    """Main menu screen with game options"""

    def __init__(self, screen_width, screen_height, start_game_callback):
        super().__init__(screen_width, screen_height)
        self.start_game_callback = start_game_callback

        # Background animation
        self.bg_offset = 0
        self.particles = ParticleSystem(screen_width, screen_height)

        # Title animation
        self.title_y_offset = 0
        self.title_animation_time = 0

        # Create UI components
        center_x = screen_width // 2
        center_y = screen_height // 2
        button_width = 200
        button_height = 60

        # Create buttons
        self.start_button = Button(
            center_x - button_width // 2,
            center_y + 20,
            button_width,
            button_height,
            "Start Game",
            self.start_game_callback,
        )

        self.quit_button = Button(
            center_x - button_width // 2,
            center_y + 100,
            button_width,
            button_height,
            "Quit",
            sys.exit,
        )

        # Create panels
        self.main_panel = Panel(center_x - 250, center_y - 200, 500, 400)

    def handle_events(self, events):
        """Process pygame events"""
        self.start_button.update(events)
        self.quit_button.update(events)

    def update(self, dt):
        """Update menu animations"""
        self.bg_offset = (self.bg_offset + 0.2 * dt) % 40
        self.particles.update(dt)

        # Animate title
        self.title_animation_time += dt
        self.title_y_offset = 5 * math.sin(self.title_animation_time * 0.002)

    def render(self, surface):
        """Render menu screen"""
        # Fill background with dark color
        surface.fill((5, 5, 30))

        # Draw animated background grid
        for x in range(-40 + int(self.bg_offset), self.screen_width, 40):
            pygame.draw.line(surface, (20, 20, 50), (x, 0), (x, self.screen_height))
        for y in range(-40 + int(self.bg_offset), self.screen_height, 40):
            pygame.draw.line(surface, (20, 20, 50), (0, y), (self.screen_width, y))

        # Draw particles
        self.particles.draw(surface)

        # Draw main panel
        self.main_panel.draw(surface)

        # Draw title
        font_large = pygame.font.SysFont("Arial", 72, bold=True)
        font_subtitle = pygame.font.SysFont("Arial", 24)

        title = font_large.render("SNAKE", True, (100, 255, 100))
        subtitle = font_subtitle.render(
            "A Modern Python Implementation", True, (200, 200, 255)
        )

        title_pos = (
            self.screen_width // 2 - title.get_width() // 2,
            self.main_panel.rect.y + 50 + self.title_y_offset,
        )
        subtitle_pos = (
            self.screen_width // 2 - subtitle.get_width() // 2,
            title_pos[1] + 80,
        )

        # Draw shadow for title
        shadow_title = font_large.render("SNAKE", True, (0, 100, 0))
        surface.blit(shadow_title, (title_pos[0] + 4, title_pos[1] + 4))
        surface.blit(title, title_pos)
        surface.blit(subtitle, subtitle_pos)

        # Draw buttons
        self.start_button.draw(surface)
        self.quit_button.draw(surface)


class GameScreen(Screen):
    """Game screen that handles the actual gameplay"""

    def __init__(
        self, screen_width, screen_height, game, renderer, return_to_menu_callback
    ):
        super().__init__(screen_width, screen_height)
        self.game = game
        self.renderer = renderer
        self.return_to_menu_callback = return_to_menu_callback

        # Initialize UI components
        self.score_display = ScoreDisplay(10, 10)
        self.particles = ParticleSystem(screen_width, screen_height)

        # Game state
        self.paused = False
        self.game_over = False

    def handle_events(self, events):
        """Handle game events"""
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.game.handle_input(UP)
                elif event.key == pygame.K_DOWN:
                    self.game.handle_input(DOWN)
                elif event.key == pygame.K_LEFT:
                    self.game.handle_input(LEFT)
                elif event.key == pygame.K_RIGHT:
                    self.game.handle_input(
                        RIGHT
                    )  # Keep any other key handling you have
                if event.key == pygame.K_p:
                    self.paused = not self.paused
                elif event.key == pygame.K_r and self.game_over:
                    self.game.reset()
                    self.game_over = False
                elif event.key == pygame.K_ESCAPE:
                    self.return_to_menu_callback()

    def update(self, dt):
        """Update game state"""
        if not self.paused and not self.game_over:
            # Update game state
            self.game.update()

            # Check for game over
            if self.game.is_game_over:
                self.game_over = True
                # Add particle effect for game over
                head_pos = self.game.snake.get_head_position()
                self.particles.add_explosion(
                    head_pos[0] + GRID_SIZE // 2,
                    head_pos[1] + GRID_SIZE // 2,
                    color=(255, 50, 50),
                    count=50,
                )

        # Always update particles
        self.particles.update(dt)

    def render(self, surface):
        """Render the game screen"""
        if not self.game:
            return        # Render game elements using the renderer
        # Modified to use a custom method that doesn't render the score
        self.renderer.render_game(surface, self.game)

        # We'll let the score_display handle rendering the score
        self.score_display.draw(surface, self.game.score)
        
        # Render particles (important for game over effects)
        self.particles.draw(surface)

        # Display pause message if the game is paused
        if self.paused:
            font = pygame.font.SysFont("Arial", 48, bold=True)
            paused_text = font.render("PAUSED", True, (255, 255, 255))
            text_rect = paused_text.get_rect(center=(self.screen_width//2, self.screen_height//2))
            
            # Draw semi-transparent overlay
            overlay = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 128))  # semi-transparent black
            surface.blit(overlay, (0, 0))
            
            # Draw text with shadow
            shadow = font.render("PAUSED", True, (50, 50, 50))
            shadow_rect = shadow.get_rect(center=(self.screen_width//2+2, self.screen_height//2+2))
            surface.blit(shadow, shadow_rect)
            surface.blit(paused_text, text_rect)


class ScreenManager:
    """Manages different screens in the game"""

    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.screens = {}
        self.current_screen = None

    def add_screen(self, name, screen):
        """Add a screen to the manager"""
        self.screens[name] = screen

    def set_current_screen(self, name):
        """Change the current active screen"""
        if name in self.screens:
            self.current_screen = name
        else:
            raise ValueError(f"Screen '{name}' not found")

    def get_current_screen(self):
        """Get the currently active screen object"""
        if self.current_screen and self.current_screen in self.screens:
            return self.screens[self.current_screen]
        return None

    def handle_events(self, events):
        """Pass events to the current screen"""
        screen = self.get_current_screen()
        if screen:
            screen.handle_events(events)

    def update(self, dt):
        """Update the current screen"""
        screen = self.get_current_screen()
        if screen:
            screen.update(dt)

    def render(self, surface):
        """Render the current screen"""
        screen = self.get_current_screen()
        if screen:
            screen.render(surface)
