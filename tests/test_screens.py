import unittest
import pygame
from ui.screens import ScreenManager, Screen, MenuScreen, GameScreen


class MockScreen(Screen):
    def __init__(self, screen_width=800, screen_height=600):
        super().__init__(screen_width, screen_height)
        self.events_handled = False
        self.update_called = False
        self.render_called = False

    def handle_events(self, events):
        self.events_handled = True

    def update(self, dt):
        self.update_called = True

    def render(self, surface):
        self.render_called = True


class TestScreenManager(unittest.TestCase):
    def setUp(self):
        pygame.init()
        self.screen_manager = ScreenManager(800, 600)
        self.test_surface = pygame.Surface((800, 600))

    def tearDown(self):
        pygame.quit()

    def test_screen_manager_initialization(self):
        self.assertEqual(self.screen_manager.screen_width, 800)
        self.assertEqual(self.screen_manager.screen_height, 600)
        self.assertEqual(self.screen_manager.current_screen, None)
        self.assertEqual(len(self.screen_manager.screens), 0)

    def test_add_screen(self):
        mock_screen = MockScreen()
        self.screen_manager.add_screen("test", mock_screen)
        self.assertIn("test", self.screen_manager.screens)
        self.assertEqual(self.screen_manager.screens["test"], mock_screen)

    def test_set_current_screen(self):
        mock_screen = MockScreen()
        self.screen_manager.add_screen("test", mock_screen)
        self.screen_manager.set_current_screen("test")
        self.assertEqual(self.screen_manager.current_screen, "test")

        # Test with non-existent screen
        with self.assertRaises(KeyError):
            self.screen_manager.set_current_screen("nonexistent")

    def test_get_current_screen(self):
        mock_screen = MockScreen()
        self.screen_manager.add_screen("test", mock_screen)
        self.screen_manager.set_current_screen("test")
        self.assertEqual(self.screen_manager.get_current_screen(), mock_screen)

    def test_handle_events(self):
        mock_screen = MockScreen()
        self.screen_manager.add_screen("test", mock_screen)
        self.screen_manager.set_current_screen("test")

        events = [pygame.event.Event(pygame.QUIT)]
        self.screen_manager.handle_events(events)
        self.assertTrue(mock_screen.events_handled)

    def test_update(self):
        mock_screen = MockScreen()
        self.screen_manager.add_screen("test", mock_screen)
        self.screen_manager.set_current_screen("test")

        self.screen_manager.update(0.1)
        self.assertTrue(mock_screen.update_called)

    def test_render(self):
        mock_screen = MockScreen()
        self.screen_manager.add_screen("test", mock_screen)
        self.screen_manager.set_current_screen("test")

        self.screen_manager.render(self.test_surface)
        self.assertTrue(mock_screen.render_called)
