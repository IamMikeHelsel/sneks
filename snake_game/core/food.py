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

    def randomize_position(self, max_x, max_y, all_snake_bodies=None):
        """
        Randomize the food position within the bounds and
        avoiding all snakes' bodies

        Args:
            max_x: Maximum x coordinate
            max_y: Maximum y coordinate
            all_snake_bodies: List of (x, y) positions of all snakes' bodies to avoid
        """
        # Ensure correct parameters
        all_snake_bodies = all_snake_bodies or []

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

            # Check if position is free (not on any snake body)
            if (new_x, new_y) not in all_snake_bodies:
                self.x = new_x
                self.y = new_y
                return

            attempts += 1

        # If we couldn't find a free spot after max attempts
        # Just choose a random spot and hope for the best
        self.x = random.randint(0, grid_max_x) * GRID_SIZE
        self.y = random.randint(0, grid_max_y) * GRID_SIZE

    def reposition(self, all_snake_bodies):
        """
        Reposition the food to avoid all snakes' bodies (alias for randomize_position)

        Args:
            all_snake_bodies: List of (x, y) positions of all snakes' bodies to avoid
        """
        # Use existing screen dimensions
        max_x = 800  # Default maximum x
        max_y = 600  # Default maximum y
        self.randomize_position(max_x, max_y, all_snake_bodies)

    def get_position(self):
        """
        Get the position of the food

        Returns:
            tuple: (x, y) coordinates of the food
        """
        return (self.x, self.y)
