import pygame
import sys
import time
import logging
from snake_game.core.game import Game
from snake_game.core.config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, GREEN, UP, DOWN, LEFT, RIGHT
from snake_game.core.network import Server, Client # Network imports
from ui.renderer import SnakeRenderer
from ui.screens import MenuScreen, GameScreen, ScreenManager

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Global variables for network instances and game state
server_instance = None
client_instance = None
game_instance = None # This will hold the current Game object
game_mode = "menu" # 'menu', 'single', 'host', 'client'
selected_classic_mode = {"mode": "normal"} # Keep classic mode selection separate
classic_gps_value = {"value": 10}


def main():
    """
    Main entry point for the Snake Game
    """
    global server_instance, client_instance, game_instance, game_mode
    global selected_classic_mode, classic_gps_value
    global game_accumulator # Make game_accumulator global for access in callbacks

    pygame.init()
    pygame.display.set_caption("SNEKS: Multiplayer Edition")

    icon = pygame.Surface((32, 32))
    icon.fill((20, 20, 40))
    pygame.draw.rect(icon, GREEN, (8, 8, 16, 16), border_radius=4)
    pygame.display.set_icon(icon)

    screen = pygame.display.set_mode(
        (SCREEN_WIDTH, SCREEN_HEIGHT), pygame.HWSURFACE | pygame.DOUBLEBUF
    )
    clock = pygame.time.Clock()
    renderer = SnakeRenderer(SCREEN_WIDTH, SCREEN_HEIGHT)
    screen_manager = ScreenManager(SCREEN_WIDTH, SCREEN_HEIGHT)
    
    game_accumulator = 0.0 # Initialize game_accumulator

    def common_game_start_actions():
        nonlocal game_accumulator # Python 2 might need global here instead of nonlocal
        game_accumulator = 0.0
        # Initialize GameScreen with the current game_instance
        # This assumes game_instance is already created by host_game, join_game, or start_single_player_game
        if game_instance:
            game_screen = GameScreen(
                SCREEN_WIDTH, SCREEN_HEIGHT, game_instance, renderer, return_to_menu
            )
            if selected_classic_mode["mode"] == "classic":
                game_screen.set_gps(classic_gps_value["value"])
            else:
                game_screen.set_gps(FPS)
            screen_manager.add_screen("game", game_screen) # Add or update game screen
            screen_manager.set_current_screen("game")
        else:
            logging.error("Attempted to start game without a game_instance!")
            return_to_menu() # Go back to menu if game_instance is not set

    def start_single_player_game():
        global game_instance, game_mode
        logging.info("Starting Single Player Game...")
        game_mode = "single"
        # For single player, player_ids list and local_player_id are the same.
        player_id = "player1" 
        game_instance = Game(
            SCREEN_WIDTH,
            SCREEN_HEIGHT,
            player_ids=[player_id],
            local_player_id=player_id,
            is_server=False, # Acts as its own "server" but no networking
            server_instance=None,
            client_instance=None,
        )
        common_game_start_actions()

    def host_game():
        global server_instance, game_instance, game_mode
        logging.info("Starting to Host Game...")
        game_mode = "host"
        host_ip = "0.0.0.0"
        port = 5555
        server_instance = Server(host_ip, port, max_clients=1) # Max 1 client for 2 players total
        
        player1_id = "player1" # Host
        # Player IDs will be updated once client connects, or assume fixed for now
        # For now, initialize with player1, then add player2 when they connect.
        # Or, assume fixed player IDs for now.
        initial_player_ids = [player1_id] # Server starts with only itself
        
        game_instance = Game(
            SCREEN_WIDTH,
            SCREEN_HEIGHT,
            player_ids=initial_player_ids, # Start with host, client ID added on connection
            local_player_id=player1_id,
            is_server=True,
            server_instance=server_instance,
            client_instance=None,
        )
        # Game will start rendering, server will wait for connections in its update loop
        common_game_start_actions()
        logging.info(f"Server listening on {host_ip}:{port}")

    def join_game():
        global client_instance, game_instance, game_mode
        logging.info("Attempting to Join Game...")
        game_mode = "client"
        # TODO: Add UI to input server IP
        server_host = "localhost" 
        port = 5555
        client_instance = Client(server_host, port)
        # Get IP from MenuScreen instance. menu_screen is globally accessible in this context.
        server_host_ip = menu_screen.ip_address_str if menu_screen else "localhost"
        logging.info(f"Attempting to Join Game at IP: {server_host_ip}")

        client_instance = Client(server_host_ip, port)
        
        current_game_screen = screen_manager.screens.get("game")
        if current_game_screen: # Set status on GameScreen if it exists
            current_game_screen.set_status_message(f"Connecting to {server_host_ip}...")
        
        if client_instance.connect():
            logging.info(f"Successfully connected to server {server_host_ip}:{port}")
            if current_game_screen: current_game_screen.set_status_message("Connected! Waiting for game state...")
            
            player2_id = "player2"  # Assume client is player2 for now
            all_player_ids = ["player1", "player2"] 
            
            game_instance = Game(
                SCREEN_WIDTH,
                SCREEN_HEIGHT,
                player_ids=all_player_ids, # Client needs to be aware of all players
                local_player_id=player2_id,
                is_server=False,
                server_instance=None,
                client_instance=client_instance,
            )
            common_game_start_actions()
            # Update GameScreen's game instance if it was created before game_instance was ready
            if screen_manager.screens.get("game"):
                 screen_manager.screens.get("game").game = game_instance
        else:
            logging.error(f"Failed to connect to server {server_host_ip}:{port}. Returning to menu.")
            if current_game_screen: current_game_screen.set_status_message(f"Failed to connect to {server_host_ip}")
            # Display error on MenuScreen or a dedicated error screen later
            menu_screen.ip_input_active = True # Keep IP input active
            game_mode = "menu"
            screen_manager.set_current_screen("menu")


    def return_to_menu():
        global game_instance, game_mode, server_instance, client_instance
        
        current_game_screen = screen_manager.screens.get("game")
        if current_game_screen:
            current_game_screen.set_status_message("") # Clear status message

        logging.info("Returning to menu...")
        if game_mode == "host" and server_instance:
            server_instance.close()
            server_instance = None
        elif game_mode == "client" and client_instance:
            client_instance.close()
            client_instance = None
        
        game_instance = None # Clear game instance
        game_mode = "menu"
        screen_manager.set_current_screen("menu")
        if screen_manager.get_current_screen() is menu_screen: # Ensure menu is active
             menu_screen.title_animation_time = 0 # Reset menu animation if needed

    def open_options():
        pass 

    def set_classic_mode(mode_name): # Renamed from set_mode to avoid conflict
        global selected_classic_mode, classic_gps_value
        selected_classic_mode["mode"] = mode_name
        if mode_name == "classic":
            import random
            classic_gps_value["value"] = random.randint(8, 12)
        else: # normal
            classic_gps_value["value"] = FPS # Use FPS for normal mode


    menu_screen = MenuScreen(
        SCREEN_WIDTH,
        SCREEN_HEIGHT,
        start_single_player_game, # start_game_callback
        host_game,                # host_game_callback
        join_game,                # join_game_callback
        open_options,
        set_mode_callback=set_classic_mode
    )
    # GameScreen is now created dynamically in common_game_start_actions
    
    screen_manager.add_screen("menu", menu_screen)
    screen_manager.set_current_screen("menu")

    last_time = time.time()
    # game_accumulator is now global

    while True:
        current_time = time.time()
        dt = current_time - last_time
        last_time = current_time
        dt = min(dt, 0.05) # Cap dt

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                if server_instance: server_instance.close()
                if client_instance: client_instance.close()
                pygame.quit()
                sys.exit()
            
            # Pass relevant events to screen manager for button clicks etc.
            # Input handling for game actions (like snake movement) should be inside GameScreen
            # or passed to game_instance if game_mode is active.
            # For now, GameScreen's handle_events is expected to call game_instance.handle_input
            # with the local_player_id.

        # --- Network updates ---
        if game_mode == "host" and server_instance and game_instance:
            new_client_ids = server_instance.accept_connections()
            for client_net_id in new_client_ids:
                logging.info(f"Server: New client connected with network ID: {client_net_id}")
                # Assign a player ID to this new client. For a 2-player game, this is 'player2'.
                # This logic needs to be robust for more players or dynamic assignment.
                if "player2" not in game_instance.player_ids: # Assuming player1 is host
                    new_player_id = "player2"
                    game_instance.player_ids.append(new_player_id)
                    # Initialize snake for new player on server
                    # Make sure this matches client-side expectation if client also auto-creates
                    start_x = (SCREEN_WIDTH // 2 + 1 * 3 * GRID_SIZE) // GRID_SIZE * GRID_SIZE 
                    start_y = (SCREEN_HEIGHT // 2) // GRID_SIZE * GRID_SIZE
                    game_instance.snakes[new_player_id] = game_instance.snakes.get(new_player_id) or \
                        type(game_instance.snakes[game_instance.local_player_id])(start_x, start_y, new_player_id) # Create snake if not exist
                    
                    logging.info(f"Server: Assigned {new_player_id} to {client_net_id}. Total players: {game_instance.player_ids}")
                    # Server might need to send an initial full state or player assignment message here.
                    # For now, the regular broadcast from game_instance.update() will handle it.
                else:
                    logging.warning("Server: Max players reached or player2 already exists. Ignoring new connection.")
            # Server's game_instance.update() handles receiving inputs and broadcasting state
            if game_instance and not game_instance.player_ids L: # if player_ids only has host
                 if screen_manager.screens.get("game"):
                    screen_manager.screens.get("game").set_status_message("Waiting for player to join...")
            elif game_instance and len(game_instance.player_ids) > 1:
                 if screen_manager.screens.get("game"):
                    screen_manager.screens.get("game").set_status_message("Player connected!") # Or clear message
        
        elif game_mode == "client" and client_instance and game_instance:
            current_game_screen = screen_manager.screens.get("game")
            if client_instance.connected:
                server_data = client_instance.receive_data()
                if server_data is False: 
                    logging.error("Client: Disconnected from server or error receiving data.")
                    if current_game_screen: current_game_screen.set_status_message("Disconnected from server.")
                    return_to_menu() 
                elif server_data is not None:
                    game_instance.update_from_server(server_data)
                    if current_game_screen and current_game_screen.status_message == "Connected! Waiting for game state...":
                         current_game_screen.set_status_message("") # Clear after first state update
            else: 
                logging.info("Client: Not connected. Attempting to return to menu.")
                if current_game_screen: current_game_screen.set_status_message("Connection lost.")
                return_to_menu()
        
        # --- Screen and Game Logic Update ---
        current_screen_obj = screen_manager.get_current_screen()
        if current_screen_obj:
            current_screen_obj.handle_events(events) 

            if current_screen_obj is screen_manager.screens.get("game") and game_instance:
                gps = classic_gps_value["value"] if selected_classic_mode["mode"] == "classic" else FPS
                game_step = 1.0 / gps
                game_accumulator += dt
                while game_accumulator >= game_step:
                    current_screen_obj.update(game_step * 1000.0) 
                    game_accumulator -= game_step
            else: 
                current_screen_obj.update(dt * 1000.0) 
        
        # --- Rendering ---
        screen.fill((20, 20, 40))
        if current_screen_obj:
            current_screen_obj.render(screen)
        pygame.display.flip()

        clock.tick(60) # Maintain 60 FPS rendering

if __name__ == "__main__":
    main()
