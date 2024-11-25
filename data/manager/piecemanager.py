from data.pieces.piece import Piece
from data.pieces.quantumpiece import QuantumPiece

class PieceManager:
    """Manages all movements of pieces"""
    
    def __init__(self, board):
        self.board = board

    def move_piece(self, moving_piece, target_square):
        """Regular moves including captures"""
        for piece, destination in self.board.possible_moves:
            if moving_piece == piece and target_square == destination:
                self.board.occupied_squares.append(target_square)
                if target_square in self.board.occupied_squares:
                    # Handle capturing if target square is occupied
                    captured_piece = next((p for p in self.board.pieces if p.square == target_square), None)
                    self.board.last_captured_piece = captured_piece
                    if captured_piece:
                        self.handle_capture(moving_piece, target_square, captured_piece)
                else:
                    # No capture, regular move
                    print(f"Moving {moving_piece.piece_type} from {moving_piece.square} to {target_square}")
                    
                # Complete the move
                self.finalize_move(moving_piece, target_square)
                return True

    def handle_capture(self, moving_piece, target_square, captured_piece):
        """Handles a capture"""
        
        # Capture logic for quantum and classical pieces
        for _, quantum_piece_list in self.board.quantum_pieces:
            if any(qp.square == target_square for qp in quantum_piece_list):
                self.capture_quantum_piece(moving_piece, captured_piece)
                return
        print(f"Capturing {captured_piece}")
        self.board.pieces.remove(captured_piece)

    def finalize_move(self, moving_piece, target_square):
        """Finalizes a move and checks if superposed pieces need to collapse"""
        
        # Finalize move: update occupied squares and switch turns
        moving_piece.square = target_square
        self.board.occupied_squares = []
        for piece in self.board.pieces:
                self.board.occupied_squares.append(piece.square)
        if isinstance(moving_piece, QuantumPiece) and isinstance(self.board.last_captured_piece, Piece) and not isinstance(self.board.last_captured_piece, QuantumPiece):
            #Quantum Piece Capturing Classical Piece
            print("Collapsing...")
            self.board.handle_measurement_for_QC_QQ(moving_piece, target_square)
        if isinstance(moving_piece, Piece) and not isinstance(moving_piece, QuantumPiece) and isinstance(self.board.last_captured_piece, QuantumPiece):
            #Classical Piece Capturing Quantum Piece
            self.board.handle_measurement_for_CQ(target_square)
        if isinstance(moving_piece, QuantumPiece) and isinstance(self.board.last_captured_piece, QuantumPiece):
            #Quantum Piece Capturing Quantum Piece
            self.board.handle_measurement_for_QC_QQ(moving_piece, target_square)
        self.board.current_player = "b" if self.board.current_player == "w" else "w"
        
    def capture_quantum_piece(self, moving_piece, captured_piece):
        """Capturing a Quantum Piece"""
        
        if moving_piece.piece_type.lower() != "p":  # Only capture if not a pawn
            print(f"Capturing quantum piece {captured_piece}")
            self.board.pieces.remove(captured_piece)
        
    def merge_pieces(self, square):
        """Merges two superposed pieces"""
        
        #Remove Quantum Pieces
        for op, qpl in self.board.quantum_pieces:
            if any(piece in qpl for piece in self.board.selected_pieces):
                self.board.quantum_pieces.remove((op, qpl))
                
        #Remove Pieces that are going to merge
        for piece in self.board.selected_pieces:
            self.board.occupied_squares.remove(piece.square)
            self.board.pieces.remove(piece)
                
        #Create Piece on merging square
        new_p = Piece(self.board.selected_pieces[0].piece_type, self.board.selected_pieces[0].color, square, self.board.images)

        #Add New Piece to Board
        self.board.pieces.append(new_p)
        self.board.occupied_squares.append(new_p.square)
        print("Pieces merged to", new_p.square)
        
        #Clear Variables
        self.board.selected_pieces = []
        self.board.merging_pieces = []
        self.board.common_destinations = {}
        
        #Change Player
        self.board.current_player = "b" if self.board.current_player == "w" else "w"
        self.board.generate_possible_moves("b" if self.board.current_player == "b" else "w")