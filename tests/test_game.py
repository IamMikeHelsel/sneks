import pytest
from snake_game.core.game import Game
from snake_game.core.config import UP, DOWN, LEFT, RIGHT, GRID_SIZE


class TestGame:
    def test_game_initialization(self):
        """Test game initialization"""
        game = Game(800, 600)
        assert game.width == 800
        assert game.height == 600
        assert game.score == 0
        assert not game.is_game_over
        assert game.snake is not None
        assert game.food is not None

    def test_game_update(self):
        """Test updating the game state"""
        game = Game(800, 600)
        initial_head_pos = game.snake.get_head_position()

        # Update game state once
        game.update()

        # Snake should have moved
        new_head_pos = game.snake.get_head_position()
        assert initial_head_pos != new_head_pos

    def test_snake_eat_food(self):
        """Test snake eating food"""
        game = Game(800, 600)

        # Position the food right in front of the snake
        snake_head = game.snake.get_head_position()
        if game.snake.direction == RIGHT:
            game.food.x = snake_head[0] + GRID_SIZE
            game.food.y = snake_head[1]

        initial_score = game.score
        initial_food_pos = game.food.get_position()

        # Update game state to eat the food
        game.update()

        # Score should increase, food should move
        assert game.score == initial_score + 1
        assert game.food.get_position() != initial_food_pos

    def test_wall_collision(self):
        """Test wall collision detection"""
        # Test top wall collision
        game = Game(800, 600)
        # Position snake near top wall
        game.snake.body = [(100, 0)]
        game.snake.direction = UP

        # Update should cause collision
        game.update()
        assert game.is_game_over

        # Test bottom wall collision
        game = Game(800, 600)
        # Position snake near bottom wall
        game.snake.body = [(100, game.height - GRID_SIZE)]
        game.snake.direction = DOWN

        # Update should cause collision
        game.update()
        assert game.is_game_over

        # Test left wall collision
        game = Game(800, 600)
        # Position snake near left wall
        game.snake.body = [(0, 100)]
        game.snake.direction = LEFT

        # Update should cause collision
        game.update()
        assert game.is_game_over

        # Test right wall collision
        game = Game(800, 600)
        # Position snake near right wall
        game.snake.x = game.width - GRID_SIZE
        game.snake.y = 100
        game.snake.direction = RIGHT

        # Update should cause collision
        game.update()
        assert game.is_game_over

    def test_handle_input(self):
        """Test handling directional input"""
        game = Game(800, 600)
        # Snake initial direction is RIGHT
        assert game.snake.direction == RIGHT

        # Change direction to UP
        game.handle_input(UP)
        assert game.snake.direction == UP

        # Try to change to DOWN (invalid as it's opposite of UP)
        game.handle_input(DOWN)
        assert game.snake.direction == UP  # Direction shouldn't change

    def test_reset_game(self):
        """Test resetting the game"""
        game = Game(800, 600)

        # Make game over
        game.is_game_over = True
        game.score = 10

        # Reset game
        game.reset()

        # Check game state reset
        assert not game.is_game_over
        assert game.score == 0
        assert game.snake is not None
        assert game.food is not None
