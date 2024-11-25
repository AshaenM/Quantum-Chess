import os

# Screen Constants
WIDTH = 700
HEIGHT = 700
SQUARE_SIZE = 65
BOARD_SIZE = SQUARE_SIZE * 8  # 8x8 board

# Calculate GAP to center the board
GAP_X = (WIDTH - BOARD_SIZE) // 2
GAP_Y = (HEIGHT - BOARD_SIZE) // 2

BOARD_OFFSET_X = (WIDTH - SQUARE_SIZE * 8) // 2
BOARD_OFFSET_Y = (HEIGHT - SQUARE_SIZE * 8) // 2

COLOUR_NAMES = {
	'BLACK':  (000, 000, 000, 255),
	'WHITE':  (255, 255, 255, 255),
	'RED':    (255, 000, 000, 255),
	'GREEN':  (000, 255, 000, 255),
	'BLUE':   (000, 000 ,255, 255),
	'GREY':   (100, 100, 100, 255),
	'PINK':   (255, 175, 175, 255),
	'YELLOW': (255, 255, 000, 255),
	'ORANGE': (255, 175, 000, 255),
	'PURPLE': (200, 000, 175, 200),
	'BROWN':  (125, 125, 100, 255),
	'AQUA':   (100, 230, 255, 255),
	'DARK_GREEN': (000, 100, 000, 255),
	'LIGHT_GREEN':(116, 150, 85, 255),
	'LIGHT_BLUE': (35, 35, 255, 255),
	'LIGHT_GREY': (200, 200, 200, 255),
	'LIGHT_PINK': (255, 230, 230, 255),
	'LIGHT_WHITE': (231, 231, 203, 255)
}

# Image Paths
ASSET_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'assets', 'images')
PIECE_IMAGES = {
    'P': 'white pawn.png',
    'R': 'white rook.png',
    'N': 'white knight.png',
    'B': 'white bishop.png',
    'Q': 'white queen.png',
    'K': 'white king.png',
    'p': 'black pawn.png',
    'r': 'black rook.png',
    'n': 'black knight.png',
    'b': 'black bishop.png',
    'q': 'black queen.png',
    'k': 'black king.png',
    'na': 'black king.png',  # Dummy piece
}