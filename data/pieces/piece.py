from settings.config import GAP_X, GAP_Y

class Piece:
    """Piece class containing the piece_type, color, square object and the relevant path to the image representing it.
    Returns a string showing the piece type and the square it is in.
    Eg: Piece (K, <Square (2, 7, 59)>)
    """
    
    def __init__(self, piece_type, color, square, images):
        self.piece_type = piece_type
        self.color = color
        self.square = square
        self.image = images[piece_type]
        self.size = 65  # Square size
        self.superposed = False
        self.removed = False
    
    def draw(self, screen):
        # Calculate the x and y position based on the square position on the board
        piece_x = GAP_X + self.size * self.square.x  + self.size // 2
        piece_y = GAP_Y + self.size * (7 - self.square.y) + self.size // 2

        # Center the piece image on the calculated square center
        image_rect = self.image.get_rect(center=(piece_x, piece_y))
        screen.blit(self.image, image_rect)
        
    def __repr__(self):
        return f"Piece ({self.piece_type}, {self.square})"
    
    def __eq__(self, other):
        if isinstance(other, Piece):
            return self.square == other.square and self.piece_type == other.piece_type and self.color == other.color
        return False
    
    def __hash__(self):
        return hash((self.piece_type, self.color, self.square))