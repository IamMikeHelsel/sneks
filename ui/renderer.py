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
        # Snake segment assets are now created dynamically based on snake color.
        # Keep food asset
        self.assets["food"] = self._create_food_surface()
        self.snake_segment_cache = {} # Cache for snake segments by color

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
        self, width, height, base_color, edge_color, corner_radius_factor=0.5
    ):
        """Create a rectangle with smooth edges and gradient fill"""
        surf = pygame.Surface((width, height), pygame.SRCALPHA)
        rect = pygame.Rect(0, 0, width, height)
        corner_radius = int(min(width, height) * corner_radius_factor)

        # Draw rounded rectangle with anti-aliasing
        pygame.draw.rect(surf, base_color, rect, border_radius=corner_radius)

        # Add subtle inner gradient / edge highlight
        # For simplicity, let's draw a slightly smaller, darker rect for the edge effect
        # or use the provided edge_color for an outline effect.
        # A true gradient as before might be too complex if edge_color is just a single color.
        # Let's try a border highlight approach.
        pygame.draw.rect(
            surf,
            edge_color,
            rect,
            border_radius=corner_radius,
            width=max(1,int(width/10)) # Border width
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

    def _get_or_create_snake_segment_surface(self, color_tuple, segment_type="body"):
        """ Gets a snake segment surface from cache or creates and caches it. """
        if (color_tuple, segment_type) in self.snake_segment_cache:
            return self.snake_segment_cache[(color_tuple, segment_type)]

        base_color = color_tuple
        # Make edge color slightly darker for depth
        edge_color = tuple(max(0, c - 40) for c in base_color[:3]) 
        
        # Make head slightly lighter or different
        if segment_type == "head":
            head_base_color = tuple(min(255, c + 30) for c in base_color[:3])
            head_edge_color = tuple(max(0, c - 20) for c in head_base_color[:3])
            surface = self._create_smooth_rect(GRID_SIZE, GRID_SIZE, head_base_color, head_edge_color, 0.7)
        else: # body
            surface = self._create_smooth_rect(GRID_SIZE, GRID_SIZE, base_color, edge_color, 0.7)
        
        self.snake_segment_cache[(color_tuple, segment_type)] = surface
        return surface

    def render_background(self, screen):
        """Render the background grid"""
        screen.blit(self.background, (0, 0))

    def render_snakes(self, screen, snakes_dict):
        """
        Render all snakes with visual enhancements using their assigned colors.

        Args:
            screen: Pygame surface to draw on
            snakes_dict: Dictionary of snake objects {player_id: snake_obj}
        """
        if not snakes_dict:
            return

        for player_id, snake_obj in snakes_dict.items():
            if not snake_obj or not hasattr(snake_obj, 'body') or not hasattr(snake_obj, 'color'):
                continue # Skip if snake object is malformed or lacks color

            snake_color_tuple = snake_obj.color 
            
            # Render body segments (in reverse so head renders on top)
            for i, segment_pos in enumerate(reversed(snake_obj.body)):
                is_head = (i == len(snake_obj.body) - 1)
                segment_type = "head" if is_head else "body"
                
                segment_surface = self._get_or_create_snake_segment_surface(snake_color_tuple, segment_type)
                screen.blit(segment_surface, segment_pos)


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
        if hasattr(game, 'snakes'): # Multiplayer game has game.snakes dict
            self.render_snakes(screen, game.snakes)
        elif hasattr(game, 'snake'): # Single player game might have game.snake
             # Adapt for single snake if necessary, or ensure game.snakes is always used
             # For now, assuming render_snakes can handle a dict with one snake
             self.render_snakes(screen, {"player1": game.snake} if game.snake else {})
        self.render_food(screen, game.food)
        self.render_score(screen, game.score)

        if game.is_game_over:
            self.render_game_over(screen)

        # Return filled surface
        return screen

    def render_game(self, surface, game):
        """
        Render the complete game state including snakes and food

        Args:
            surface: The surface to draw on
            game: The game state to render (should have game.snakes, game.food, game.score, game.is_game_over)
        """
        # First render the background
        self.render_background(surface)

        # Render the snakes
        if hasattr(game, 'snakes'):
             self.render_snakes(surface, game.snakes)
        elif hasattr(game, 'snake'): # Backwards compatibility or single player mode
             self.render_snakes(surface, {"player1": game.snake} if game.snake else {})


        # Render food
        self.render_food(surface, game.food)

        # We'll skip score rendering here since it's handled by the ScoreDisplay component
        # Comment out or remove: self.render_score(surface, game.score)

        # If game is over, render game over screen
        if game.is_game_over:
            self.render_game_over(surface)
