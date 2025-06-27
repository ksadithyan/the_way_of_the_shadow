
from settings import *
from sprites import Player, Platform, Collectible, Goal
from levels import LEVELS, MAX_LEVELS
from ui import Button, draw_text
def format_time(total_seconds):
    """Formats time in seconds to MM:SS:ms"""
    # Check for infinity OR None (safer initial state)
    if total_seconds == float('inf') or total_seconds is None or total_seconds < 0:
        return "--:--:---"
    milliseconds = int((total_seconds * 1000) % 1000)
    seconds = int(total_seconds % 60)
    minutes = int(total_seconds // 60)
    return f"{minutes:02}:{seconds:02}:{milliseconds:03}"
class Game:
    def __init__(self):
        pygame.mixer.pre_init(44100, -16, 2, 512);
        pygame.init();
        pygame.mixer.init()
        self.current_screen_width = SCREEN_WIDTH;
        self.current_screen_height = SCREEN_HEIGHT
        self.screen_flags = pygame.RESIZABLE | pygame.SCALED
        self.screen = pygame.display.set_mode((self.current_screen_width, self.current_screen_height),
                                              self.screen_flags)
        pygame.display.set_caption(TITLE);
        self.clock = pygame.time.Clock()
        self.running = True;
        self.fullscreen = False

        # --- Timer and High Score Variables ---
        self.level_elapsed_time = 0.0
        self.total_game_time = 0.0  # Accumulates *successfully completed* level times
        self.final_time = None  # Set only upon winning the *entire* game
        self.timer_active = False
        self.high_score = self.load_highscore()  # Load best time initially
        # ------------------------------------
        self.coins_for_powerup_count = 0
        self.powerup_active = False
        self.powerup_end_time = 0
        # -----------------------------
        self.load_assets();
        self.setup_game_variables()  # Initial setup

    def setup_game_variables(self):
        """Initialize/Reset game state variables for a new game session from menu."""
        self.game_state = STATE_MENU
        self.current_level_index = 0
        self.score = 0
        self.all_sprites = pygame.sprite.Group();
        self.platforms = pygame.sprite.Group();
        self.collectibles = pygame.sprite.Group();
        self.goal_group = pygame.sprite.GroupSingle()
        if not hasattr(self, 'player'):  # Create player only once
            self.player = Player(self)
        else:
            self.player.kill()  # Remove from any previous groups if resetting mid-game
            # Player state is reset in load_level

        # --- Reset Timers for a completely new game attempt ---
        self.level_elapsed_time = 0.0
        self.total_game_time = 0.0
        self.final_time = None  # Reset final time
        self.timer_active = False
        # --- High score is NOT reset here ---

        # --- Reset Power-up State ---
        self.coins_for_powerup_count = 0
        self.powerup_active = False
        self.powerup_end_time = 0
        # -----------------------------

        # Buttons... (Ensure button font is loaded before creating buttons)
        btn_center_x = SCREEN_WIDTH // 2
        self.play_button = Button(btn_center_x, 300, "Play", RED, self.button_font, self.button_img_normal,
                                  self.button_img_hover);
        self.controls_button = Button(btn_center_x, 400, "Controls", RED, self.button_font, self.button_img_normal,
                                      self.button_img_hover);
        self.exit_button = Button(btn_center_x, 500, "Exit", RED, self.button_font, self.button_img_normal,
                                  self.button_img_hover)
        self.menu_buttons = [self.play_button, self.controls_button, self.exit_button]
        self.back_button = Button(btn_center_x, SCREEN_HEIGHT - 100, "Back", BUTTON_TEXT_COLOR, self.button_font,
                                  self.button_img_normal, self.button_img_hover)
        self.next_level_button = Button(btn_center_x, SCREEN_HEIGHT // 2 + 50, "Next Level", BUTTON_TEXT_COLOR,
                                        self.button_font, self.button_img_normal, self.button_img_hover)
        self.restart_level_button = Button(btn_center_x, SCREEN_HEIGHT // 2 + 50, "Restart Level", BUTTON_TEXT_COLOR,
                                           self.button_font, self.button_img_normal, self.button_img_hover)
        self.main_menu_button = Button(btn_center_x, SCREEN_HEIGHT // 2 + 140, "Main Menu", BUTTON_TEXT_COLOR,
                                       self.button_font, self.button_img_normal, self.button_img_hover)
        self.win_main_menu_button = Button(btn_center_x, SCREEN_HEIGHT // 2 + 100, "Main Menu", BUTTON_TEXT_COLOR,
                                           self.button_font, self.button_img_normal, self.button_img_hover)

        # main.py -> Game class

    def load_highscore(self):
        """Loads the high score from the file, creating/fixing it if necessary."""
        score = float('inf')  # Default to infinity (means no valid score yet)
        filepath = HIGHSCORE_FILE
        try:
            # Create file with 'inf' if it doesn't exist
            if not os.path.exists(filepath):
                try:
                    with open(filepath, 'w') as f:
                        f.write(str(float('inf')))
                    print(f"Created high score file: {filepath}")
                except IOError as e_create:
                    print(f"ERROR: Could not create HS file: {e_create}");
                    return score

            # Read the file
            with open(filepath, 'r') as f:
                score_str = f.read().strip()
                if score_str:
                    try:
                        loaded_score = float(score_str)
                        # Treat 0.0 or less as invalid/no score yet, same as infinity
                        if loaded_score <= 0:
                            print(
                                f"Warning: Found score <= 0 ({loaded_score}) in {filepath}. Treating as no score yet.")
                            score = float('inf')
                            # Optionally fix the file now
                            # try:
                            #     with open(filepath, 'w') as f_fix: f_fix.write(str(float('inf')))
                            # except IOError: pass
                        else:
                            score = loaded_score  # Use the valid loaded score
                        print(f"Loaded high score: {format_time(score)} ({score})")
                    except ValueError:
                        print(f"ERROR: Invalid content '{score_str}' in {filepath}. Resetting.")
                        score = float('inf')
                        try:  # Attempt to fix the file
                            with open(filepath, 'w') as f_fix:
                                f_fix.write(str(float('inf')))
                        except IOError:
                            pass
                else:  # File was empty
                    print(f"Warning: High score file {filepath} empty. Resetting.")
                    score = float('inf')
                    try:  # Attempt to fix the file
                        with open(filepath, 'w') as f_fix:
                            f_fix.write(str(float('inf')))
                    except IOError:
                        pass
        except IOError as e_read:
            print(f"ERROR: Could not read HS file {filepath}: {e_read}");
            score = float('inf')
        except Exception as e:
            print(f"Unexpected error loading HS: {e}");
            score = float('inf')
        return score

    def save_highscore(self):
        """Saves the current valid high score to the file."""
        # Only save if high_score is a valid number (not infinity)
        if self.high_score != float('inf') and isinstance(self.high_score, (int, float)):
            try:
                with open(HIGHSCORE_FILE, 'w') as f:
                    f.write(str(self.high_score))  # Save the current best score
                    print(f"Saved new high score: {format_time(self.high_score)} ({self.high_score})")
            except IOError as e:
                print(f"ERROR: Could not save high score to {HIGHSCORE_FILE}: {e}")
        else:
            print("Skipping save: High score is still infinity or invalid.")

    def load_level(self, level_index):
        """Load sprites and player position, but DO NOT reset level timer here."""
        # Clear groups
        self.all_sprites.empty();
        self.platforms.empty();
        self.collectibles.empty();
        self.goal_group.empty()
        if level_index < 0 or level_index >= MAX_LEVELS: print(
            f"Invalid level index {level_index}"); self.game_state = STATE_MENU; return
        level_data = LEVELS[level_index]
        # Load level elements
        for p_data in level_data['platforms']: platform = Platform(self, *p_data); self.all_sprites.add(
            platform); self.platforms.add(platform)
        for c_data in level_data['collectibles']: collectible = Collectible(self.collectible_frames,
                                                                            *c_data); self.all_sprites.add(
            collectible); self.collectibles.add(collectible)
        goal = Goal(self, *level_data['goal']);
        self.all_sprites.add(goal);
        self.goal_group.add(goal)
        # Reset player state for the new level
        self.player.reset(*level_data['player_start'])
        # Add player to sprite group for drawing if not drawing manually (we are, so skip)
        # self.all_sprites.add(self.player)
        self.score = 0;
        # --- DO NOT reset level_elapsed_time or set timer_active here ---
        print(f"Level {level_index + 1} loaded. Total time before this level: {self.total_game_time:.3f}s")
        print(f"Level {level_index + 1} loaded. Coins towards powerup: {self.coins_for_powerup_count}, Active: {self.powerup_active}")
    def load_assets(self):
        """Load images, sounds, fonts, and animation frames."""
        # --- Fonts ---
        custom_font_loaded = False
        try:
            self.button_font = pygame.font.Font(BUTTON_FONT_PATH, BUTTON_FONT_SIZE)
            self.title_font = pygame.font.Font(BUTTON_FONT_PATH, TITLE_FONT_SIZE)
            self.controls_font = pygame.font.Font(BUTTON_FONT_PATH, CONTROLS_FONT_SIZE)
            self.info_font = pygame.font.Font(BUTTON_FONT_PATH, INFO_FONT_SIZE)
            print(f"Loaded custom font: {BUTTON_FONT_NAME}")
            custom_font_loaded = True
        except (FileNotFoundError, pygame.error) as e:
            print(f"Warning: Failed custom font '{BUTTON_FONT_PATH}'. Using default.\n{e}")
            self.button_font = pygame.font.Font(None, BUTTON_FONT_SIZE)
            self.title_font = pygame.font.Font(None, TITLE_FONT_SIZE)
            self.controls_font = pygame.font.Font(None, CONTROLS_FONT_SIZE)
            self.info_font = pygame.font.Font(None, INFO_FONT_SIZE)

        # --- Background ---
        try:
            original_background = pygame.image.load(os.path.join(IMG_DIR, BACKGROUND_IMG)).convert()
            original_width, original_height = original_background.get_size();
            target_width, target_height = SCREEN_WIDTH, SCREEN_HEIGHT
            if original_width != target_width or original_height != target_height:
                self.background_img = pygame.transform.scale(original_background, (target_width, target_height))
            else:
                self.background_img = original_background
        except pygame.error as e:
            print(f"CRITICAL ERROR loading background: {e}"); self.background_img = pygame.Surface(
                (SCREEN_WIDTH, SCREEN_HEIGHT)); self.background_img.fill(BLACK)

        # --- Other Assets ---
        try:
            self.platform_tile_img = pygame.image.load(os.path.join(IMG_DIR, PLATFORM_TILE_IMG)).convert()
        except pygame.error as e:
            print(f"Platform tile load error: {e}"); self.platform_tile_img = pygame.Surface((32, 32)).fill(GRAY)
        try:
            self.door_img = pygame.image.load(os.path.join(IMG_DIR, DOOR_IMG)).convert_alpha()
        except pygame.error as e:
            print(f"Door load error: {e}"); self.door_img = None

        # --- Buttons ---
        BUTTON_DISPLAY_WIDTH = 220;
        BUTTON_DISPLAY_HEIGHT = 80;
        temp_button_normal = None;
        temp_button_hover = None
        try:
            temp_button_normal = pygame.image.load(os.path.join(IMG_DIR,
                                                                BUTTON_NORMAL_IMG)).convert_alpha(); self.button_img_normal = pygame.transform.smoothscale(
                temp_button_normal, (BUTTON_DISPLAY_WIDTH, BUTTON_DISPLAY_HEIGHT))
        except pygame.error as e:
            print(f"CRITICAL button normal load/scale error: {e}"); self.button_img_normal = pygame.Surface(
                (BUTTON_DISPLAY_WIDTH, BUTTON_DISPLAY_HEIGHT)); self.button_img_normal.fill(BLUE)
        try:
            temp_button_hover = pygame.image.load(os.path.join(IMG_DIR,
                                                               BUTTON_HOVER_IMG)).convert_alpha(); self.button_img_hover = pygame.transform.smoothscale(
                temp_button_hover, (BUTTON_DISPLAY_WIDTH, BUTTON_DISPLAY_HEIGHT))
        except pygame.error as e:
            print(f"Warning: button hover load/scale error: {e}"); self.button_img_hover = None

        # --- Collectibles ---
        self.collectible_frames = [];
        print(f"Loading collectible frames '{COLLECTIBLE_IMG_PATTERN}'...")
        for i in range(COLLECTIBLE_IMG_COUNT):
            filename = COLLECTIBLE_IMG_PATTERN.format(i);
            filepath = os.path.join(IMG_DIR, filename)
            try:
                original_frame = pygame.image.load(
                    filepath).convert_alpha(); frame_scaled = pygame.transform.smoothscale(original_frame, (
                COLLECTIBLE_WIDTH, COLLECTIBLE_HEIGHT)); self.collectible_frames.append(frame_scaled)
            except (pygame.error, Exception) as e:
                print(f"Error loading/scaling collectible {filepath}: {e}"); break
        if not self.collectible_frames: print(
            "Warning: Collectible frames empty. Using fallback."); fallback = pygame.Surface(
            (COLLECTIBLE_WIDTH, COLLECTIBLE_HEIGHT)); fallback.fill(YELLOW); fallback.set_colorkey(
            BLACK); self.collectible_frames = [fallback]

        # --- Sounds ---
        try:
            pygame.mixer.music.load(os.path.join(SND_DIR, MUSIC_BACKGROUND)); pygame.mixer.music.set_volume(0.4)
        except pygame.error as e:
            print(f"Music load error: {e}")
        try:
            self.sfx_jump = pygame.mixer.Sound(os.path.join(SND_DIR, SFX_JUMP)); self.sfx_collect = pygame.mixer.Sound(
                os.path.join(SND_DIR, SFX_COLLECT)); self.sfx_jump.set_volume(0.6); self.sfx_collect.set_volume(0.7)
        except pygame.error as e:
            print(f"SFX load error: {e}"); self.sfx_jump = pygame.mixer.Sound(
                pygame.scrap.get("application/octet-stream")); self.sfx_collect = pygame.mixer.Sound(
                pygame.scrap.get("application/octet-stream"))

    def play_sound(self, sound):
        # ... () ...
        try:
            sound.play()
        except AttributeError:
            pass
        except pygame.error as e:
            print(f"Error playing sound: {e}")

    def toggle_fullscreen(self):
        # ... ( needed, but ensure it exists) ...
        self.fullscreen = not self.fullscreen;
        pygame.display.quit();
        pygame.display.init()
        if self.fullscreen:
            try:
                info = pygame.display.Info(); fs_width, fs_height = info.current_w, info.current_h; self.screen_flags = pygame.FULLSCREEN | pygame.SCALED; self.screen = pygame.display.set_mode(
                    (fs_width, fs_height), self.screen_flags)
            except Exception as e:
                print(
                    f"FS info error: {e}"); self.screen_flags = pygame.FULLSCREEN | pygame.SCALED; self.screen = pygame.display.set_mode(
                    (self.current_screen_width, self.current_screen_height), self.screen_flags)
        else:
            self.screen_flags = pygame.RESIZABLE | pygame.SCALED; self.screen = pygame.display.set_mode(
                (self.current_screen_width, self.current_screen_height), self.screen_flags)
        pygame.display.set_caption(TITLE);
        print("Display mode toggled.")

    def run(self):
        # ... () ...
        if pygame.mixer.music.get_busy() == 0 and hasattr(pygame.mixer.music, 'play'):
            try:
                pygame.mixer.music.play(loops=-1)
            except pygame.error as e:
                print(f"Error starting music: {e}")
        while self.running:
            self.dt = self.clock.tick(FPS) / 1000.0;
            self.events();
            self.update();
            self.draw()
        pygame.mixer.music.stop()

    def events(self):
        """Handle all input events and state changes affecting timer."""
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT: self.running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F11: self.toggle_fullscreen(); continue

            if self.game_state == STATE_MENU:
                if self.play_button.is_clicked(event):
                    self.setup_game_variables()  # Full reset for new game
                    self.current_level_index = 0
                    self.level_elapsed_time = 0.0  # Explicitly reset level time before load
                    self.timer_active = True  # Activate timer for first level
                    self.load_level(self.current_level_index)
                    self.game_state = STATE_PLAYING
                elif self.controls_button.is_clicked(event):
                    self.game_state = STATE_CONTROLS
                elif self.exit_button.is_clicked(event):
                    self.running = False

            elif self.game_state == STATE_CONTROLS:
                if self.back_button.is_clicked(event): self.game_state = STATE_MENU

            elif self.game_state == STATE_PLAYING:
                if event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_SPACE, pygame.K_UP, pygame.K_w): self.player.jump()
                    if event.key == pygame.K_r:
                        self.level_elapsed_time = 0.0  # Reset time for this level attempt
                        self.timer_active = True  # Ensure timer is active

                        self.coins_for_powerup_count = 0
                        self.powerup_active = False
                        self.powerup_end_time = 0
                        print("  Power-up state reset.")
                        self.load_level(self.current_level_index)  # Reload assets/player pos
                        self.game_state = STATE_PLAYING
                    if event.key == pygame.K_ESCAPE:
                        print(f"ESCAPE KEY: Going to Menu. Resetting game variables.")
                        self.high_score = self.load_highscore()  # Reload highscore first
                        self.setup_game_variables()  # Full reset including timers
                        self.game_state = STATE_MENU
                        if hasattr(pygame.mixer.music, 'rewind'): pygame.mixer.music.rewind()

            elif self.game_state == STATE_LEVEL_COMPLETE:
                if self.current_level_index + 1 < MAX_LEVELS and self.next_level_button.is_clicked(event):
                    # --- Accumulate time HERE ---
                    self.total_game_time += self.level_elapsed_time
                    print(f"NEXT LEVEL: Added {self.level_elapsed_time:.3f}s. New total = {self.total_game_time:.3f}s")
                    self.level_elapsed_time = 0.0  # Reset for next level immediately
                    # ---------------------------
                    self.current_level_index += 1
                    self.timer_active = True  # Activate timer for next level
                    self.load_level(self.current_level_index)  # Load assets/player pos
                    self.game_state = STATE_PLAYING
                elif self.main_menu_button.is_clicked(event):
                    self.high_score = self.load_highscore()  # Reload high score
                    self.setup_game_variables()  # Full reset
                    self.game_state = STATE_MENU
                    if hasattr(pygame.mixer.music, 'rewind'): pygame.mixer.music.rewind()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    self.level_elapsed_time = 0.0  # Reset time for this level attempt
                    self.timer_active = True  # Ensure timer is active
                    self.load_level(self.current_level_index)  # Reload assets/player pos
                    self.game_state = STATE_PLAYING

            elif self.game_state == STATE_GAME_OVER:
                if self.restart_level_button.is_clicked(event):
                    self.coins_for_powerup_count = 0
                    self.powerup_active = False
                    self.powerup_end_time = 0
                    print("  Power-up state reset.")
                    self.level_elapsed_time = 0.0  # Reset time for this level attempt
                    self.timer_active = True  # Ensure timer is active
                    self.load_level(self.current_level_index)  # Reload assets/player pos
                    self.game_state = STATE_PLAYING
                elif self.main_menu_button.is_clicked(event):
                    self.high_score = self.load_highscore()  # Reload high score
                    self.setup_game_variables()  # Full reset
                    self.game_state = STATE_MENU
                    if hasattr(pygame.mixer.music, 'rewind'): pygame.mixer.music.rewind()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    self.level_elapsed_time = 0.0  # Reset time for this level attempt
                    self.timer_active = True  # Ensure timer is active
                    self.load_level(self.current_level_index)  # Reload assets/player pos
                    self.game_state = STATE_PLAYING

            elif self.game_state == STATE_GAME_WON:
                if self.win_main_menu_button.is_clicked(event):
                    self.high_score = self.load_highscore()  # Reload high score
                    self.setup_game_variables()  # Full reset
                    self.game_state = STATE_MENU
                    if hasattr(pygame.mixer.music, 'rewind'): pygame.mixer.music.rewind()

        # Button Hover States ( needed)
        if self.game_state == STATE_MENU:
            [b.check_hover(mouse_pos) for b in self.menu_buttons]
        elif self.game_state == STATE_CONTROLS:
            self.back_button.check_hover(mouse_pos)
        elif self.game_state == STATE_LEVEL_COMPLETE:
            if self.current_level_index + 1 < MAX_LEVELS: self.next_level_button.check_hover(mouse_pos)
            self.main_menu_button.check_hover(mouse_pos)
        elif self.game_state == STATE_GAME_OVER:
            self.restart_level_button.check_hover(mouse_pos); self.main_menu_button.check_hover(mouse_pos)
        elif self.game_state == STATE_GAME_WON:
            self.win_main_menu_button.check_hover(mouse_pos)

    def update(self):
        """Update game logic, including timer and high score check."""
        # --- Power-up Timer Check ---
        now = pygame.time.get_ticks()
        if self.powerup_active and now >= self.powerup_end_time:
            print("Power-up Expired.")
            self.powerup_active = False
            # Player physics will automatically revert in the Player class
        # --------------------------

        # --- Timer Increment ---
        # Increment ONLY if timer is active (set during state transitions)
        if self.timer_active:
            self.level_elapsed_time += self.dt
        # ---------------------

        if self.game_state == STATE_PLAYING:
            self.player.update(self.platforms)

            self.all_sprites.update()  # Includes Collectible animation

            collected_items = pygame.sprite.spritecollide(self.player, self.collectibles, True)
            if collected_items:
                num_collected = len(collected_items)
                self.score += num_collected  # Increase general score display
            #if collected_items: self.score += len(collected_items);
                self.play_sound(self.sfx_collect)
                # Process each collected coin for power-up logic
                current_time = pygame.time.get_ticks()  # Get time again in case loop takes time
                for _ in range(num_collected):
                    if self.powerup_active:
                        self.powerup_end_time += POWERUP_EXTENSION_PER_COIN
                        print(
                            f"Power-up extended! New end: {(self.powerup_end_time - current_time) / 1000.0:.1f}s remaining")
                        # Add a sound effect for extension?
                    else:
                        # Work towards activating power-up
                        self.coins_for_powerup_count += 1
                        print(f"Coins towards power-up: {self.coins_for_powerup_count}/{COINS_NEEDED_FOR_POWERUP}")
                        if self.coins_for_powerup_count >= COINS_NEEDED_FOR_POWERUP:
                            print("Power-up Activated!")
                            self.powerup_active = True
                            self.powerup_end_time = current_time + POWERUP_INITIAL_DURATION
                            self.coins_for_powerup_count = 0  # Reset count for the *next* power-up
                            # Add a sound effect for activation?
                    # --- End Collectible / Power-up Logic ---
                # Extend current power-up duration
            # --- Goal Hit Logic ---
            if pygame.sprite.spritecollide(self.player, self.goal_group, False):
                if self.timer_active:
                    print(f"GOAL HIT: Pausing timer.")
                    self.timer_active = False
                current_level_final_time = self.level_elapsed_time  # Time for *this* level
                self.final_time = self.total_game_time + current_level_final_time  # Total time for *this run*

                if self.current_level_index + 1 >= MAX_LEVELS:  # Last level?
                    self.game_state = STATE_GAME_WON
                    print(f"Game Won! Final Total Time: {format_time(self.final_time)}")

                    # --- Check and Save High Score ---
                    # Compare final_time of this run with the loaded high_score
                    if self.final_time is not None and self.final_time < self.high_score:
                        print(f"New High Score! Beating {format_time(self.high_score)}")
                        self.high_score = self.final_time  # Update the high score in memory
                        self.save_highscore()  # Save the *updated* self.high_score to file
                    else:
                        print(f"Did not beat high score of {format_time(self.high_score)}")
                    # -------------------------------

                else:  # Not last level
                    self.game_state = STATE_LEVEL_COMPLETE
                print(
                    f"Level {self.current_level_index + 1} finished. Time for level: {format_time(current_level_final_time)}. State: {self.game_state}")
            # --- End Goal Hit ---

            # ... (Falling out logic) ...

            # Falling out
            if self.player.rect.top > SCREEN_HEIGHT + 50:
                if self.timer_active:  # Check if timer was running
                    print(f"FELL OUT: Pausing timer.")
                    self.timer_active = False  # PAUSE timer
                self.game_state = STATE_GAME_OVER
                print(f"Player fell out! State: {self.game_state}")
        # --- End STATE_PLAYING block ---

    def draw(self):
        # ... (draw method contents - s needed here for timer logic) ...
        self.screen.blit(self.background_img, (0, 0))
        if self.game_state == STATE_MENU:
            self.draw_menu()
        elif self.game_state == STATE_CONTROLS:
            self.draw_controls()
        elif self.game_state == STATE_PLAYING:
            self.draw_playing()
        elif self.game_state == STATE_LEVEL_COMPLETE:
            self.draw_level_complete()
        elif self.game_state == STATE_GAME_OVER:
            self.draw_game_over()
        elif self.game_state == STATE_GAME_WON:
            self.draw_game_won()
        pygame.display.flip()

    # --- Drawing Helper Methods ---
    def draw_menu(self):
        draw_text(TITLE, self.title_font, WHITE, self.screen, SCREEN_WIDTH // 2, 150, center=True)
        # --- Draw High Score ---
        highscore_str = format_time(self.high_score)  # Format the loaded high score
        draw_text(f"Best Time: {highscore_str}", self.info_font, YELLOW, self.screen, SCREEN_WIDTH // 2, 230,
                  center=True)
        # --- End High Score ---
        for button in self.menu_buttons: button.draw(self.screen)

    def draw_controls(self):
        # ... (s needed) ...
        self.screen.fill((128, 128, 128));
        draw_text("Controls", self.title_font, BLACK, self.screen, SCREEN_WIDTH // 2, 100, center=True)
        controls_text = [
            "A/Left: Move Left",
            "D/Right: Move Right",
            "W/Up/Space: Jump/Double Jump",
            "Hold Dir into wall: Wall Slide",
            "Jump on wall: Wall Jump",
            "R: Restart Level",
            "Esc: Main Menu",
            "",  # Blank line for spacing
            f"Collect {COINS_NEEDED_FOR_POWERUP} Scroll Coins:",  # Use the setting
            f" - Get Speed Boost ({POWERUP_SPEED_MULTIPLIER}x) for {POWERUP_INITIAL_DURATION / 1000.0:.0f}s!",
            # Use settings
            f" - Get Jump Boost ({POWERUP_JUMP_MULTIPLIER}x) for {POWERUP_INITIAL_DURATION / 1000.0:.0f}s!",
            # Use settings
            f" - Extra coins extend boost by {POWERUP_EXTENSION_PER_COIN / 1000.0:.0f}s each.",  # Use settings
            "",  # Blank line for spacing
            "Reach the Goal!"  # Goal text moved down
        ]
        y_offset = 150;
        x_pos = 100
        line_height = 35
        for i, line in enumerate(controls_text):
            # Highlight power-up lines (optional)
            clr = YELLOW if "Scroll Coin" in line or "Boost" in line else BLACK
            draw_text(line, self.controls_font, clr, self.screen, x_pos, y_offset)
            y_offset += line_height  # Use line_height variable

        self.back_button.rect.centery = SCREEN_HEIGHT - 80  # Adjusted Back button position slightly
        self.back_button.draw(self.screen)

    def draw_playing(self):
        # ... (drawing non-player sprites and player - ) ...
        non_player_sprites = pygame.sprite.Group([s for s in self.all_sprites if s != self.player]);
        non_player_sprites.draw(self.screen)
        image_draw_x = self.player.rect.centerx - (PLAYER_WIDTH // 2);
        image_draw_y = (self.player.rect.bottom - PLAYER_HEIGHT) + PLAYER_VISUAL_Y_OFFSET
        self.screen.blit(self.player.image, (image_draw_x, image_draw_y))
        #pygame.draw.rect(self.screen, (255, 0, 0), self.player.rect, 1) # Debug hitbox

        # --- Draw UI ---
        draw_text(f"Scrolls: {self.score}", self.info_font, WHITE, self.screen, 10, 10)
        draw_text(f"Level: {self.current_level_index + 1}/{MAX_LEVELS}", self.info_font, WHITE, self.screen,
                  SCREEN_WIDTH - 150, 10)
        # --- Calculate and Format Display Time ---
        # Display TOTAL accumulated time + current level's time
        display_time = self.total_game_time + self.level_elapsed_time
        time_str = format_time(display_time)
        # --- End Calculation ---
        draw_text(time_str, self.info_font, WHITE, self.screen, SCREEN_WIDTH // 2, 10,
                  center=True)  # Draw formatted time
        # --- Draw Power-up Indicator (Optional) ---
        if self.powerup_active:
            now = pygame.time.get_ticks()
            remaining_ms = max(0, self.powerup_end_time - now)  # Avoid negative display
            remaining_s = remaining_ms / 1000.0
            powerup_text = f"Boost: {remaining_s:.1f}s"
            # Position it somewhere visible, e.g., below the main timer
            draw_text(powerup_text, self.info_font, YELLOW, self.screen, SCREEN_WIDTH // 2, 40, center=True)
        elif self.coins_for_powerup_count > 0:
            # Optionally show progress towards next powerup
            powerup_progress_text = f"Boost: {self.coins_for_powerup_count}/{COINS_NEEDED_FOR_POWERUP}"
            draw_text(powerup_progress_text, self.info_font, GRAY, self.screen, SCREEN_WIDTH // 2, 40, center=True)
        # -----------------------------------------

    def draw_end_screen_overlay(self):
        # ... ( needed) ...
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA);
        overlay.fill((0, 0, 0, 180));
        self.screen.blit(overlay, (0, 0))

    def draw_level_complete(self):
        # ... (draw background sprites/player - ) ...
        non_player_sprites = pygame.sprite.Group([s for s in self.all_sprites if s != self.player]);
        non_player_sprites.draw(self.screen)
        image_draw_x = self.player.rect.centerx - (PLAYER_WIDTH // 2);
        image_draw_y = (self.player.rect.bottom - PLAYER_HEIGHT) + PLAYER_VISUAL_Y_OFFSET;
        self.screen.blit(self.player.image, (image_draw_x, image_draw_y))
        self.draw_end_screen_overlay();
        draw_text(f"Level {self.current_level_index + 1} Complete!", self.title_font, GREEN, self.screen,
                  SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100, center=True);
        # --- Display Time for Just Completed Level ---
        level_time_str = format_time(self.level_elapsed_time)  # Format the stored level time
        draw_text(f"Level Time: {level_time_str}", self.info_font, WHITE, self.screen, SCREEN_WIDTH // 2,
                  SCREEN_HEIGHT // 2 - 40, center=True)
        # --- Display Score ---
        draw_text(f"Coins Collected: {self.score}", self.info_font, WHITE, self.screen, SCREEN_WIDTH // 2,
                  SCREEN_HEIGHT // 2 + 0, center=True)  # Adjusted y slightly
        # --- Buttons ---
        if self.current_level_index + 1 < MAX_LEVELS: self.next_level_button.draw(self.screen)
        self.main_menu_button.draw(self.screen)

    def draw_game_over(self):
        # ... (draw background sprites/player - ) ...
        non_player_sprites = pygame.sprite.Group([s for s in self.all_sprites if s != self.player]);
        non_player_sprites.draw(self.screen)
        image_draw_x = self.player.rect.centerx - (PLAYER_WIDTH // 2);
        image_draw_y = (self.player.rect.bottom - PLAYER_HEIGHT) + PLAYER_VISUAL_Y_OFFSET;
        self.screen.blit(self.player.image, (image_draw_x, image_draw_y))
        self.draw_end_screen_overlay();
        draw_text("Game Over!", self.title_font, RED, self.screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100,
                  center=True);
        draw_text("You fell into the abyss...", self.info_font, WHITE, self.screen, SCREEN_WIDTH // 2,
                  SCREEN_HEIGHT // 2, center=True)  # Centered text
        self.restart_level_button.draw(self.screen);
        self.main_menu_button.draw(self.screen)

    def draw_game_won(self):
        self.screen.fill(LIGHT_BLUE);
        self.draw_end_screen_overlay()
        draw_text("Congratulations!", self.title_font, GREEN, self.screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 150,
                  center=True)
        draw_text("You have mastered the Way of the Shadow!", self.info_font, WHITE, self.screen, SCREEN_WIDTH // 2,
                  SCREEN_HEIGHT // 2 - 50, center=True)
        # --- Display Final Time ---
        final_time_str = format_time(self.final_time)  # Use the stored final time
        draw_text(f"Your Time: {final_time_str}", self.info_font, WHITE, self.screen, SCREEN_WIDTH // 2,
                  SCREEN_HEIGHT // 2 + 0, center=True)
        # --- Compare with High Score ---
        if self.final_time is not None and self.final_time <= self.high_score:
            draw_text("New Best Time!", self.info_font, YELLOW, self.screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 40,
                      center=True)
        else:
            highscore_str = format_time(self.high_score)
            draw_text(f"(Best: {highscore_str})", self.controls_font, GRAY, self.screen, SCREEN_WIDTH // 2,
                      SCREEN_HEIGHT // 2 + 40, center=True)
        # Position button lower
        self.win_main_menu_button.rect.centery = SCREEN_HEIGHT // 2 + 120
        self.win_main_menu_button.draw(self.screen)