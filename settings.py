
# game options
TITLE = "untitled_space_game"
WIDTH = 700
HEIGHT = 480
FPS = 60
FONT_NAME = 'arial'
HS_FILE = "highscore.txt"

# Player properties
PLAYER_ACC = 0.8
PLAYER_FRICTION = -0.12
PLAYER_GRAV = 0.6
PLAYER_JUMP = 20

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GOLD = (188, 162, 65)
LIGHTBLUE = (0, 155, 155)
BGCOLOR = BLACK

# Starting platforms
PLATFORM_LIST = [(0, HEIGHT-40, WIDTH, 40), 
                (WIDTH/2 - 50, HEIGHT * 3/4, 100, 20), 
                (125, HEIGHT - 350, 100, 20),
                (360, 200, 100, 20), 
                (175, 100, 50, 20)]
