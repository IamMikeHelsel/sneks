import pygame
import math
from pygame import gfxdraw
from snake_game.core.config import GRID_SIZE, BLACK, WHITE, GREEN, RED, BLUE


class SnakeRenderer:
    """
    Enhanced renderer for Snake Game with modern visual effects
    """

    def __init__(self, screen_width, screen_height):
        """
        Initialize the renderer

        Args:
            screen_width: Width of the screen
            screen_height: Height of the screen
        """
        self.screen_width = screen_width
        self.screen_height = screen_height

        # Pre-render background grid for better performance
        self.background = self._create_background()

        # Load and cache assets
        self.assets = {}
        self._initialize_assets()

        # Prepare animation variables
        self.animations = {}
        self.food_pulse = 0

    def _initialize_assets(self):
        """Initialize and cache game assets"""
        # Create snake segment assets (head and body with smooth borders)
        self.assets["snake_body"] = self._create_smooth_rect(
            GRID_SIZE, GRID_SIZE, (50, 220, 50), (30, 180, 30), 0.7
        )

        self.assets["snake_head"] = self._create_smooth_rect(
            GRID_SIZE, GRID_SIZE, (70, 255, 70), (40, 220, 40), 0.7
        )

        # Create food asset (circular with glow effect)
        self.assets["food"] = self._create_food_surface()

    def _create_background(self):
        """Create a pre-rendered background grid surface for performance"""
        bg = pygame.Surface((self.screen_width, self.screen_height))
        bg.fill((10, 10, 35))  # Dark blue background

        # Draw subtle grid lines
        for x in range(0, self.screen_width, GRID_SIZE):
            pygame.draw.line(bg, (30, 30, 60), (x, 0), (x, self.screen_height))
        for y in range(0, self.screen_height, GRID_SIZE):
            pygame.draw.line(bg, (30, 30, 60), (0, y), (self.screen_width, y))

        return bg

    def _create_smooth_rect(
        self, width, height, color, edge_color, corner_radius_factor=0.5
    ):
        """Create a rectangle with smooth edges and gradient fill"""
        surf = pygame.Surface((width, height), pygame.SRCALPHA)
        rect = pygame.Rect(0, 0, width, height)
        corner_radius = int(min(width, height) * corner_radius_factor)

        # Draw rounded rectangle with anti-aliasing
        pygame.draw.rect(surf, color, rect, border_radius=corner_radius)

        # Add subtle inner gradient
        for i in range(corner_radius):
            alpha = 255 - int(255 * i / corner_radius)
            pygame.draw.rect(
                surf,
                (*edge_color, alpha),
                rect.inflate(-2 * i, -2 * i),
                border_radius=corner_radius - i,
            )

        return surf

    def _create_food_surface(self):
        """Create food with glowing effect"""
        size = GRID_SIZE
        surf = pygame.Surface((size, size), pygame.SRCALPHA)
        center = size // 2

        # Draw base circular shape
        pygame.draw.circle(surf, (255, 50, 50), (center, center), center - 2)

        # Add highlight
        pygame.draw.circle(surf, (255, 200, 200), (center - 2, center - 2), center // 3)

        return surf

    def _update_animations(self):
        """Update animation states"""
        # Update food pulsing effect
        self.food_pulse = (self.food_pulse + 0.1) % (2 * math.pi)

    def render_background(self, screen):
        """Render the background grid"""
        screen.blit(self.background, (0, 0))

    def render_snake(self, screen, snake):
        """
        Render the snake with visual enhancements

        Args:
            screen: Pygame surface to draw on
            snake: Snake object to render
        """
        # Render body segments (in reverse so head renders on top)
        for i, segment in enumerate(reversed(snake.body)):
            # Head gets special treatment
            if i == len(snake.body) - 1:
                screen.blit(self.assets["snake_head"], segment)
            else:
                screen.blit(self.assets["snake_body"], segment)

    def render_food(self, screen, food):
        """
        Render the food with visual effects

        Args:
            screen: Pygame surface to draw on
            food: Food object to render
        """
        # Apply pulsing effect to food
        scale_factor = 0.9 + 0.1 * math.sin(self.food_pulse)

        # Calculate new dimensions
        original_size = GRID_SIZE
        new_size = int(original_size * scale_factor)
        offset = (original_size - new_size) // 2

        # Scale the food surface
        scaled_food = pygame.transform.scale(self.assets["food"], (new_size, new_size))

        # Draw with centered offset
        screen.blit(scaled_food, (food.x + offset, food.y + offset))

    def render_score(self, screen, score):
        """
        Render the score with enhanced styling

        Args:
            screen: Pygame surface to draw on
            score: Current game score to display
        """
        font = pygame.font.SysFont("Arial", 28, bold=True)

        # Create gradient text effect
        text = font.render(f"Score: {score}", True, (220, 220, 255))

        # Add subtle shadow for depth
        shadow = font.render(f"Score: {score}", True, (20, 20, 40))
        screen.blit(shadow, (12, 12))
        screen.blit(text, (10, 10))

    def render_game_over(self, screen):
        """
        Render game over screen with enhanced styling

        Args:
            screen: Pygame surface to draw on
        """
        # Semi-transparent overlay
        overlay = pygame.Surface(
            (self.screen_width, self.screen_height), pygame.SRCALPHA
        )
        overlay.fill((0, 0, 0, 150))
        screen.blit(overlay, (0, 0))

        # Game over text
        font_large = pygame.font.SysFont("Arial", 64, bold=True)
        font_small = pygame.font.SysFont("Arial", 28)

        game_over = font_large.render("Game Over", True, (255, 50, 50))
        restart_text = font_small.render("Press 'R' to restart", True, (200, 200, 200))

        # Position text in center of screen
        game_over_rect = game_over.get_rect(
            center=(self.screen_width // 2, self.screen_height // 2 - 40)
        )
        restart_rect = restart_text.get_rect(
            center=(self.screen_width // 2, self.screen_height // 2 + 20)
        )

        # Add shadow effect
        shadow_offset = 3
        shadow1 = font_large.render("Game Over", True, (100, 0, 0))
        shadow1_rect = shadow1.get_rect(
            center=(
                self.screen_width // 2 + shadow_offset,
                self.screen_height // 2 - 40 + shadow_offset,
            )
        )

        # Draw elements
        screen.blit(shadow1, shadow1_rect)
        screen.blit(game_over, game_over_rect)
        screen.blit(restart_text, restart_rect)

    def render_frame(self, screen, game):
        """
        Render a complete frame

        Args:
            screen: Pygame surface to draw on
            game: Game object containing game state
        """
        # Update animations
        self._update_animations()

        # Draw all components
        self.render_background(screen)
        self.render_snake(screen, game.snake)
        self.render_food(screen, game.food)
        self.render_score(screen, game.score)

        if game.is_game_over:
            self.render_game_over(screen)

        # Return filled surface
        return screen

    def render_game(self, surface, game):
        """
        Render the complete game state including snake and food

        Args:
            surface: The surface to draw on
            game: The game state to render
        """
        # First render the background
        self.render_background(surface)

        # Render the snake
        self.render_snake(surface, game.snake)

        # Render food
        self.render_food(surface, game.food)

        # We'll skip score rendering here since it's handled by the ScoreDisplay component
        # Comment out or remove: self.render_score(surface, game.score)

        # If game is over, render game over screen
        if game.is_game_over:
            self.render_game_over(surface)
