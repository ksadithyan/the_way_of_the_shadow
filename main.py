# main.py
import Game
import sys
from settings import *


# --- Main Execution ---
if __name__ == '__main__':
    game = Game.Game()
    game.run()
    pygame.quit()
    sys.exit()
