import random
from snake_game.core.config import GRID_SIZE


class Food:
    """
    Food class representing the food that the snake eats
    """

    def __init__(self, x, y):
        """
        Initialize food at the given position

        Args:
            x: Initial x coordinate
            y: Initial y coordinate
        """
        self.x = x
        self.y = y

    def randomize_position(self, max_x, max_y, snake_body=None):
        """
        Randomize the food position within the bounds and
        avoiding the snake's body

        Args:
            max_x: Maximum x coordinate
            max_y: Maximum y coordinate
            snake_body: List of (x, y) positions of the snake's body to avoid
        """
        # Ensure correct parameters
        snake_body = snake_body or []

        # Calculate grid-aligned positions
        grid_max_x = (max_x // GRID_SIZE) - 1
        grid_max_y = (max_y // GRID_SIZE) - 1

        # Try to find a position not occupied by the snake
        max_attempts = 100  # Avoid infinite loop
        attempts = 0

        while attempts < max_attempts:
            # Choose a random grid-aligned position
            new_x = random.randint(0, grid_max_x) * GRID_SIZE
            new_y = random.randint(0, grid_max_y) * GRID_SIZE

            # Check if position is free (not on snake body)
            if (new_x, new_y) not in snake_body:
                self.x = new_x
                self.y = new_y
                return

            attempts += 1

        # If we couldn't find a free spot after max attempts
        # Just choose a random spot and hope for the best
        self.x = random.randint(0, grid_max_x) * GRID_SIZE
        self.y = random.randint(0, grid_max_y) * GRID_SIZE

    def get_position(self):
        """
        Get the position of the food

        Returns:
            tuple: (x, y) coordinates of the food
        """
        return (self.x, self.y)
