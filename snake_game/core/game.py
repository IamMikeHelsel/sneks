from snake_game.core.snake import Snake
from snake_game.core.food import Food
from snake_game.core.config import GRID_SIZE


class Game:
    """
    Game class managing the overall game state and logic
    """

    def __init__(self, width, height):
        """
        Initialize a new game with the given dimensions

        Args:
            width: Game screen width
            height: Game screen height
        """
        self.width = width
        self.height = height
        self.score = 0
        self.is_game_over = False  # Initialize snake in the middle of the screen
        start_x = (width // 2) // GRID_SIZE * GRID_SIZE
        start_y = (height // 2) // GRID_SIZE * GRID_SIZE
        self.snake = Snake(start_x, start_y)

        # Initialize food at a random position
        self.food = Food(0, 0)
        self.food.randomize_position(width, height, self.snake.body)

    def update(self):
        """
        Update the game state for one frame
        """
        if self.is_game_over:
            return

        # Move the snake
        self.snake.move()

        # Check for wall collision
        head_x, head_y = self.snake.get_head_position()
        if head_x < 0 or head_x >= self.width or head_y < 0 or head_y >= self.height:
            self.is_game_over = True
            return  # Check if the snake is dead due to self-collision
        if self.snake.check_self_collision():
            self.is_game_over = True
            return

        # Check if snake has eaten food
        if head_x == self.food.x and head_y == self.food.y:
            self.score += 1
            self.snake.grow()
            self.food.randomize_position(self.width, self.height, self.snake.body)

    def handle_input(self, direction):
        """
        Handle direction input from player

        Args:
            direction: The new direction (UP, DOWN, LEFT, RIGHT)
        """
        if not self.is_game_over:
            self.snake.change_direction(direction)

    def reset(self):
        """
        Reset the game state to start a new game
        """
        self.score = 0
        self.is_game_over = False

        # Reinitialize snake in the middle of the screen
        start_x = (self.width // 2) // GRID_SIZE * GRID_SIZE
        start_y = (self.height // 2) // GRID_SIZE * GRID_SIZE

        # Reset snake, food, and other game elements
        # This will need to match the initialization in __init__
        # Recreate the snake
        self.snake = Snake(start_x, start_y)  # Generate new food at a random position
        self.food = Food(0, 0)  # Initialize with temporary position
        self.food.randomize_position(
            self.width, self.height, self.snake.get_body_positions()
        )

    def get_score(self):
        """
        Get the current score

        Returns:
            int: Current score
        """
        return self.score
