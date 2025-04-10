import pytest
from snake_game.core.snake import Snake
from snake_game.core.config import UP, DOWN, LEFT, RIGHT


class TestSnake:
    def test_snake_initialization(self):
        """Test that snake initializes with correct position and body"""
        snake = Snake(100, 100)
        assert snake.x == 100
        assert snake.y == 100
        assert snake.direction == RIGHT
        assert len(snake.body) > 0
        assert (100, 100) in snake.body

    def test_snake_move_right(self):
        """Test snake moving right"""
        snake = Snake(100, 100)
        snake.direction = RIGHT
        snake.move()
        assert snake.x == 120  # Moved right by GRID_SIZE (20)
        assert snake.y == 100  # Y coordinate unchanged
        assert (120, 100) in snake.body

    def test_snake_move_left(self):
        """Test snake moving left"""
        snake = Snake(100, 100)
        snake.direction = LEFT
        snake.move()
        assert snake.x == 80  # Moved left by GRID_SIZE (20)
        assert snake.y == 100  # Y coordinate unchanged
        assert (80, 100) in snake.body

    def test_snake_move_up(self):
        """Test snake moving up"""
        snake = Snake(100, 100)
        snake.direction = UP
        snake.move()
        assert snake.x == 100  # X coordinate unchanged
        assert snake.y == 80  # Moved up by GRID_SIZE (20)
        assert (100, 80) in snake.body

    def test_snake_move_down(self):
        """Test snake moving down"""
        snake = Snake(100, 100)
        snake.direction = DOWN
        snake.move()
        assert snake.x == 100  # X coordinate unchanged
        assert snake.y == 120  # Moved down by GRID_SIZE (20)
        assert (100, 120) in snake.body
    
        def test_change_direction_valid(self):
            """Test valid direction changes"""
            snake = Snake(100, 100)
            snake.direction = RIGHT
    
            # Should be able to change to UP or DOWN, but not LEFT (reverse)
            snake.change_direction(UP)
            assert snake.direction == UP

        # Need to change to a horizontal direction first before going DOWN
        # as UP to DOWN is a 180-degree turn
        snake.change_direction(RIGHT)
        snake.change_direction(DOWN)
        assert snake.direction == DOWN

        # Try invalid direction change (reverse)
        snake.direction = RIGHT
        snake.change_direction(LEFT)
        assert snake.direction == RIGHT  # Direction should remain unchanged    def test_snake_grow(self):
        """Test snake growth"""
        snake = Snake(100, 100)
        initial_length = len(snake.body)
        snake.grow()
        # Growth happens on the next move
        snake.move()
        assert len(snake.body) == initial_length + 1

    def test_check_self_collision(self):
        """Test collision with self detection"""
        snake = Snake(100, 100)
        # No collision initially
        assert not snake.check_self_collision()

        # Force a collision by adding head position to body again
        snake.body.append((snake.x, snake.y))
        assert snake.check_self_collision()

    def test_get_head_position(self):
        """Test getting snake head position"""
        snake = Snake(100, 100)
        assert snake.get_head_position() == (100, 100)
