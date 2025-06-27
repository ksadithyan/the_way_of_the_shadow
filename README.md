

**Shadow Scrolls - A 2D Pygame Platformer**

A fast-paced 2D platformer built with Python and Pygame. The goal is to navigate challenging levels, collect all the "Scroll Coins", and reach the goal in the fastest time possible, utilizing advanced movement like wall jumps and a temporary speed-boost power-up.


**Features**

Advanced Player Movement: Responsive controls including running, jumping, double jumping, wall sliding, and wall jumping.

Physics Engine: Custom physics implementation for acceleration, friction, and gravity.

Multi-Level System: Levels are loaded from a central configuration file (levels.py), making it easy to add more.

Timer & High Score: An in-game timer tracks your speed. The best overall time is saved to highscore.txt and persists between sessions.

Power-Up System: Collect 3 scrolls to activate a speed and jump boost for a limited time. Collecting more scrolls while the boost is active extends its duration.

Complete Game Loop: Features a main menu, controls screen, gameplay state, level complete/game over screens, and a final win screen.

UI Elements: Includes a Heads-Up Display (HUD) for score/timer and custom-image buttons with hover effects.

Animation & Sound: Animated sprites for the player and collectibles, plus background music and sound effects for key actions.

Modular Codebase: The project is organized into separate modules for settings, sprites, levels, and UI, promoting clean and readable code.


**Technologies Used**

Python 3.12.5

Pygame 2.5.2


**How to Run**

**1. Prerequisites**
Make sure you have Python 3.12.5 installed on your system.
Make sure you have Pip (Python's package installer) available.


**2. Installation & Setup**

**Clone the repository:**
git clone https://github.com/ksadithyan/the_way_of_the_shadow.git


**Navigate to the project directory:**
cd the_way_of_the_shadow


**Install dependencies:**
Run the following command in your terminal to install Pygame.

pip install -r requirements.txt

Run the game:

python main.py


**Controls**

Move Left: A or Left Arrow\
Move Right: D or Right Arrow\
Jump / Double Jump: W, Up Arrow, or Spacebar\
Wall Slide: Hold the directional key into a wall while falling.\
Wall Jump: Press the jump key while wall sliding.\
Restart Level: R\
Return to Main Menu: Esc\
Toggle Fullscreen: F11


**File Structure**

The project is organized to separate different components of the game:

main.py

Game.py: The main game engine, handles the game loop, state management, and high-level logic.

sprites.py: Contains the classes for all game objects (Player, Platform, Collectible, Goal).

settings.py: A configuration file for all constants, physics values, colors, and asset paths.

levels.py: Defines the layout for all game levels.

ui.py: Contains classes and functions for UI elements like buttons and text rendering.

assets/: A directory containing subfolders for images (img/), sounds (snd/), and fonts (font/).

highscore.txt: A text file automatically created to store the best time.


**Customization**

Most game parameters can be easily tuned in the settings.py file. This includes:

Player physics (gravity, speed, jump height, friction).

Power-up values (coins needed, duration, multipliers).

Screen resolution and FPS.

Colors and font sizes.


This project is free to use or modify. Dont forget to give credits to me as well !!!

**Attribution:**

Credit: ksadithyan\
GitHub - https://github.com/ksadithyan


