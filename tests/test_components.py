import unittest
import pygame
from ui.components import Button, Panel, ScoreDisplay


class TestButton(unittest.TestCase):
    def setUp(self):
        pygame.init()
        self.screen = pygame.Surface((800, 600))

    def tearDown(self):
        pygame.quit()

    def test_button_initialization(self):
        action_called = False

        def test_action():
            nonlocal action_called
            action_called = True

        button = Button(100, 200, 200, 50, "Test Button", test_action)
        self.assertEqual(button.text, "Test Button")
        self.assertEqual(button.rect.x, 100)
        self.assertEqual(button.rect.y, 200)
        self.assertEqual(button.rect.width, 200)
        self.assertEqual(button.rect.height, 50)
        self.assertFalse(button.hovered)

        # Test action callback
        button.action()
        self.assertTrue(action_called)

    def test_button_hover(self):
        button = Button(100, 200, 200, 50, "Test Button")

        # Mouse outside button
        pygame.mouse.set_pos((50, 50))
        events = []
        button.update(events)
        self.assertFalse(button.hovered)

        # Mouse inside button
        pygame.mouse.set_pos((150, 225))
        button.update(events)
        self.assertTrue(button.hovered)

    def test_button_click(self):
        action_called = False

        def test_action():
            nonlocal action_called
            action_called = True

        button = Button(100, 200, 200, 50, "Test Button", test_action)

        # Simulate mouse inside button
        pygame.mouse.set_pos((150, 225))

        # Create a click event
        click_event = pygame.event.Event(
            pygame.MOUSEBUTTONDOWN, {"button": 1, "pos": (150, 225)}
        )
        button.update([click_event])

        self.assertTrue(action_called)


class TestPanel(unittest.TestCase):
    def setUp(self):
        pygame.init()
        self.screen = pygame.Surface((800, 600))

    def tearDown(self):
        pygame.quit()

    def test_panel_initialization(self):
        panel = Panel(50, 50, 300, 200)
        self.assertEqual(panel.rect.x, 50)
        self.assertEqual(panel.rect.y, 50)
        self.assertEqual(panel.rect.width, 300)
        self.assertEqual(panel.rect.height, 200)
        self.assertEqual(panel.bg_color, (20, 20, 40, 200))

    def test_custom_bg_color(self):
        panel = Panel(50, 50, 300, 200, bg_color=(100, 100, 100, 150))
        self.assertEqual(panel.bg_color, (100, 100, 100, 150))

    def test_draw(self):
        panel = Panel(50, 50, 300, 200)
        panel.draw(self.screen)
        # Just verify it doesn't throw an exception
        # Testing the actual render would require more complex pixel inspection


class TestScoreDisplay(unittest.TestCase):
    def setUp(self):
        pygame.init()
        self.screen = pygame.Surface((800, 600))

    def tearDown(self):
        pygame.quit()

    def test_score_display_initialization(self):
        score_display = ScoreDisplay(10, 10)
        self.assertEqual(score_display.x, 10)
        self.assertEqual(score_display.y, 10)
        self.assertEqual(score_display.current_score, 0)

    def test_score_update(self):
        score_display = ScoreDisplay(10, 10)
        score_display.update(100, 60.5)
        self.assertEqual(score_display.current_score, 100)
        self.assertEqual(score_display.elapsed_time, 60.5)
