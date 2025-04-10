import pygame
import math
from pygame import gfxdraw


class Button:
    """
    Modern, animated button component
    """

    def __init__(self, x, y, width, height, text, action=None):
        """
        Initialize a button

        Args:
            x, y: Position coordinates
            width, height: Button dimensions
            text: Button text
            action: Function to call when clicked
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.action = action
        self.hovered = False

    def update(self, events):
        # Check if the mouse is hovering over the button
        mouse_pos = pygame.mouse.get_pos()
        for event in events:
            if event.type == pygame.MOUSEMOTION:
                mouse_pos = event.pos  # Use event position for testing compatibility
        self.hovered = self.rect.collidepoint(mouse_pos)

        # Check for click events
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.hovered and self.action:
                    self.action()

    def draw(self, surface):
        """
        Draw the button on the given surface with visual feedback for hover state

        Args:
            surface: The pygame surface to draw on
        """
        # Determine colors based on hover state
        bg_color = (80, 180, 80) if self.hovered else (60, 140, 60)
        border_color = (120, 255, 120) if self.hovered else (100, 200, 100)
        text_color = (255, 255, 255)

        # Create button surface with alpha for glow effects
        button_surface = pygame.Surface(
            (self.rect.width, self.rect.height), pygame.SRCALPHA
        )

        # Draw button base
        pygame.draw.rect(
            button_surface,
            bg_color,
            (0, 0, self.rect.width, self.rect.height),
            border_radius=10,
        )

        # Draw border
        pygame.draw.rect(
            button_surface,
            border_color,
            (0, 0, self.rect.width, self.rect.height),
            border_radius=10,
            width=2,
        )

        # Add highlight effect on top
        highlight_height = self.rect.height // 3
        for i in range(highlight_height):
            alpha = 50 - int((i / highlight_height) * 50)
            pygame.draw.rect(
                button_surface,
                (255, 255, 255, alpha),
                (2, 2 + i, self.rect.width - 4, 1),
                border_radius=10,
            )

        # Draw text
        font = pygame.font.SysFont("Arial", 20, bold=True)
        text_surf = font.render(self.text, True, text_color)
        text_pos = (
            self.rect.width // 2 - text_surf.get_width() // 2,
            self.rect.height // 2 - text_surf.get_height() // 2,
        )
        button_surface.blit(text_surf, text_pos)

        # Draw button on target surface
        surface.blit(button_surface, (self.rect.x, self.rect.y))

        # Add glow effect if hovered
        if self.hovered:
            glow_surf = pygame.Surface(
                (self.rect.width + 10, self.rect.height + 10), pygame.SRCALPHA
            )
            for i in range(5):
                alpha = 10 - i * 2
                pygame.draw.rect(
                    glow_surf,
                    (120, 255, 120, alpha),
                    (5 - i, 5 - i, self.rect.width + i * 2, self.rect.height + i * 2),
                    border_radius=10 + i,
                )
            surface.blit(glow_surf, (self.rect.x - 5, self.rect.y - 5))


class Panel:
    """
    Semi-transparent panel with rounded corners
    """

    def __init__(self, x, y, width, height, bg_color=(20, 20, 40, 200)):
        """
        Initialize panel

        Args:
            x, y: Position coordinates
            width, height: Panel dimensions
            bg_color: Background color (with alpha)
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.bg_color = bg_color
        self.shadow_offset = 5

    def draw(self, surface):
        """Render the panel with shadow effect"""
        # Draw shadow
        shadow_rect = self.rect.copy()
        shadow_rect.x += self.shadow_offset
        shadow_rect.y += self.shadow_offset
        pygame.draw.rect(
            surface,
            (0, 0, 0, 100),  # Semi-transparent black
            shadow_rect,
            border_radius=15,
        )

        # Draw panel background
        panel_surface = pygame.Surface(
            (self.rect.width, self.rect.height), pygame.SRCALPHA
        )
        pygame.draw.rect(
            panel_surface,
            self.bg_color,
            (0, 0, self.rect.width, self.rect.height),
            border_radius=15,
        )

        # Add subtle gradient highlight at the top
        highlight_height = self.rect.height // 4
        for i in range(highlight_height):
            alpha = 100 - int((i / highlight_height) * 100)
            pygame.draw.rect(
                panel_surface,
                (255, 255, 255, alpha),
                (0, i, self.rect.width, 1),
                border_radius=15,
            )

        # Draw border
        pygame.draw.rect(
            panel_surface,
            (100, 100, 160, 255),
            (0, 0, self.rect.width, self.rect.height),
            border_radius=15,
            width=2,
        )

        surface.blit(panel_surface, (self.rect.x, self.rect.y))


class ScoreDisplay:
    """
    Enhanced score display with animations
    """

    def __init__(self, x, y):
        """
        Initialize score display

        Args:
            x, y: Position coordinates
        """
        self.x = x
        self.y = y
        self.current_displayed_score = 0
        self.target_score = 0
        self.last_score_increase_time = 0
        self.score_change_animation = 0
        self.current_score = 0  # Added for test compatibility
        self.elapsed_time = 0  # Added for test compatibility

    def update(self, score, current_time):
        """
        Update score display with animation

        Args:
            score: New score value
            current_time: Current time in milliseconds
        """
        if score > self.target_score:
            self.target_score = score
            self.current_score = score  # Update the test-compatible property
            self.elapsed_time = current_time  # Store time for test compatibility
            self.last_score_increase_time = current_time
            self.score_change_animation = 1.0

        # Animate score counting up
        if self.current_displayed_score < self.target_score:
            # Speed increases with larger differences
            increment = max(1, (self.target_score - self.current_displayed_score) // 10)
            self.current_displayed_score = min(
                self.target_score, self.current_displayed_score + increment
            )
        # Fade animation
        if self.score_change_animation > 0:
            self.score_change_animation = max(0, self.score_change_animation - 0.05)

    def draw(self, surface, score=None):
        """
        Draw the score display on the surface

        Args:
            surface: The surface to draw on
            score: The current game score to display (optional)
        """
        # Implementation to draw the score
        # Only render if not already handled by the renderer
        if score is None:
            score = self.current_displayed_score

        font = pygame.font.Font(None, 36)
        text = font.render(f"Score: {score}", True, (255, 255, 255))
        surface.blit(text, (self.x, self.y))
