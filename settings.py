# settings.py
import pygame
import os

# --- Asset Folders ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__)); ASSETS_DIR = os.path.join(BASE_DIR, 'assets'); IMG_DIR = os.path.join(ASSETS_DIR, 'images'); SND_DIR = os.path.join(ASSETS_DIR, 'sounds'); FONT_DIR = os.path.join(ASSETS_DIR, 'fonts')

# --- Screen ---
TITLE = "The Way of the Shadow"; SCREEN_WIDTH = 1000; SCREEN_HEIGHT = 700; FPS = 60

# --- Colors ---
WHITE=(255, 255, 255); BLACK=(0, 0, 0); RED=(255, 0, 0); BLUE=(0, 0, 255); GREEN=(0, 255, 0); YELLOW=(255, 255, 0); GRAY=(128, 128, 128); LIGHT_BLUE=(173, 216, 230); DARK_GRAY=(50, 50, 50)

# --- Game Object Images ---
PLAYER_IDLE_IMG = 'player_idle.png' # Renamed for clarity
PLAYER_RUN_IMG = 'run.png'          # <-- NEW: Running animation sheet
BACKGROUND_IMG = 'background.png'; PLATFORM_TILE_IMG = 'platform_tile.png'; DOOR_IMG = 'door.png'

# --- Collectible (Coin) Animation Settings ---
COLLECTIBLE_IMG_PATTERN = "coin_{}.png"; COLLECTIBLE_IMG_COUNT = 9
COLLECTIBLE_WIDTH = 30; COLLECTIBLE_HEIGHT = 30; COLLECTIBLE_ANIM_SPEED = 90

# --- Player Properties ---
PLAYER_WIDTH = 120; PLAYER_HEIGHT = 120 # Visual size
PLAYER_HITBOX_WIDTH = 30; PLAYER_HITBOX_HEIGHT = 45 # Collision size (Tune)
PLAYER_VISUAL_Y_OFFSET = 18 # Pixels to shift visual down (Tune)
PLAYER_ACC = 0.7; PLAYER_FRICTION = -0.15; PLAYER_GRAVITY = 0.6
PLAYER_JUMP_POWER = -13; PLAYER_DOUBLE_JUMP_POWER = -10
PLAYER_WALL_SLIDE_SPEED = 2; PLAYER_WALL_JUMP_X_POWER = 7; PLAYER_WALL_JUMP_Y_POWER = -10
MAX_FALL_SPEED = 15; MAX_RUN_SPEED = 7
PLAYER_IDLE_FRAMES = 10 # <-- NEW: Frames in idle sheet
PLAYER_RUN_FRAMES = 16  # <-- NEW: Frames in run sheet
PLAYER_ANIMATION_SPEED = 100 # Milliseconds per frame (Adjust for run/idle feel)

# --- Power-up Settings ---
COINS_NEEDED_FOR_POWERUP = 3
POWERUP_INITIAL_DURATION = 2500  # milliseconds (3 seconds)
POWERUP_EXTENSION_PER_COIN = 1000 # milliseconds (1 second)
POWERUP_SPEED_MULTIPLIER = 1.3
POWERUP_JUMP_MULTIPLIER = 1.2 # Doubling jump might be too much, adjust as needed

# --- UI Elements ---
BUTTON_NORMAL_IMG = 'button_retro_normal.png'; BUTTON_HOVER_IMG = 'button_retro_hover.png'
BUTTON_TEXT_COLOR = WHITE; BUTTON_FONT_NAME = 'pixel_font.ttf'; BUTTON_FONT_PATH = os.path.join(FONT_DIR, BUTTON_FONT_NAME)
HIGHSCORE_FILE = "highscore.txt" # <-- NEW: File to store best time

# --- Game States ---
STATE_MENU=0; STATE_CONTROLS=1; STATE_PLAYING=2; STATE_LEVEL_COMPLETE=3; STATE_GAME_OVER=4; STATE_GAME_WON=5

# --- Audio Files ---
MUSIC_BACKGROUND='music_background.ogg'; SFX_JUMP='sfx_jump.wav'; SFX_COLLECT='sfx_collect.wav'

# --- Fonts ---
TITLE_FONT_SIZE = 72; BUTTON_FONT_SIZE = 30; INFO_FONT_SIZE = 36; CONTROLS_FONT_SIZE = 24
