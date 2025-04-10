import unittest
import pygame
import sys
from unittest.mock import MagicMock, patch

# Add the parent directory to sys.path to import the required modules
sys.path.append("c:\\Dev\\clinetest2")

from snake_game.core.game import Game
from snake_game.core.config import SCREEN_WIDTH, SCREEN_HEIGHT
from ui.renderer import SnakeRenderer
from ui.screens import MenuScreen, GameScreen, ScreenManager


class TestScreenManager(unittest.TestCase):
    """Tests for the ScreenManager class"""

    def setUp(self):
        pygame.init()
        self.screen_manager = ScreenManager(SCREEN_WIDTH, SCREEN_HEIGHT)

    def tearDown(self):
        pygame.quit()

    def test_add_and_set_screen(self):
        """Test adding screens and setting the current screen"""
        # Create mock screens
        mock_menu = MagicMock()
        mock_game = MagicMock()

        # Add screens to manager
        self.screen_manager.add_screen("menu", mock_menu)
        self.screen_manager.add_screen("game", mock_game)

        # Test setting current screen
        self.screen_manager.set_current_screen("menu")
        self.assertEqual(self.screen_manager.current_screen, "menu")

        self.screen_manager.set_current_screen("game")
        self.assertEqual(self.screen_manager.current_screen, "game")

    def test_invalid_screen(self):
        """Test setting an invalid screen name"""
        with self.assertRaises(ValueError):
            self.screen_manager.set_current_screen("nonexistent")


class TestGameScreen(unittest.TestCase):
    """Tests for the GameScreen class"""

    def setUp(self):
        pygame.init()
        self.game = Game(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.renderer = SnakeRenderer(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.return_to_menu = MagicMock()
        self.game_screen = GameScreen(
            SCREEN_WIDTH, SCREEN_HEIGHT, self.game, self.renderer, self.return_to_menu
        )

    def tearDown(self):
        pygame.quit()

    def test_game_reset(self):
        """Test that game can be reset"""
        # Simulate game over
        self.game.is_game_over = True
        self.game.score = 100

        # Reset game
        self.game.reset()

        # Check game state is reset
        self.assertFalse(self.game.is_game_over)
        self.assertEqual(self.game.score, 0)


class TestMenuScreen(unittest.TestCase):
    """Tests for the MenuScreen class"""

    def setUp(self):
        pygame.init()
        self.start_game = MagicMock()
        self.open_options = MagicMock()
        self.menu_screen = MenuScreen(
            SCREEN_WIDTH, SCREEN_HEIGHT, self.start_game, self.open_options
        )

    def tearDown(self):
        pygame.quit()

    def test_menu_initialization(self):
        """Test that menu initializes correctly"""
        self.assertIsNotNone(self.menu_screen.particles)
        self.assertEqual(self.menu_screen.screen_width, SCREEN_WIDTH)
        self.assertEqual(self.menu_screen.screen_height, SCREEN_HEIGHT)


if __name__ == "__main__":
    unittest.main()
