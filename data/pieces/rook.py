from .piece import Piece

class Rook(Piece):
    """Rook Piece"""
    
    def __init__(self, piece_type, color, square, images):
        super().__init__(piece_type, color, square, images)