import unittest
from unittest.mock import MagicMock
from snake_game.core.game import Game
from snake_game.core.snake import Snake
from snake_game.core.food import Food
from snake_game.core.config import SCREEN_WIDTH, SCREEN_HEIGHT, PLAYER_COLORS, UP, DOWN, LEFT, RIGHT, GRID_SIZE

class TestGameMultiplayer(unittest.TestCase):

    def setUp(self):
        """Common setup for game tests."""
        self.player1_id = "player1"
        self.player2_id = "player2"
        self.player_ids = [self.player1_id, self.player2_id]
        
        # Mock network instances
        self.mock_server_instance = MagicMock()
        self.mock_client_instance = MagicMock()

    def create_server_game(self, player_ids=None):
        if player_ids is None:
            player_ids = [self.player1_id] # Server initially might only know itself
            
        game = Game(
            width=SCREEN_WIDTH,
            height=SCREEN_HEIGHT,
            player_ids=player_ids,
            local_player_id=self.player1_id, # Server's own ID
            is_server=True,
            server_instance=self.mock_server_instance,
            client_instance=None
        )
        return game

    def create_client_game(self, local_player_id, all_player_ids):
        game = Game(
            width=SCREEN_WIDTH,
            height=SCREEN_HEIGHT,
            player_ids=all_player_ids,
            local_player_id=local_player_id,
            is_server=False,
            server_instance=None,
            client_instance=self.mock_client_instance
        )
        return game

    def test_game_initialization_multiplayer(self):
        """Test game initializes with multiple players, distinct positions and colors."""
        game = self.create_server_game(player_ids=self.player_ids)
        
        self.assertEqual(len(game.snakes), len(self.player_ids))
        positions = []
        colors = []
        for i, player_id in enumerate(self.player_ids):
            self.assertIn(player_id, game.snakes)
            snake = game.snakes[player_id]
            self.assertIsInstance(snake, Snake)
            self.assertEqual(snake.player_id, player_id)
            positions.append(snake.body[0])
            colors.append(snake.color)
            self.assertEqual(snake.color, PLAYER_COLORS[i % len(PLAYER_COLORS)])

        # Check for distinct starting positions (simple check, assumes they are not all same)
        self.assertTrue(len(set(positions)) == len(positions), "Snakes should have distinct starting positions.")
        # Check for distinct colors if enough PLAYER_COLORS are available
        if len(PLAYER_COLORS) >= len(self.player_ids):
            self.assertTrue(len(set(colors)) == len(colors), "Snakes should have distinct colors.")

    def test_server_handle_input_for_itself(self):
        """Test server game handles input for its own snake directly."""
        game = self.create_server_game(player_ids=[self.player1_id])
        initial_direction = game.snakes[self.player1_id].direction
        self.assertNotEqual(initial_direction, UP) # Assuming initial direction is not UP

        game.handle_input(self.player1_id, UP)
        self.assertEqual(game.snakes[self.player1_id].direction, UP)

    def test_server_processes_received_client_input(self):
        """Test server game processes input received from a client via server_instance."""
        # Server game with two players already known
        game = self.create_server_game(player_ids=self.player_ids)
        
        client_input_data = {'type': 'input', 'player_id': self.player2_id, 'direction': LEFT}
        self.mock_server_instance.receive_data.return_value = [("network_client_id_for_p2", client_input_data)]
        
        initial_direction_p2 = game.snakes[self.player2_id].direction
        self.assertNotEqual(initial_direction_p2, LEFT)

        game.update() # Server update processes received data

        self.assertEqual(game.snakes[self.player2_id].direction, LEFT)
        self.mock_server_instance.broadcast_data.assert_called() # Server should broadcast after update

    def test_client_sends_input_via_client_instance(self):
        """Test client game sends its input via client_instance."""
        game = self.create_client_game(local_player_id=self.player1_id, all_player_ids=self.player_ids)
        
        game.handle_input(self.player1_id, DOWN)
        
        expected_action = {'type': 'input', 'player_id': self.player1_id, 'direction': DOWN}
        self.mock_client_instance.send_data.assert_called_with(expected_action)

    def test_multi_snake_movement_and_food_consumption(self):
        """Test movement of multiple snakes and one eating food on server."""
        game = self.create_server_game(player_ids=self.player_ids)
        snake1 = game.snakes[self.player1_id]
        snake2 = game.snakes[self.player2_id]

        # Position snake1 to eat food
        # Assuming food is at (fx, fy) and snake1 moves towards it
        game.food.x = snake1.body[0][0] + GRID_SIZE # Place food in front of snake1 (if moving RIGHT)
        game.food.y = snake1.body[0][1]
        snake1.change_direction(RIGHT)
        snake2.change_direction(LEFT) # Move snake2 away or in some other direction

        initial_score = game.score
        initial_len_s1 = len(snake1.body)
        initial_len_s2 = len(snake2.body)
        initial_food_pos = (game.food.x, game.food.y)

        game.update() # Server processes one game tick

        self.assertEqual(game.score, initial_score + 1, "Score should increment.")
        self.assertEqual(len(snake1.body), initial_len_s1 + 1, "Snake1 should grow.")
        self.assertEqual(len(snake2.body), initial_len_s2, "Snake2 length should not change.")
        self.assertNotEqual((game.food.x, game.food.y), initial_food_pos, "Food should reposition.")
        
        # Ensure new food position is not under any snake
        all_bodies = game._get_all_snake_bodies()
        self.assertNotIn((game.food.x, game.food.y), all_bodies, "New food position should not overlap with snakes.")

    def test_multi_snake_wall_collision(self):
        """Test game over when one snake hits a wall on server."""
        game = self.create_server_game(player_ids=self.player_ids)
        snake1 = game.snakes[self.player1_id]
        
        # Move snake1 towards wall until it collides
        snake1.change_direction(LEFT) # Assuming starts near center, move left
        snake1.body = [(0, snake1.body[0][1])] # Place head at edge
        
        self.assertFalse(game.is_game_over)
        game.update() # Snake moves one step: (0,y) -> (-GRID_SIZE,y) -> collision
        self.assertTrue(game.is_game_over, "Game should be over after wall collision.")

    def test_multi_snake_self_collision(self):
        """Test game over when one snake collides with itself on server."""
        game = self.create_server_game(player_ids=self.player_ids)
        snake1 = game.snakes[self.player1_id]

        # Force self-collision for snake1
        # Needs a snake of at least 4 segments to make a simple self-collision by turning back
        snake1.body = [(2*GRID_SIZE, 0), (GRID_SIZE,0), (0,0), (-GRID_SIZE,0)] # Head at (2*GRID_SIZE,0)
        snake1.change_direction(LEFT) # Try to move into (GRID_SIZE,0) which is part of its body
        
        self.assertFalse(game.is_game_over)
        game.update() # Snake moves, head now at (GRID_SIZE,0)
        self.assertTrue(game.is_game_over, "Game should be over after self-collision.")

    def test_snakes_pass_through_each_other(self):
        """Test that snakes can pass through each other without collision (as per current rules)."""
        game = self.create_server_game(player_ids=self.player_ids)
        snake1 = game.snakes[self.player1_id]
        snake2 = game.snakes[self.player2_id]

        # Position snakes to cross paths
        snake1.body = [(GRID_SIZE * 2, GRID_SIZE * 2)]
        snake1.change_direction(RIGHT) # Will move to (3,2)
        
        snake2.body = [(GRID_SIZE * 3, GRID_SIZE * 2)] # Will be at same spot as snake1's new head
        snake2.change_direction(LEFT) # Will move to (2,2)

        self.assertFalse(game.is_game_over)
        game.update() # Snakes move and cross paths
        self.assertFalse(game.is_game_over, "Game should not be over if snakes just pass through.")
        self.assertEqual(snake1.get_head_position(), (GRID_SIZE * 3, GRID_SIZE * 2))
        self.assertEqual(snake2.get_head_position(), (GRID_SIZE * 2, GRID_SIZE * 2))

    def test_game_state_serialization(self):
        """Test _get_serializable_game_state contains essential info."""
        game = self.create_server_game(player_ids=self.player_ids)
        # Make snakes have multiple segments and specific directions/colors
        game.snakes[self.player1_id].grow()
        game.snakes[self.player1_id].move()
        game.snakes[self.player1_id].change_direction(UP)
        game.snakes[self.player2_id].change_direction(DOWN)
        
        state = game._get_serializable_game_state()

        self.assertIn('snakes', state)
        self.assertIn('food_pos', state)
        self.assertIn('score', state)
        self.assertIn('is_game_over', state)
        self.assertIn('player_ids', state)
        self.assertEqual(state['player_ids'], self.player_ids)

        self.assertEqual(len(state['snakes']), len(self.player_ids))
        for player_id, snake_data in state['snakes'].items():
            original_snake = game.snakes[player_id]
            self.assertEqual(snake_data['body'], original_snake.body)
            self.assertEqual(snake_data['direction'], original_snake.direction)
            self.assertEqual(snake_data['is_dead'], original_snake.is_dead)
            self.assertEqual(snake_data['color'], original_snake.color)
        
        self.assertEqual(state['food_pos'], (game.food.x, game.food.y))
        self.assertEqual(state['score'], game.score)
        self.assertEqual(state['is_game_over'], game.is_game_over)

    def test_client_update_from_server_state(self):
        """Test client game updates its local state from a received server state."""
        client_game = self.create_client_game(local_player_id=self.player1_id, all_player_ids=self.player_ids)
        
        # Sample server state
        server_snake1_body = [(GRID_SIZE, GRID_SIZE), (GRID_SIZE, GRID_SIZE*2)]
        server_snake2_body = [(GRID_SIZE*5, GRID_SIZE*5), (GRID_SIZE*5, GRID_SIZE*6)]
        server_state = {
            'snakes': {
                self.player1_id: {'body': server_snake1_body, 'direction': RIGHT, 'is_dead': False, 'color': PLAYER_COLORS[0]},
                self.player2_id: {'body': server_snake2_body, 'direction': LEFT, 'is_dead': True, 'color': PLAYER_COLORS[1]},
            },
            'food_pos': (GRID_SIZE*3, GRID_SIZE*3),
            'score': 10,
            'is_game_over': True, # Game is over because player2 is dead
            'player_ids': self.player_ids
        }

        client_game.update_from_server(server_state)

        # Check client's game state
        self.assertEqual(client_game.score, 10)
        self.assertTrue(client_game.is_game_over)
        self.assertEqual((client_game.food.x, client_game.food.y), (GRID_SIZE*3, GRID_SIZE*3))
        
        client_snake1 = client_game.snakes[self.player1_id]
        self.assertEqual(client_snake1.body, server_snake1_body)
        self.assertEqual(client_snake1.direction, RIGHT)
        self.assertFalse(client_snake1.is_dead)
        self.assertEqual(client_snake1.color, PLAYER_COLORS[0])

        client_snake2 = client_game.snakes[self.player2_id]
        self.assertEqual(client_snake2.body, server_snake2_body)
        self.assertEqual(client_snake2.direction, LEFT)
        self.assertTrue(client_snake2.is_dead)
        self.assertEqual(client_snake2.color, PLAYER_COLORS[1])

if __name__ == '__main__':
    unittest.main()
