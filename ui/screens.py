import pygame
import sys
import time
import math
from snake_game.core.config import UP, DOWN, LEFT, RIGHT, GRID_SIZE
from ui.components import Button, Panel, ScoreDisplay
from ui.effects import ParticleSystem


class Screen:
    """Base screen class for all game screens"""

    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height

    def handle_events(self, events):
        """Process pygame events"""
        pass

    def update(self, dt):
        """Update screen state"""
        pass

    def render(self, surface):
        """Render the screen"""
        pass


class MenuScreen(Screen):
    """Main menu screen with game options"""

    def __init__(
        self,
        screen_width,
        screen_height,
        start_game_callback, # For single player
        host_game_callback,  # For hosting a multiplayer game
        join_game_callback,  # For joining a multiplayer game
        open_options_callback,
        set_mode_callback=None 
    ):
        super().__init__(screen_width, screen_height)
        self.start_game_callback = start_game_callback
        self.host_game_callback = host_game_callback
        self.join_game_callback = join_game_callback # Will be called with IP
        self.open_options_callback = open_options_callback
        self.set_mode_callback = set_mode_callback 
        self.selected_mode = "normal"

        # IP Input for Join Game
        self.ip_input_active = False
        self.ip_address_str = "localhost" # Default IP
        self.font_small = pygame.font.SysFont("Arial", 24) # For IP input text

        # Background animation
        self.bg_offset = 0
        self.particles = ParticleSystem(screen_width, screen_height)

        # Title animation
        self.title_y_offset = 0
        self.title_animation_time = 0

        # Create UI components
        center_x = screen_width // 2
        center_y = screen_height // 2
        button_width = 200
        button_height = 60

        # Create buttons - adjusting layout for new options
        self.classic_mode_button = Button( # Kept for now, could be integrated differently
            center_x - button_width // 2,
            center_y - 100, # Moved up
            button_width,
            button_height,
            "Classic Mode",
            self._select_classic_mode,
        )
        
        self.start_button = Button( # This will be "Single Player"
            center_x - button_width // 2,
            center_y - 30, # Adjusted y-position
            button_width,
            button_height,
            "Single Player", # Renamed
            self.start_game_callback, # This callback should set game to single player mode
        )

        self.host_game_button = Button(
            center_x - button_width // 2,
            center_y + 40, # New button
            button_width,
            button_height,
            "Host Game",
            self.host_game_callback,
        )

        self.join_game_button = Button(
            center_x - button_width // 2,
            center_y + 110, # New button
            button_width,
            button_height,
            "Join Game",
            self._activate_ip_input_and_join, # Wrapper to handle IP
        )

        self.quit_button = Button(
            center_x - button_width // 2,
            center_y + 180, # Moved down
            button_width,
            button_height,
            "Quit",
            sys.exit,
        )

        # Create panels
        self.main_panel = Panel(center_x - 250, center_y - 200, 500, 450) # Increased height for more buttons

    def _select_classic_mode(self):
        self.selected_mode = "classic"
        if self.set_mode_callback:
            self.set_mode_callback("classic")

    def _activate_ip_input_and_join(self):
        # This method is called when "Join Game" button is clicked.
        # First click might activate IP input, second click (or Enter) could confirm.
        # For simplicity, let's assume one click activates input, then Enter/Return confirms.
        # Or, a more direct approach: clicking "Join Game" uses the current self.ip_address_str.
        # The prompt implies MenuScreen has the input field, and callback gets the IP.
        # So, we need a way to get the IP from MenuScreen when join_game_callback is eventually called.
        # Let's make "Join Game" button directly try to join with current IP string.
        # The actual text input handling will be in handle_events.
        if not self.ip_input_active:
            self.ip_input_active = True
            # User can now type. "Join Game" button won't immediately join yet.
            # Or, make "Join Game" always try with current IP, and have a separate "Edit IP" button?
            # Let's try: click "Join Game" focuses input, type, press Enter to join.
            # For now, let's make "Join Game" use the current IP.
            # The focus will be on how text is entered and displayed.
            # The prompt says "MenuScreen: Add a simple text input field".
            # This method is the button's action. So it should try to join.
            self.join_game_callback(self.ip_address_str)


    def handle_events(self, events):
        """Process pygame events"""
        if self.ip_input_active:
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.ip_input_active = False # Deactivate input on Enter
                        self.join_game_callback(self.ip_address_str) # Try to join
                    elif event.key == pygame.K_BACKSPACE:
                        self.ip_address_str = self.ip_address_str[:-1]
                    elif event.unicode.isprintable(): # Allow typing characters
                        self.ip_address_str += event.unicode
                        if len(self.ip_address_str) > 30: # Limit IP length
                             self.ip_address_str = self.ip_address_str[:30]
                # Let buttons still be clickable to deactivate IP input mode maybe
                # For now, IP input mode captures all keydown until Enter or click outside (not implemented)
        
        # Always handle button events, unless IP input is very modal
        # If IP input is active, we might not want buttons to be immediately responsive,
        # or clicking a button deactivates IP input.
        # For now, let's allow button updates always.
        # Clicking "Join Game" again while input is active could also trigger join.
        
        # Pass events to buttons
        self.classic_mode_button.update(events)
        self.start_button.update(events)
        self.host_game_button.update(events)
        self.join_game_button.update(events) # join_game_button's callback is _activate_ip_input_and_join
        self.quit_button.update(events)

        # If a mouse click occurs, and it's not on the Join Game button (or a conceptual input field area)
        # deactivate ip_input_active. This is a bit simplified.
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                # A bit of a hack: if join button is not pressed, deactivate ip input.
                # A proper UI would have focus management.
                if not self.join_game_button.rect.collidepoint(event.pos):
                     # And if it's not any other button either (for future text fields)
                    is_on_any_button = False
                    for btn in [self.classic_mode_button, self.start_button, self.host_game_button, self.quit_button]:
                        if btn.rect.collidepoint(event.pos):
                            is_on_any_button = True
                            break
                    if not is_on_any_button:
                        self.ip_input_active = False



    def update(self, dt):
        """Update menu animations"""
        self.bg_offset = (self.bg_offset + 0.2 * dt) % 40
        self.particles.update(dt)

        # Animate title
        self.title_animation_time += dt
        self.title_y_offset = 5 * math.sin(self.title_animation_time * 0.002)

    def render(self, surface):
        """Render menu screen"""
        # Fill background with dark color
        surface.fill((5, 5, 30))

        # Draw animated background grid
        for x in range(-40 + int(self.bg_offset), self.screen_width, 40):
            pygame.draw.line(surface, (20, 20, 50), (x, 0), (x, self.screen_height))
        for y in range(-40 + int(self.bg_offset), self.screen_height, 40):
            pygame.draw.line(surface, (20, 20, 50), (0, y), (self.screen_width, y))

        # Draw particles
        self.particles.draw(surface)

        # Draw main panel
        self.main_panel.draw(surface)

        # Draw title
        font_large = pygame.font.SysFont("Arial", 72, bold=True)
        font_subtitle = pygame.font.SysFont("Arial", 24)

        title = font_large.render("SNAKE", True, (100, 255, 100))
        subtitle = font_subtitle.render(
            "A Modern Python Implementation", True, (200, 200, 255)
        )

        title_pos = (
            self.screen_width // 2 - title.get_width() // 2,
            self.main_panel.rect.y + 50 + self.title_y_offset,
        )
        subtitle_pos = (
            self.screen_width // 2 - subtitle.get_width() // 2,
            title_pos[1] + 80,
        )

        # Draw shadow for title
        shadow_title = font_large.render("SNAKE", True, (0, 100, 0))
        surface.blit(shadow_title, (title_pos[0] + 4, title_pos[1] + 4))
        surface.blit(title, title_pos)
        surface.blit(subtitle, subtitle_pos)

        # Draw buttons
        self.classic_mode_button.draw(surface)
        self.start_button.draw(surface)
        self.host_game_button.draw(surface)
        self.join_game_button.draw(surface)
        self.quit_button.draw(surface)

        # Display IP Address Input Field if active or always for visibility
        ip_text_prompt = "Server IP:"
        ip_render_text = self.font_small.render(f"{ip_text_prompt} {self.ip_address_str}", True, (200, 200, 255))
        
        # Position for IP input text (e.g., below Join Game button)
        ip_text_pos_x = self.join_game_button.rect.x
        ip_text_pos_y = self.join_game_button.rect.bottom + 10
        
        surface.blit(ip_render_text, (ip_text_pos_x, ip_text_pos_y))

        if self.ip_input_active:
            # Draw a simple cursor or highlight for the input field
            cursor_x = ip_text_pos_x + self.font_small.size(f"{ip_text_prompt} {self.ip_address_str}")[0] + 2
            cursor_y = ip_text_pos_y
            pygame.draw.line(surface, (200, 200, 255), (cursor_x, cursor_y), (cursor_x, cursor_y + self.font_small.get_height()), 2)


class GameScreen(Screen):
    """Game screen that handles the actual gameplay"""

    def __init__(
        self, screen_width, screen_height, game, renderer, return_to_menu_callback, gps=10
    ):
        super().__init__(screen_width, screen_height)
        self.game = game # Game instance, contains local_player_id, is_server etc.
        self.renderer = renderer
        self.return_to_menu_callback = return_to_menu_callback
        self.gps = gps

        # Initialize UI components
        self.score_display = ScoreDisplay(10, 10)
        self.particles = ParticleSystem(screen_width, screen_height)
        self.font_status = pygame.font.SysFont("Arial", 20)
        self.status_message = "" # For messages like "Connecting...", "Waiting for player..."

        # Game state
        self.paused = False
        # self.game_over is now primarily driven by self.game.is_game_over

    def set_gps(self, gps): # Remains for classic mode
        self.gps = gps
    
    def set_status_message(self, message):
        self.status_message = message

    def handle_events(self, events):
        """Handle game events"""
        for event in events:
            if event.type == pygame.KEYDOWN:
                # Pass the local_player_id for multiplayer context
                local_player_id = self.game.local_player_id if self.game else None

                if event.key == pygame.K_UP:
                    self.game.handle_input(local_player_id, UP)
                elif event.key == pygame.K_DOWN:
                    self.game.handle_input(local_player_id, DOWN)
                elif event.key == pygame.K_LEFT:
                    self.game.handle_input(local_player_id, LEFT)
                elif event.key == pygame.K_RIGHT:
                    self.game.handle_input(local_player_id, RIGHT)
                
                if event.key == pygame.K_p: # Pause should be local
                    self.paused = not self.paused
                elif event.key == pygame.K_r and self.game_over:
                    # Reset in networked game is complex. Server should initiate.
                    # For now, this might only work well in single player or if server handles 'r'
                    if self.game.is_server or not (self.game.client_instance or self.game.server_instance): # single player or server
                        self.game.reset()
                        self.game_over = False
                elif event.key == pygame.K_ESCAPE:
                    self.return_to_menu_callback() # This should also handle disconnecting network if active

    def update(self, dt):
        """Update game state"""
        game_is_over = self.game.is_game_over if self.game else True

        if not self.paused and not game_is_over:
            if self.game:
                 self.game.update() # This now handles server/client specific logic

            # Particle effect for game over - needs to be triggered when self.game.is_game_over becomes true
            # This might need a flag to ensure it only triggers once.
            if self.game and self.game.is_game_over:
                 if not hasattr(self, '_game_over_effect_done') or not self._game_over_effect_done:
                    if self.game.local_player_id and self.game.local_player_id in self.game.snakes:
                        local_snake = self.game.snakes[self.game.local_player_id]
                        if not local_snake.is_dead: 
                            head_pos = local_snake.get_head_position()
                            self.particles.add_explosion(
                                head_pos[0] + GRID_SIZE // 2,
                                head_pos[1] + GRID_SIZE // 2,
                                color=(255, 50, 50), count=50,
                            )
                    self._game_over_effect_done = True # Mark effect as done
        elif not game_is_over : # Game is not over, but paused
            pass # Paused logic
        else: # Game is over
            if hasattr(self, '_game_over_effect_done') and not self.game.is_game_over:
                self._game_over_effect_done = False # Reset for next game

        self.particles.update(dt)


    def render(self, surface):
        """Render the game screen"""
        if not self.game:
            # Potentially render a "Loading..." or error message if game is None
            return

        # Render game elements using the renderer.
        # render_game now uses render_snakes internally.
        self.renderer.render_game(surface, self.game) 

        # Render score
        self.score_display.draw(surface, self.game.score)

        # Render particles
        self.particles.draw(surface)

        # Display role and local player ID
        role_text = "Host" if self.game.is_server else "Client"
        player_id_text = f"Player ID: {self.game.local_player_id}"
        
        role_surface = self.font_status.render(role_text, True, (220, 220, 255))
        pid_surface = self.font_status.render(player_id_text, True, (220, 220, 255))
        
        surface.blit(role_surface, (self.screen_width - role_surface.get_width() - 10, 10))
        surface.blit(pid_surface, (self.screen_width - pid_surface.get_width() - 10, 35))

        # Display status message (e.g., "Connecting...", "Waiting for player...")
        if self.status_message:
            status_surface = self.font_status.render(self.status_message, True, (255, 255, 100))
            status_pos_x = self.screen_width // 2 - status_surface.get_width() // 2
            status_pos_y = 10 # Display at the top-center
            surface.blit(status_surface, (status_pos_x, status_pos_y))
            
        # Display pause message if the game is paused
        if self.paused and not self.game.is_game_over:
            font_pause = pygame.font.SysFont("Arial", 48, bold=True)
            paused_text_surf = font_pause.render("PAUSED", True, (255, 255, 255))
            text_rect = paused_text_surf.get_rect(center=(self.screen_width // 2, self.screen_height // 2))
            overlay = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 128))
            surface.blit(overlay, (0, 0))
            shadow_pause = font_pause.render("PAUSED", True, (50, 50, 50))
            shadow_rect = shadow_pause.get_rect(center=(self.screen_width // 2 + 2, self.screen_height // 2 + 2))
            surface.blit(shadow_pause, shadow_rect)
            surface.blit(paused_text_surf, text_rect)
        
        # Game over message is handled by renderer.render_game_over if self.game.is_game_over is true.


class OptionsScreen(Screen):
    """Options screen for adjusting game settings"""

    def __init__(self, screen_width, screen_height, return_to_menu_callback):
        super().__init__(screen_width, screen_height)
        self.return_to_menu_callback = return_to_menu_callback

    def handle_events(self, events):
        pass

    def update(self, dt):
        pass

    def render(self, surface):
        surface.fill((30, 30, 60))
        font = pygame.font.SysFont("Arial", 48, bold=True)
        options_text = font.render("OPTIONS", True, (255, 255, 255))
        text_rect = options_text.get_rect(
            center=(self.screen_width // 2, self.screen_height // 2)
        )
        surface.blit(options_text, text_rect)


class ScreenManager:
    """Manages different screens in the game"""

    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.screens = {}
        self.current_screen = None

    def add_screen(self, name, screen):
        """Add a screen to the manager"""
        self.screens[name] = screen

    def set_current_screen(self, name):
        """Change the current active screen"""
        if name in self.screens:
            self.current_screen = name
        else:
            raise ValueError(
                f"Screen '{name}' not found"
            )  # Changed KeyError to ValueError

    def get_current_screen(self):
        """Get the currently active screen object"""
        if self.current_screen and self.current_screen in self.screens:
            return self.screens[self.current_screen]
        return None

    def handle_events(self, events):
        """Pass events to the current screen"""
        screen = self.get_current_screen()
        if screen:
            screen.handle_events(events)

    def update(self, dt):
        """Update the current screen"""
        screen = self.get_current_screen()
        if screen:
            screen.update(dt)

    def render(self, surface):
        """Render the current screen"""
        screen = self.get_current_screen()
        if screen:
            screen.render(surface)
