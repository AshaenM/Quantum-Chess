from .piece import Piece

class QuantumPiece(Piece):
    """A Piece that has quantum mechanics"""
    
    def __init__(self, piece_type, color, square, images):
        super().__init__(piece_type, color, square, images)