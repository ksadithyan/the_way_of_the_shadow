# sprites.py

import pygame
import os
from settings import * # Import all settings

vec = pygame.math.Vector2

# --- Player Class ---
class Player(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        self.game = game

        # --- Animation Frame Lists ---
        self.idle_frames_r = []
        self.idle_frames_l = []
        self.run_frames_r = []  # <-- NEW
        self.run_frames_l = []  # <-- NEW
        # ---------------------------

        self.load_images() # Load images, scale them to PLAYER_WIDTH/HEIGHT for visuals

        # --- Define the HITBOX rect ---
        self.rect = pygame.Rect(0, 0, PLAYER_HITBOX_WIDTH, PLAYER_HITBOX_HEIGHT)

        # --- Visual Image ---
        # Initialize with first idle frame if available
        self.image = self.idle_frames_r[0] if self.idle_frames_r else pygame.Surface((PLAYER_WIDTH, PLAYER_HEIGHT))
        if not self.idle_frames_r: print("CRITICAL: Player idle frames failed loading.")

        try: self.mask = pygame.mask.from_surface(self.image)
        except: self.mask = None

        # Movement vectors
        self.pos = vec(0, 0); self.vel = vec(0, 0); self.acc = vec(0, 0)

        # Animation state
        self.current_frame_index = 0; self.last_anim_update = pygame.time.get_ticks(); self.facing_right = True
        self.current_action = 'idle' # Track if 'idle' or 'run'
        self.last_action = 'idle'

        # Gameplay state variables
        self.on_ground = False; self.jumps_left = 2; self.wall_sliding = False; self.wall_slide_side = 0

    def load_images(self):
        """Loads sprite sheets and extracts animation frames, scaled for visuals."""
        print("Loading player assets...")

        # --- Load IDLE Frames ---
        idle_sheet_path = os.path.join(IMG_DIR, PLAYER_IDLE_IMG)
        try:
            idle_spritesheet = pygame.image.load(idle_sheet_path).convert_alpha()
            self._extract_frames(idle_spritesheet, PLAYER_IDLE_FRAMES, self.idle_frames_r, self.idle_frames_l, "Idle")
        except pygame.error as e:
            print(f"Error loading PLAYER IDLE sheet '{PLAYER_IDLE_IMG}': {e}")
            self._add_fallback_frame(self.idle_frames_r, self.idle_frames_l)

        # --- Load RUN Frames ---
        run_sheet_path = os.path.join(IMG_DIR, PLAYER_RUN_IMG)
        try:
            run_spritesheet = pygame.image.load(run_sheet_path).convert_alpha()
            self._extract_frames(run_spritesheet, PLAYER_RUN_FRAMES, self.run_frames_r, self.run_frames_l, "Run")
        except pygame.error as e:
            print(f"Error loading PLAYER RUN sheet '{PLAYER_RUN_IMG}': {e}")
            self._add_fallback_frame(self.run_frames_r, self.run_frames_l)

        # Final check
        if not self.idle_frames_r: print("WARNING: Player idle frames list is empty!")
        if not self.run_frames_r: print("WARNING: Player run frames list is empty!")


    def _extract_frames(self, spritesheet, num_frames, frame_list_r, frame_list_l, anim_name):
        """Helper to extract, scale, and append frames from a sheet."""
        print(f"  Extracting {anim_name} frames ({num_frames})...")
        if spritesheet.get_width() < num_frames or num_frames <= 0:
             print(f"    Error: Invalid frames/sheet width for {anim_name}.")
             self._add_fallback_frame(frame_list_r, frame_list_l)
             return
        frame_width = spritesheet.get_width() // num_frames
        frame_height = spritesheet.get_height()
        print(f"    Sheet: {spritesheet.get_size()}, Frame: {frame_width}x{frame_height}, Scaling to: {PLAYER_WIDTH}x{PLAYER_HEIGHT}")

        for i in range(num_frames):
            x = i * frame_width; frame_rect = pygame.Rect(x, 0, frame_width, frame_height)
            try:
                frame_surface = spritesheet.subsurface(frame_rect)
                if frame_surface.get_width() != PLAYER_WIDTH or frame_surface.get_height() != PLAYER_HEIGHT:
                    # Use smoothscale for potentially better results when scaling non-integer amounts
                    frame_surface = pygame.transform.smoothscale(frame_surface, (PLAYER_WIDTH, PLAYER_HEIGHT))
                frame_list_r.append(frame_surface)
                frame_list_l.append(pygame.transform.flip(frame_surface, True, False))
            except ValueError as e:
                print(f"    Error processing {anim_name} frame {i}: {e}")
                self._add_fallback_frame(frame_list_r, frame_list_l) # Add fallback if one frame fails
                break # Stop processing this sheet

    def _add_fallback_frame(self, frame_list_r, frame_list_l):
         """Adds a fallback red square if loading fails."""
         if not frame_list_r: # Only add if list is currently empty
             print("    Adding fallback frame.")
             fallback = pygame.Surface((PLAYER_WIDTH, PLAYER_HEIGHT)); fallback.fill(RED); fallback.set_colorkey(BLACK)
             frame_list_r.append(fallback)
             frame_list_l.append(fallback)


    def reset(self, x, y):
        """Resets player state and positions the HITBOX rect correctly."""
        self.pos = vec(x, y); self.vel = vec(0, 0); self.acc = vec(0, 0)
        self.on_ground = False; self.jumps_left = 2; self.wall_sliding = False; self.wall_slide_side = 0
        self.facing_right = True

        # --- Reset Animation State ---
        self.current_frame_index = 0
        self.current_action = 'idle'
        self.last_action = 'idle'
        if self.idle_frames_r: self.image = self.idle_frames_r[0] # Start with idle image
        else: fallback = pygame.Surface((PLAYER_WIDTH, PLAYER_HEIGHT)); fallback.fill(RED); self.image = fallback # Fallback
        self.last_anim_update = pygame.time.get_ticks()
        # ---------------------------

        self.rect.topleft = self.pos # Position hitbox
        # --- Ground Snapping Logic ---
        ground_platform = None; possible_grounds = [p for p in self.game.platforms if p.rect.left < self.rect.centerx < p.rect.right and p.rect.top >= self.pos.y]
        if possible_grounds: ground_platform = min(possible_grounds, key=lambda p: p.rect.top)
        if ground_platform: self.rect.bottom = ground_platform.rect.top
        # ---------------------------
        self.pos.x = self.rect.x; self.pos.y = self.rect.y; # Sync pos to potentially snapped rect
        # --- Immediate Ground Check ---
        self.check_collisions_y(self.game.platforms); self.vel = vec(0, 0)
        self.pos.x = self.rect.x; self.pos.y = self.rect.y # Final sync
        print(f"Player reset. Hitbox: {self.rect.topleft}, OnGround: {self.on_ground}")

    def animate(self):
        """Switches between idle and run animations and updates the current frame."""
        now = pygame.time.get_ticks()

        # --- Determine Current Action ---
        # Simple check: Running if moving horizontally on ground or in air (can adjust later)
        if abs(self.vel.x) > 0.1:
             self.current_action = 'run'
        else:
             self.current_action = 'idle'
        # Add more checks here later for jumping, falling, wallsliding etc.
        # -----------------------------

        # --- Select Frame List ---
        if self.current_action == 'run':
            frame_list = self.run_frames_r if self.facing_right else self.run_frames_l
        else: # Default to idle
            frame_list = self.idle_frames_r if self.facing_right else self.idle_frames_l

        # Use fallback idle if specific animation list is empty
        if not frame_list and self.idle_frames_r:
             frame_list = self.idle_frames_r if self.facing_right else self.idle_frames_l
        elif not frame_list:
             return # Cannot animate if no frames loaded at all

        # --- Reset Frame Index if Action Changed ---
        if self.current_action != self.last_action:
            self.current_frame_index = 0
            self.last_action = self.current_action
        # -----------------------------------------

        # --- Update Frame ---
        if now - self.last_anim_update > PLAYER_ANIMATION_SPEED:
            self.last_anim_update = now
            self.current_frame_index = (self.current_frame_index + 1) % len(frame_list)
            # Get the new image based on action, direction, and frame index
            new_image = frame_list[self.current_frame_index]
            # Update the visual image (hitbox rect remains unchanged)
            self.image = new_image
            # Update mask if needed (optional)
            # try: self.mask = pygame.mask.from_surface(self.image)
            # except: pass # Ignore errors if mask fails briefly

    # --- jump, update, check_collisions_x, check_collisions_y ---
    # Ensure the 'update' method calls self.animate() at the start
    # Ensure the wall slide check logic is correct (from previous fixes)

    def jump(self):
        # Determine multiplier based on power-up status from the Game object
        jump_mult = POWERUP_JUMP_MULTIPLIER if self.game.powerup_active else 1.0

        can_jump = False
        if self.wall_sliding:
            # Apply multiplier to wall jump vertical power
            self.vel.y = PLAYER_WALL_JUMP_Y_POWER * jump_mult
            # Horizontal wall jump usually isn't multiplied
            self.vel.x = PLAYER_WALL_JUMP_X_POWER * -self.wall_slide_side
            self.wall_sliding = False;
            self.jumps_left = 1;  # <--- THIS IS THE KEY POINT
            self.on_ground = False;
            can_jump = True;
            self.facing_right = self.vel.x > 0
        elif self.on_ground:
            # Apply multiplier to initial jump power
            self.vel.y = PLAYER_JUMP_POWER * jump_mult
            self.jumps_left -= 1;  # Starts at 2, becomes 1
            self.on_ground = False;
            can_jump = True
        elif self.jumps_left > 0:  # This handles the double jump
            # Apply multiplier to double jump power
            self.vel.y = PLAYER_DOUBLE_JUMP_POWER * jump_mult
            self.jumps_left -= 1;  # Becomes 0 if it was 1
            self.on_ground = False;
            can_jump = True

        if can_jump and hasattr(self.game, 'sfx_jump'):
            self.game.play_sound(self.game.sfx_jump)
    def update(self, platforms):
        self.animate()  # Animate first
        original_speed_mult = 1  # Store the real multiplier
        # --- Determine Multipliers ---
        speed_mult = POWERUP_SPEED_MULTIPLIER if self.game.powerup_active else 1.0
        # Jump multiplier is handled directly in the jump() method

        # --- Apply Input and Acceleration ---
        keys = pygame.key.get_pressed()
        self.acc = vec(0, PLAYER_GRAVITY)  # Start with gravity
        moving_sideways = False

        # Apply speed multiplier to horizontal acceleration from input
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.acc.x = -PLAYER_ACC * speed_mult
            moving_sideways = True
            self.facing_right = False
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.acc.x = PLAYER_ACC * speed_mult
            moving_sideways = True
            self.facing_right = True

        # --- Apply Friction ---
        # Friction usually isn't multiplied by the power-up, but you could if you wanted
        if not moving_sideways:
            self.acc.x += self.vel.x * PLAYER_FRICTION

        # --- Update Velocity ---
        self.vel += self.acc

        # --- Cap Horizontal Speed ---
        # Apply speed multiplier to the maximum running speed
        current_max_speed = MAX_RUN_SPEED * speed_mult
        if abs(self.vel.x) > current_max_speed:
            self.vel.x = current_max_speed if self.vel.x > 0 else -current_max_speed

        # Stop small horizontal drift
        if abs(self.vel.x) < 0.1: self.vel.x = 0

        # --- Wall Sliding Check ---
        # (Wall slide logic remains the same - it checks keys/collision, doesn't directly use multipliers here)
        self.wall_sliding = False;
        self.wall_slide_side = 0;
        hits_l = None
        # --- TEMPORARY TEST ---
        # speed_mult = 1.0 # Force normal speed ONLY for the collision check? (This won't work directly as velocity is already high)
        # Instead, let's focus on the collision check pixel distance
        check_dist = 2 if original_speed_mult > 1.0 else 1  # Check 2 pixels out if boosted?
        # --- END TEMP TEST ---
        if not self.on_ground and self.vel.y > 0:
            print(f"Wall slide check. SpeedMult: {original_speed_mult}, CheckDist: {check_dist}")  # Debug
            # Use check_dist instead of 1
            self.rect.x += check_dist;
            hits_r = pygame.sprite.spritecollide(self, platforms, False);
            self.rect.x -= check_dist
            print(f"  Checking right wall ({check_dist}px)... Hits_R: {bool(hits_r)}")

            if hits_r and (keys[pygame.K_RIGHT] or keys[pygame.K_d]):
                self.wall_sliding = True;
                self.wall_slide_side = 1
                print("    >>> Sliding RIGHT")

            elif (keys[pygame.K_LEFT] or keys[pygame.K_a]):
                # Use check_dist instead of 1
                self.rect.x -= check_dist;
                hits_l = pygame.sprite.spritecollide(self, platforms, False);
                self.rect.x += check_dist
                print(f"  Checking left wall ({check_dist}px)... Hits_L: {bool(hits_l)}")
                if hits_l:
                    self.wall_sliding = True;
                    self.wall_slide_side = -1
                    print("    >>> Sliding LEFT")
            # ... (rest of wall slide checking logic) ...
            if self.wall_sliding:
                # Wall slide speed itself usually isn't affected by power-up, but you could multiply here too
                self.vel.y = min(self.vel.y, PLAYER_WALL_SLIDE_SPEED)
                self.jumps_left = 1

        # --- Apply Movement and Check Collisions ---
        # Horizontal
        self.pos.x += self.vel.x + 0.5 * self.acc.x
        self.rect.x = round(self.pos.x)
        self.check_collisions_x(platforms)

        # Vertical
        self.pos.y += self.vel.y + 0.5 * self.acc.y
        self.rect.y = round(self.pos.y)
        if not self.wall_sliding: self.on_ground = False
        self.check_collisions_y(platforms)

        # Apply Max Fall Speed AFTER Y collisions
        # Max fall speed usually isn't affected by power-ups, but you could multiply MAX_FALL_SPEED here if desired
        if self.vel.y > MAX_FALL_SPEED: self.vel.y = MAX_FALL_SPEED

    def check_collisions_x(self, platforms):
        collisions = pygame.sprite.spritecollide(self, platforms, False)
        for platform in collisions:
            if self.vel.x > 0: self.rect.right = platform.rect.left
            elif self.vel.x < 0: self.rect.left = platform.rect.right
            self.pos.x = self.rect.x; self.vel.x = 0

    def check_collisions_y(self, platforms):
        collisions = pygame.sprite.spritecollide(self, platforms, False); collisions.sort(key=lambda p: p.rect.top)
        original_on_ground = self.on_ground; landed_this_frame = False; hit_ceiling_this_frame = False
        for platform in collisions:
            if self.vel.y > 0 and self.rect.bottom > platform.rect.top:
                 if self.rect.centery < platform.rect.top + (PLAYER_HITBOX_HEIGHT / 2): # Check vertical alignment
                    self.rect.bottom = platform.rect.top; landed_this_frame = True; self.vel.y = 0; self.pos.y = self.rect.y
            elif self.vel.y < 0 and self.rect.top < platform.rect.bottom:
                 if self.rect.centery > platform.rect.bottom - (PLAYER_HITBOX_HEIGHT / 2): # Check vertical alignment
                    self.rect.top = platform.rect.bottom; hit_ceiling_this_frame = True; self.vel.y = 0; self.pos.y = self.rect.y
        if landed_this_frame: self.on_ground = True
        if landed_this_frame and self.wall_sliding: self.wall_sliding = False; self.wall_slide_side = 0
        if landed_this_frame: self.jumps_left = 2
        # No need for `elif hit_ceiling_this_frame: self.vel.y = 0` as it's done in loop


# --- Collectible Class ---
class Collectible(pygame.sprite.Sprite):
    # ... (Collectible class code - unchanged) ...
    def __init__(self, frames, x, y):
        super().__init__(); self.frames = frames
        if not self.frames: print("Error: Collectible init empty frames."); self.image = pygame.Surface([COLLECTIBLE_WIDTH, COLLECTIBLE_HEIGHT]); self.image.fill(YELLOW); self.image.set_colorkey(BLACK); self.frames = [self.image]
        else: self.image = self.frames[0]
        self.rect = self.image.get_rect(); self.rect.center = (x, y)
        self.current_frame_index = 0; self.last_anim_update = pygame.time.get_ticks()

    def update(self):
        now = pygame.time.get_ticks();
        if not self.frames: return
        if now - self.last_anim_update > COLLECTIBLE_ANIM_SPEED:
            self.last_anim_update = now; old_center = self.rect.center
            self.current_frame_index = (self.current_frame_index + 1) % len(self.frames)
            self.image = self.frames[self.current_frame_index]
            self.rect = self.image.get_rect(); self.rect.center = old_center

# --- Platform Class ---
class Platform(pygame.sprite.Sprite):
    # ... (Platform class code using tiling - unchanged) ...
    def __init__(self, game, x, y, width, height):
        super().__init__(); self.game = game; self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.Surface(self.rect.size, pygame.SRCALPHA).convert_alpha(); self.image.fill((0, 0, 0, 0))
        if hasattr(self.game, 'platform_tile_img') and self.game.platform_tile_img:
            tile_img = self.game.platform_tile_img; tile_w, tile_h = tile_img.get_size()
            if tile_w > 0 and tile_h > 0:
                for tile_x in range(0, self.rect.width, tile_w):
                    for tile_y in range(0, self.rect.height, tile_h): self.image.blit(tile_img, (tile_x, tile_y))
            else: print("Warning: Platform tile zero dimension."); self.image.fill(GRAY)
        else: print("Warning: Platform tile not loaded."); self.image.fill(GRAY)

# --- Goal Class ---
class Goal(pygame.sprite.Sprite):
    # ... (Goal class code using door image - unchanged) ...
     def __init__(self, game, x, y, width, height):
        super().__init__(); self.game = game
        self.image = pygame.Surface([width, height]); self.image.fill(GREEN); self.image.set_colorkey(BLACK); fallback_used = True
        if hasattr(self.game, 'door_img') and self.game.door_img:
            try: scaled_door_img = pygame.transform.smoothscale(self.game.door_img, (width, height)); self.image = scaled_door_img; fallback_used = False
            except (ValueError, TypeError, pygame.error) as e: print(f"Error scaling door: {e}")
        if fallback_used: print(f"Warning: Using fallback goal at ({x},{y}).")
        self.rect = self.image.get_rect(); self.rect.topleft = (x, y)