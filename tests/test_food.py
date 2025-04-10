from snake_game.core.food import Food
from snake_game.core.config import GRID_SIZE


class TestFood:
    def test_food_initialization(self):
        """Test food initialization with given position"""
        food = Food(100, 100)
        assert food.x == 100
        assert food.y == 100

    def test_randomize_position(self):
        """Test randomizing food position within bounds"""
        food = Food(0, 0)
        max_x = 800
        max_y = 600

        food.randomize_position(max_x, max_y)

        # Check that the food is within bounds and aligned to grid
        assert 0 <= food.x < max_x
        assert 0 <= food.y < max_y
        assert food.x % GRID_SIZE == 0
        assert food.y % GRID_SIZE == 0

    def test_randomize_position_avoids_snake(self):
        """Test that food doesn't appear on snake body"""
        food = Food(0, 0)
        max_x = 800
        max_y = 600

        # Create a mock snake body
        snake_body = [(100, 100), (120, 100), (140, 100)]

        # Try multiple times to ensure it's avoiding snake
        for _ in range(10):
            food.randomize_position(max_x, max_y, snake_body)
            assert (food.x, food.y) not in snake_body

    def test_get_position(self):
        """Test getting food position"""
        food = Food(100, 100)
        assert food.get_position() == (100, 100)
