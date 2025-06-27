# levels.py

# Import screen dimensions needed for level definitions
from settings import SCREEN_WIDTH, SCREEN_HEIGHT

# Standard Goal Size (adjust if your door graphic needs different dimensions)
GOAL_W = 50
GOAL_H = 70
# Standard distance collectibles float above platform tops
COLLECT_OFFSET = 30

# Structure: {'platforms': [...], 'collectibles': [...], 'goal': (x, y, w, h), 'player_start': (x, y)}
LEVELS = [
    # Level 1 (Original - Adjusted Goal Size)
    {
        'platforms': [
            (0, SCREEN_HEIGHT - 40, SCREEN_WIDTH, 40), # Ground
            (200, SCREEN_HEIGHT - 150, 150, 20),       # Plat 1
            (450, SCREEN_HEIGHT - 280, 200, 20),       # Plat 2
            (50, SCREEN_HEIGHT - 400, 100, 20),        # Plat 3
            (700, SCREEN_HEIGHT - 450, 150, 20),       # Plat 4
            (SCREEN_WIDTH - 100, 100, 100, 200),       # Right Wall Upper
            (SCREEN_WIDTH - 100, 400, 100, 200),       # Right Wall Lower
            (0, 100, 100, SCREEN_HEIGHT - 140),        # Left Wall (Full except bottom)
            (300, 150, 200, 20)                        # Ceiling Platform
        ],
        'collectibles': [
            (275, SCREEN_HEIGHT - 150 - COLLECT_OFFSET), # Above Plat 1
            (550, SCREEN_HEIGHT - 280 - COLLECT_OFFSET), # Above Plat 2
            (120, SCREEN_HEIGHT - 400 - COLLECT_OFFSET), # Above Plat 3
            (775, SCREEN_HEIGHT - 450 - COLLECT_OFFSET), # Above Plat 4
            (400, 150 - COLLECT_OFFSET),                 # Above Ceiling Platform
            (SCREEN_WIDTH - 50, 80)                      # High near Right Wall (needs wall jump)
        ],
        # Positioned near top right, goal bottom roughly at y=50+70=120
        'goal': (SCREEN_WIDTH - 80, 50, GOAL_W, GOAL_H),
        'player_start': (150, SCREEN_HEIGHT - 80) # Start slightly above ground
    },
    # Level 2 (Focus on Jumps - Adjusted Goal Size)
    {
        'platforms': [
            (0, SCREEN_HEIGHT - 40, 200, 40),         # Start Ground
            (300, SCREEN_HEIGHT - 100, 150, 20),       # Plat 1
            (550, SCREEN_HEIGHT - 180, 150, 20),       # Plat 2
            (800, SCREEN_HEIGHT - 250, 150, 20),       # Plat 3
            (600, SCREEN_HEIGHT - 350, 100, 20),       # Plat 4 (Back Left)
            (350, SCREEN_HEIGHT - 450, 100, 20),       # Plat 5 (Back Left)
            (100, SCREEN_HEIGHT - 550, 100, 20),       # Plat 6 (Goal Plat)
            (SCREEN_WIDTH - 50, 0, 50, SCREEN_HEIGHT) # Right safety wall
        ],
        'collectibles': [
            (375, SCREEN_HEIGHT - 100 - COLLECT_OFFSET), # Above Plat 1
            (625, SCREEN_HEIGHT - 180 - COLLECT_OFFSET), # Above Plat 2
            (875, SCREEN_HEIGHT - 250 - COLLECT_OFFSET), # Above Plat 3
            (650, SCREEN_HEIGHT - 350 - COLLECT_OFFSET), # Above Plat 4
            (400, SCREEN_HEIGHT - 450 - COLLECT_OFFSET), # Above Plat 5
            (150, SCREEN_HEIGHT - 550 - COLLECT_OFFSET)  # Above Plat 6
        ],
        # Positioned on Plat 6 (top is H-550). Goal top = Plat top - Goal H.
        'goal': (125, SCREEN_HEIGHT - 550 - GOAL_H, GOAL_W, GOAL_H),
        'player_start': (50, SCREEN_HEIGHT - 80)
    },
    # Level 3 (Wall Jump Focus - Adjusted Goal Size)
    {
        'platforms': [
            (0, SCREEN_HEIGHT - 40, 100, 40),           # Start plat
            (SCREEN_WIDTH - 100, SCREEN_HEIGHT - 40, 100, 40), # End plat
            (200, 100, 50, SCREEN_HEIGHT - 150),         # Left Wall 1
            (400, 200, 50, SCREEN_HEIGHT - 250),         # Right Wall 1
            (600, 100, 50, SCREEN_HEIGHT - 150),         # Left Wall 2
            (800, 200, 50, SCREEN_HEIGHT - 250),         # Right Wall 2
            (0, 0, SCREEN_WIDTH, 20)                     # Ceiling
        ],
        'collectibles': [
            (170, SCREEN_HEIGHT - 100), # Between walls 1 and starting floor
            (380, SCREEN_HEIGHT - 200), # Between walls 1 lower
            (575, SCREEN_HEIGHT - 100), # Between walls 2
            (775, SCREEN_HEIGHT - 200), # Between walls 2 lower
            (500, 50)                   # Near Ceiling, centered
        ],
        # Positioned on the End Plat (top is H-40). Goal top = Plat top - Goal H
        'goal': (SCREEN_WIDTH - 75, SCREEN_HEIGHT - 40 - GOAL_H, GOAL_W, GOAL_H),
        'player_start': (50, SCREEN_HEIGHT - 80)
    },
     # Level 4 (Precision - Adjusted Goal Size)
    {
        'platforms': [
            (0, SCREEN_HEIGHT - 40, 150, 40),         # Start
            (250, SCREEN_HEIGHT - 100, 80, 20),       # P1
            (400, SCREEN_HEIGHT - 160, 80, 20),       # P2
            (550, SCREEN_HEIGHT - 220, 80, 20),       # P3
            (700, SCREEN_HEIGHT - 280, 80, 20),       # P4
            (550, SCREEN_HEIGHT - 400, 80, 20),       # P5 (Back Left)
            (400, SCREEN_HEIGHT - 460, 80, 20),       # P6
            (250, SCREEN_HEIGHT - 520, 80, 20),       # P7
            (100, SCREEN_HEIGHT - 580, 80, 20),       # P8 (Goal Plat)
            (SCREEN_WIDTH - 50, 0, 50, SCREEN_HEIGHT) # Right safety wall
        ],
        'collectibles': [
            (290, SCREEN_HEIGHT - 100 - COLLECT_OFFSET), # Above P1
            (440, SCREEN_HEIGHT - 160 - COLLECT_OFFSET), # Above P2
            (590, SCREEN_HEIGHT - 220 - COLLECT_OFFSET), # Above P3
            (740, SCREEN_HEIGHT - 280 - COLLECT_OFFSET), # Above P4
            (590, SCREEN_HEIGHT - 400 - COLLECT_OFFSET), # Above P5
            (440, SCREEN_HEIGHT - 460 - COLLECT_OFFSET), # Above P6
            (290, SCREEN_HEIGHT - 520 - COLLECT_OFFSET), # Above P7
            (140, SCREEN_HEIGHT - 580 - COLLECT_OFFSET), # Above P8
        ],
        # Positioned on P8 (top is H-580). Goal top = Plat top - Goal H.
        'goal': (115, SCREEN_HEIGHT - 580 - GOAL_H, GOAL_W, GOAL_H),
        'player_start': (50, SCREEN_HEIGHT - 80)
    },
    # Level 5 (Vertical Ascent - Adjusted Goal Size)
    {
        'platforms': [
            (0, SCREEN_HEIGHT - 40, SCREEN_WIDTH, 40), # Ground
            (100, SCREEN_HEIGHT - 150, 100, 20),       # L1
            (SCREEN_WIDTH - 200, SCREEN_HEIGHT - 250, 100, 20), # R1
            (100, SCREEN_HEIGHT - 350, 100, 20),       # L2
            (SCREEN_WIDTH - 200, SCREEN_HEIGHT - 450, 100, 20), # R2
            (100, SCREEN_HEIGHT - 550, 100, 20),       # L3
            (SCREEN_WIDTH - 200, SCREEN_HEIGHT - 650, 100, 20), # R3 (Goal Plat)
            (0, 0, 20, SCREEN_HEIGHT),                 # Left wall
            (SCREEN_WIDTH-20, 0, 20, SCREEN_HEIGHT)    # Right wall
        ],
        'collectibles': [
            (150, SCREEN_HEIGHT - 150 - COLLECT_OFFSET), # Above L1
            (SCREEN_WIDTH - 150, SCREEN_HEIGHT - 250 - COLLECT_OFFSET), # Above R1
            (150, SCREEN_HEIGHT - 350 - COLLECT_OFFSET), # Above L2
            (SCREEN_WIDTH - 150, SCREEN_HEIGHT - 450 - COLLECT_OFFSET), # Above R2
            (150, SCREEN_HEIGHT - 550 - COLLECT_OFFSET)  # Above L3
        ],
        # Positioned on R3 (top is H-650). Goal top = Plat top - Goal H.
        'goal': (SCREEN_WIDTH - 175, SCREEN_HEIGHT - 650 - GOAL_H, GOAL_W, GOAL_H),
        'player_start': (SCREEN_WIDTH / 2, SCREEN_HEIGHT - 80) # Center start
    },
    # Level 6 (Complex Layout - Adjusted Goal Size)
    {
        'platforms': [
            (0, SCREEN_HEIGHT - 40, SCREEN_WIDTH, 40), # Ground
            (100, SCREEN_HEIGHT - 140, 100, 20),       # Low L
            (300, SCREEN_HEIGHT - 240, 100, 20),       # Low R
            (50, 400, 100, 20),                        # Mid L
            (SCREEN_WIDTH - 150, 400, 100, 20),        # Mid R
            (300, 250, 400, 20),                       # Center High
            (SCREEN_WIDTH - 100, 100, 100, 200),       # Right wall top
            (0, 100, 100, 200),                        # Left wall top
            (SCREEN_WIDTH / 2 - 50, 100, 100, 20)      # Top Mid (Goal Plat)
        ],
        'collectibles': [
            (150, SCREEN_HEIGHT - 140 - COLLECT_OFFSET), # Above Low L
            (350, SCREEN_HEIGHT - 240 - COLLECT_OFFSET), # Above Low R
            (100, 400 - COLLECT_OFFSET),                 # Above Mid L
            (SCREEN_WIDTH - 100, 400 - COLLECT_OFFSET),  # Above Mid R
            (400, 250 - COLLECT_OFFSET),                 # Above Center High L
            (600, 250 - COLLECT_OFFSET),                 # Above Center High R
            (50, 75),                                   # High Left Wall Area
            (SCREEN_WIDTH - 50, 75)                     # High Right Wall Area
        ],
        # Positioned on Top Mid Plat (top is 100). Goal top = Plat top - Goal H.
        'goal': (SCREEN_WIDTH / 2 - GOAL_W / 2, 100 - GOAL_H, GOAL_W, GOAL_H),
        'player_start': (50, SCREEN_HEIGHT - 80)
    },
    # Level 7 (Simple Ascent - Adjusted Goal)
    {
        'platforms': [
            (0, SCREEN_HEIGHT - 40, SCREEN_WIDTH, 40), # Ground
            (200, 500, 100, 20),                       # P1
            (400, 400, 100, 20),                       # P2
            (600, 300, 100, 20)                        # P3 (Goal Plat)
        ],
        'collectibles': [
            (250, 500 - COLLECT_OFFSET), # Above P1
            (450, 400 - COLLECT_OFFSET), # Above P2
            (650, 300 - COLLECT_OFFSET)  # Above P3
        ],
        # Positioned on P3 (top is 300). Goal top = Plat top - Goal H.
        'goal': (625, 300 - GOAL_H, GOAL_W, GOAL_H),
        'player_start': (50, SCREEN_HEIGHT - 80)
    },
    # Level 8 (Vertical ZigZag - Adjusted Goal Size)
    {
        'platforms': [
            (0, SCREEN_HEIGHT - 40, 100, 40),   # Start
            (200, SCREEN_HEIGHT-100, 50, 20),  # R1
            (0, SCREEN_HEIGHT-200, 50, 20),    # L1
            (200, SCREEN_HEIGHT-300, 50, 20),  # R2
            (0, SCREEN_HEIGHT-400, 50, 20),    # L2
            (200, SCREEN_HEIGHT-500, 50, 20),  # R3 (Top-ish)
            (SCREEN_WIDTH - 50, 0, 50, SCREEN_HEIGHT) # Right Wall
        ],
        'collectibles': [
            (225, SCREEN_HEIGHT-100 - COLLECT_OFFSET), # Above R1
            (25, SCREEN_HEIGHT-200 - COLLECT_OFFSET),  # Above L1
            (225, SCREEN_HEIGHT-300 - COLLECT_OFFSET), # Above R2
            (25, SCREEN_HEIGHT-400 - COLLECT_OFFSET),  # Above L2
            (225, SCREEN_HEIGHT-500 - COLLECT_OFFSET)  # Above R3
        ],
        # Positioned high near right wall, requires wall jump from R3 or right wall
        'goal': (SCREEN_WIDTH - 100, 80, GOAL_W, GOAL_H),
        'player_start': (50, SCREEN_HEIGHT - 80)
    },
    # Level 9 (Diagonal Ascent - Adjusted Goal Size)
    {
        # Using list comprehension for platforms and collectibles
        'platforms': [(x*100 + 50, SCREEN_HEIGHT - 40 - i*60, 80, 20) for i, x in enumerate(range(10))],
        'collectibles': [(x*100 + 50 + 40, SCREEN_HEIGHT - 40 - i*60 - COLLECT_OFFSET) for i, x in enumerate(range(10))],
        # Goal on the last platform (i=9 -> x=9 -> plat_x=950, plat_y=H-40-540=120)
        # Goal top = 120 - Goal H
        'goal': (950 + 40 - GOAL_W/2, 120 - GOAL_H, GOAL_W, GOAL_H),
        'player_start': (40, SCREEN_HEIGHT - 80)
    },
    # Level 10 (Final Challenge - Adjusted Collectible & Goal)
    {
        'platforms': [
            (0, SCREEN_HEIGHT - 40, 150, 40),             # Start
            (300, SCREEN_HEIGHT - 100, 100, 20),           # Jump 1
            (150, SCREEN_HEIGHT - 200, 50, 20),            # Jump 2 (Small Left)
            (0, 100, 50, SCREEN_HEIGHT - 140),             # Left wall run
            (200, SCREEN_HEIGHT - 350, 100, 20),           # Mid Plat 1
            (400, SCREEN_HEIGHT - 450, 100, 20),           # Mid Plat 2
            (600, SCREEN_HEIGHT - 550, 100, 20),           # Mid Plat 3
            (SCREEN_WIDTH - 50, 100, 50, SCREEN_HEIGHT - 100), # Right Wall
            (SCREEN_WIDTH - 150, 50, 100, 20)             # Goal Plat (Top Right)
        ],
        'collectibles': [
            (350, SCREEN_HEIGHT-100 - COLLECT_OFFSET),  # Above Jump 1
            (175, SCREEN_HEIGHT-200 - COLLECT_OFFSET),  # Above Jump 2
            (70, 150),                                 # High on Left Wall
            (250, SCREEN_HEIGHT-350 - COLLECT_OFFSET),  # Above Mid Plat 1
            (450, SCREEN_HEIGHT-450 - COLLECT_OFFSET),  # Above Mid Plat 2
            (650, SCREEN_HEIGHT-550 - COLLECT_OFFSET),  # Above Mid Plat 3
            (SCREEN_WIDTH - 75, 150)                   # High on Right Wall
        ],
        # Goal on Goal Plat (top = 50). Goal top = Plat top - Goal H.
        'goal': (SCREEN_WIDTH - 100, 50 - GOAL_H, GOAL_W, GOAL_H),
        'player_start': (50, SCREEN_HEIGHT - 80)
    },
]

MAX_LEVELS = len(LEVELS)