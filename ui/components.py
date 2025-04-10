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
        self.hover = False
        self.pressed = False

        # Animation state
        self.animation_progress = 0
        self.ripple_center = None
        self.ripple_radius = 0

    def update(self, events):
        """Update button state based on events"""
        mouse_pos = pygame.mouse.get_pos()
        self.hover = self.rect.collidepoint(mouse_pos)

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.hover:
                    self.pressed = True
                    self.ripple_center = (
                        mouse_pos[0] - self.rect.x,
                        mouse_pos[1] - self.rect.y,
                    )
                    self.ripple_radius = 0

            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if self.hover and self.pressed and self.action:
                    self.action()
                self.pressed = False

        # Update animations
        if self.ripple_center:
            self.ripple_radius += 5
            if self.ripple_radius > self.rect.width * 1.5:
                self.ripple_radius = 0
                self.ripple_center = None

        # Smooth hover animation
        if self.hover:
            self.animation_progress = min(1.0, self.animation_progress + 0.1)
        else:
            self.animation_progress = max(0.0, self.animation_progress - 0.1)

    def draw(self, surface):
        """Render the button"""
        # Base colors
        bg_color = (30, 30, 60)
        hover_color = (50, 50, 100)
        text_color = (220, 220, 255)
        border_color = (100, 100, 200)

        # Create button surface with alpha for effects
        button_surface = pygame.Surface(
            (self.rect.width, self.rect.height), pygame.SRCALPHA
        )

        # Interpolate color based on hover
        current_color = [
            bg_color[0] + (hover_color[0] - bg_color[0]) * self.animation_progress,
            bg_color[1] + (hover_color[1] - bg_color[1]) * self.animation_progress,
            bg_color[2] + (hover_color[2] - bg_color[2]) * self.animation_progress,
        ]

        # Draw button background with rounded corners
        pygame.draw.rect(
            button_surface,
            current_color,
            (0, 0, self.rect.width, self.rect.height),
            border_radius=10,
        )

        # Draw ripple effect when pressed
        if self.ripple_center and self.ripple_radius > 0:
            pygame.draw.circle(
                button_surface,
                (255, 255, 255, 50),  # Semi-transparent white
                self.ripple_center,
                self.ripple_radius,
            )

        # Draw border
        border_width = 2
        pygame.draw.rect(
            button_surface,
            border_color,
            (0, 0, self.rect.width, self.rect.height),
            border_radius=10,
            width=border_width,
        )

        # Draw text
        font = pygame.font.SysFont("Arial", 24)
        text_surf = font.render(self.text, True, text_color)
        text_rect = text_surf.get_rect(
            center=(self.rect.width // 2, self.rect.height // 2)
        )
        button_surface.blit(text_surf, text_rect)

        # Draw to main surface
        surface.blit(button_surface, (self.rect.x, self.rect.y))


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

    def update(self, score, current_time):
        """
        Update score display with animation

        Args:
            score: New score value
            current_time: Current time in milliseconds
        """
        if score > self.target_score:
            self.target_score = score
            self.last_score_increase_time = current_time
            self.score_change_animation = 1.0

        # Animate score counting up
        if self.current_displayed_score < self.target_score:
            # Speed increases with larger differences
            increment = max(1, (self.target_score - self.current_displayed_score) // 10)
            self.current_displayed_score = min(
                self.target_score, self.current_displayed_score + increment
            )        # Fade animation
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
