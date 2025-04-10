from snake_game.core.config import GRID_SIZE, UP, DOWN, LEFT, RIGHT


class Snake:
    """
    Snake class representing the player-controlled snake
    """

    def __init__(self, x, y):
        """
        Initialize a snake with a single segment at the given position

        Args:
            x: Initial x-coordinate for the snake's head
            y: Initial y-coordinate for the snake's head
        """
        # Initialize snake with a single segment
        self.body = [(x, y)]
        self.is_dead = False
        # Start with right direction
        self.direction = RIGHT

        # Flag to track growth
        self.growing = False

    @property
    def x(self):
        """
        Get the x coordinate of the snake's head

        Returns:
            int: x coordinate
        """
        return self.body[0][0]

    @property
    def y(self):
        """
        Get the y coordinate of the snake's head

        Returns:
            int: y coordinate
        """
        return self.body[0][1]

    @property
    def segments(self):
        """
        Property that returns the snake's body segments for renderer compatibility

        Returns:
            list: List of (x,y) coordinates representing the snake's body
        """
        return self.body

    def move(self):
        """Move the snake in the current direction"""
        # Update head position based on direction
        if self.direction == UP:
            self.body.insert(0, (self.body[0][0], self.body[0][1] - GRID_SIZE))
        elif self.direction == DOWN:
            self.body.insert(0, (self.body[0][0], self.body[0][1] + GRID_SIZE))
        elif self.direction == LEFT:
            self.body.insert(0, (self.body[0][0] - GRID_SIZE, self.body[0][1]))
        elif self.direction == RIGHT:
            self.body.insert(0, (self.body[0][0] + GRID_SIZE, self.body[0][1]))

        if not self.growing:
            self.body.pop()
        else:
            self.growing = False

    def change_direction(self, new_direction):
        """
        Change the snake's direction if valid (not reverse)

        Args:
            new_direction: The new direction to move in
        """
        # Prevent 180-degree turns (can't go directly opposite)
        if (
            (new_direction == UP and self.direction != DOWN)
            or (new_direction == DOWN and self.direction != UP)
            or (new_direction == LEFT and self.direction != RIGHT)
            or (new_direction == RIGHT and self.direction != LEFT)
        ):
            self.direction = new_direction

    def grow(self):
        """Grow the snake on the next move"""
        self.growing = True

    def check_self_collision(self):
        """
        Check if the snake has collided with itself

        Returns:
            bool: True if collision detected, False otherwise
        """
        # Check if head position is in the rest of the body
        head_pos = self.get_head_position()
        return head_pos in self.body[1:]

    def get_head_position(self):
        """
        Get the position of the snake's head

        Returns:
            tuple: (x, y) coordinates of head
        """
        return self.body[0]

    def get_body_positions(self):
        """
        Get all body segment positions

        Returns:
            list: List of (x, y) coordinates for all body segments
        """
        return self.body.copy()
