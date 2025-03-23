# utils/config.py:

ROW_COUNT = 6
COLUMN_COUNT = 7
WIN_COUNT = 4
SQUARESIZE = 100
RADIUS = SQUARESIZE // 2 - 5

WIDTH = COLUMN_COUNT * SQUARESIZE
HEIGHT = (ROW_COUNT + 1) * SQUARESIZE
width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT + 1) * SQUARESIZE  # Extra row for player input

# Colors
BLUE = (33, 150, 243)          # Board background
DARK_BLUE = (25, 118, 210)     # Empty cell fill
RED = (244, 67, 54)            # Player outer
DARK_RED = (211, 47, 47)       # Player inner
YELLOW = (255, 235, 59)        # AI outer
DARK_YELLOW = (255, 193, 7)    # AI inner
HOVER_YELLOW = (255, 245, 157) # AI predicted hover move
BLACK = (0, 0, 0)
GRAY = (169, 169, 169)
WHITE = (255, 255, 255)


# Game Settings
MAX_SCORE = 3  # Number of rounds to win match
ANIMATION_DELAY = 30  # ms per frame during drop animation


PLAYER = 1
AI = 2

