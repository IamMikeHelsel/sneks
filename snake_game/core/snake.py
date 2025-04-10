from snake_game.core.config import UP, DOWN, LEFT, RIGHT, GRID_SIZE


class Snake:
    """
    Snake class representing the player-controlled snake in the game
    """

    def __init__(self, x, y):
        """
        Initialize a snake at the given position

        Args:
            x: Initial x coordinate
            y: Initial y coordinate
        """
        self.x = x
        self.y = y
        self.direction = RIGHT
        self.body = [(x, y)]  # Head is the first element
        # Initialize with length 3
        self.body.append((x - GRID_SIZE, y))
        self.body.append((x - GRID_SIZE * 2, y))
        self.growth_pending = 0

    def move(self):
        """Move the snake in the current direction"""
        # Update head position based on direction
        if self.direction == UP:
            self.y -= GRID_SIZE
        elif self.direction == DOWN:
            self.y += GRID_SIZE
        elif self.direction == LEFT:
            self.x -= GRID_SIZE
        elif self.direction == RIGHT:
            self.x += GRID_SIZE

        # Add new head position to the body
        self.body.insert(0, (self.x, self.y))

        # Remove tail unless growth is pending
        if self.growth_pending > 0:
            self.growth_pending -= 1
        else:
            self.body.pop()

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
        self.growth_pending += 1

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
        return (self.x, self.y)

    def get_body(self):
        """
        Get the snake's body segments

        Returns:
            list: List of (x, y) tuples representing body segments
        """
        return self.body
