from snake_game.core.snake import Snake
from snake_game.core.food import Food
from snake_game.core.config import GRID_SIZE, UP, DOWN, LEFT, RIGHT, PLAYER_COLORS # Added PLAYER_COLORS
import logging

class Game:
    """
    Game class managing the overall game state and logic, including network roles.
    """

    def __init__(
        self,
        width,
        height,
        player_ids,
        local_player_id,
        is_server=False,
        server_instance=None,
        client_instance=None,
    ):
        """
        Initialize a new game with dimensions, player info, and network instances.

        Args:
            width: Game screen width
            height: Game screen height
            player_ids: List of all player IDs in the game
            local_player_id: ID of the player this game instance controls/represents
            is_server: Boolean, True if this instance is the server
            server_instance: Server network object (if is_server)
            client_instance: Client network object (if not is_server)
        """
        self.width = width
        self.height = height
        self.player_ids = player_ids
        self.local_player_id = local_player_id
        self.is_server = is_server
        self.server_instance = server_instance
        self.client_instance = client_instance

        self.score = 0
        self.is_game_over = False
        self.snakes = {}

        # Initialize snakes for each player
        for i, player_id in enumerate(self.player_ids):
            color = PLAYER_COLORS[i % len(PLAYER_COLORS)] # Assign color based on index
            # Start each snake at a slightly different position
            start_x = (width // 2 + i * 3 * GRID_SIZE) // GRID_SIZE * GRID_SIZE
            start_y = (height // 2) // GRID_SIZE * GRID_SIZE
            self.snakes[player_id] = Snake(start_x, start_y, player_id, color)

        # Initialize food at a random position, avoiding all snakes
        self.food = Food(0, 0)
        if self.is_server or not self.client_instance: # Server or single player initializes food
            self.food.randomize_position(
                self.width, self.height, self._get_all_snake_bodies()
            )

    def _get_all_snake_bodies(self):
        self.food.randomize_position(
            self.width, self.height, self._get_all_snake_bodies()
        )

    def _get_all_snake_bodies(self):
        """
        Helper method to get all segments from all snakes
        """
        all_bodies = []
        for snake in self.snakes.values():
            all_bodies.extend(snake.body)
        return all_bodies

    def update(self):
        """
        Update the game state for one frame.
        If server, runs simulation and broadcasts. If client, this is a lighter update (e.g., local animations).
        """
        if self.is_server:
            if self.is_game_over: # Server checks game over state
                # Broadcast game over state one last time if it just happened
                if hasattr(self, "_last_game_over_sent") and not self._last_game_over_sent:
                    game_state = self._get_serializable_game_state()
                    self.server_instance.broadcast_data(game_state)
                    self._last_game_over_sent = True
                return

            # Server: Receive client inputs
            client_inputs = self.server_instance.receive_data()
            for client_net_id, data_packet in client_inputs: # client_net_id is from network layer
                if isinstance(data_packet, dict) and data_packet.get('type') == 'input':
                    # Map network client_id to game player_id if necessary.
                    # For now, assume client_net_id might be player_id or needs mapping.
                    # Let's assume player_id is sent in the packet.
                    input_player_id = data_packet.get('player_id')
                    direction = data_packet.get('direction')
                    if input_player_id in self.snakes and direction:
                        logging.info(f"Server received input from {input_player_id}: {direction}")
                        self.snakes[input_player_id].change_direction(direction)
            
            # Server: Execute game logic
            if not self.is_game_over: # Re-check, as client input processing might not set it
                for player_id, snake in self.snakes.items():
                    snake.move()

                    # Check for wall collision
                    head_x, head_y = snake.get_head_position()
                    if (
                        head_x < 0
                        or head_x >= self.width
                        or head_y < 0
                        or head_y >= self.height
                    ):
                        self.is_game_over = True
                        logging.info(f"Game Over: Snake {player_id} hit a wall.")
                        break 

                    # Check for self-collision
                    if snake.check_self_collision():
                        self.is_game_over = True
                        logging.info(f"Game Over: Snake {player_id} collided with itself.")
                        break
                    
                    # Check for collision with other snakes (optional, can be complex)
                    # For now, not implementing snake-vs-snake collision that ends game

                    # Check if snake has eaten food
                    if head_x == self.food.x and head_y == self.food.y:
                        self.score += 1
                        snake.grow()
                        self.food.randomize_position(
                            self.width, self.height, self._get_all_snake_bodies()
                        )
                        # Break because only one snake can eat the food per frame
                        break 
                
                if self.is_game_over: # if game ended in this loop
                     self._last_game_over_sent = False # Flag to send game over state

            # Server: Prepare and broadcast game state
            game_state = self._get_serializable_game_state()
            self.server_instance.broadcast_data(game_state)

        else: # Client logic (minimal, relies on update_from_server)
            if self.is_game_over:
                return
            # Client specific updates can go here if any (e.g., local animations not tied to server state)
            pass

    def _get_serializable_game_state(self):
        """ Helper to create a dictionary of the current game state for network transfer. """
        snakes_data = {}
        for player_id, snake_obj in self.snakes.items():
            snakes_data[player_id] = {
                'body': snake_obj.body,
                'direction': snake_obj.direction,
                'is_dead': snake_obj.is_dead,
                'color': snake_obj.color, # Include color
                # 'player_id': snake_obj.player_id
            }
        return {
            'snakes': snakes_data,
            'food_pos': (self.food.x, self.food.y),
            'score': self.score,
            'is_game_over': self.is_game_over,
            'player_ids': self.player_ids, # Useful for client to know all players
        }

    def update_from_server(self, game_state):
        """
        NEW: Client-side method to update local game state from server broadcast.
        """
        if self.is_server: # Should not be called on server
            return

        logging.debug(f"Client {self.local_player_id} received game state: {game_state}")
        
        # Update snakes
        received_snakes_data = game_state.get('snakes', {})
        for player_id, data in received_snakes_data.items():
            if player_id in self.snakes:
                # Update existing snake
                self.snakes[player_id].body = data['body']
                self.snakes[player_id].direction = data['direction']
                self.snakes[player_id].is_dead = data['is_dead']
                self.snakes[player_id].color = data.get('color', PLAYER_COLORS[0]) # Get color, default if missing
            else:
                # If a snake appears mid-game (e.g. late join)
                # Create it with data from server. Client needs to know all player_ids from start.
                if player_id in self.player_ids: # Only create if it's a known player_id
                    logging.info(f"Client: Creating new snake {player_id} from server data.")
                    color = data.get('color', PLAYER_COLORS[self.player_ids.index(player_id) % len(PLAYER_COLORS)])
                    self.snakes[player_id] = Snake(data['body'][0][0], data['body'][0][1], player_id, color)
                    self.snakes[player_id].body = data['body']
                    self.snakes[player_id].direction = data['direction']
                    self.snakes[player_id].is_dead = data['is_dead']
                else:
                    logging.warning(f"Client received data for unknown or unexpected snake {player_id}")
                    
        # Update food
        food_pos = game_state.get('food_pos')
        if food_pos:
            self.food.x, self.food.y = food_pos
        
        # Update score and game_over status
        self.score = game_state.get('score', self.score)
        self.is_game_over = game_state.get('is_game_over', self.is_game_over)
        if self.is_game_over:
            logging.info(f"Client {self.local_player_id}: Game Over message received from server.")


    def handle_input(self, player_id, direction):
        """
        Handle direction input. Server acts directly, client sends to server.
        """
        if self.is_game_over: # No input if game is over
            return

        if self.is_server:
            if player_id in self.snakes:
                logging.info(f"Server handling input for {player_id}: {direction}")
                self.snakes[player_id].change_direction(direction)
            else:
                logging.warning(f"Server received input for unknown player_id: {player_id}")
        else: # Client
            if player_id == self.local_player_id and self.client_instance:
                logging.info(f"Client {self.local_player_id} sending input: {direction}")
                action = {'type': 'input', 'player_id': player_id, 'direction': direction}
                self.client_instance.send_data(action)
            # else: client should not handle input for other players

    def reset(self):
        """
        Reset the game state. For networked games, this is complex.
        Currently, server re-initializes state. Clients get updated via broadcast.
        A full robust networked reset would require more state synchronization.
        """
        logging.info(f"Game reset called. is_server: {self.is_server}")
        self.score = 0
        self.is_game_over = False
        # Server should re-initialize snakes and food, then broadcast
        # Client should ideally wait for server's new state
        
        # Store original player_ids to reinitialize snakes correctly
        # (self.player_ids should already be stored from __init__)

        # Re-initialize snakes for each player
        self.snakes = {} # Clear existing snakes
        for i, player_id in enumerate(self.player_ids):
            color = PLAYER_COLORS[i % len(PLAYER_COLORS)]
            start_x = (self.width // 2 + i * 3 * GRID_SIZE) // GRID_SIZE * GRID_SIZE
            start_y = (self.height // 2) // GRID_SIZE * GRID_SIZE
            self.snakes[player_id] = Snake(start_x, start_y, player_id, color)

        if self.is_server or not self.client_instance: # Server or single player mode
            self.food = Food(0, 0)
            self.food.randomize_position(
                self.width, self.height, self._get_all_snake_bodies()
            )
        
        # If server, an immediate broadcast of this new state might be needed
        # if self.is_server and self.server_instance:
        #     game_state = self._get_serializable_game_state()
        #     self.server_instance.broadcast_data(game_state)
        # However, reset is usually tied to starting a new game sequence in main.py

    def get_score(self):
        """
        Get the current score

        Returns:
            int: Current score
        """
        return self.score
