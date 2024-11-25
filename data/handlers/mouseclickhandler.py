from data.pieces.quantumpiece import QuantumPiece
from data.manager.piecemanager import PieceManager

class MouseClickHandler:
    """Manages the 3 different Mouse Click Actions"""
    
    def __init__(self, board):
        self.board = board
        self.board.piece_manager = PieceManager(board)
        
    def handle_left_click(self, x, y):
        """Handles functionality when the user presses the Left Mouse Button"""
        
        board_x, board_y = self.board.get_square_from_mouse(x, y)
        square = self.board.get_square_on_board(board_x, board_y)
        
        if square in self.board.squares:
                        
            if len(self.board.selected_pieces) == 2 and square in self.board.common_destinations:
                print("Merging...")
                self.board.piece_manager.merge_pieces(square)
            else:
                self.board.merging_pieces = []
                self.board.common_destinations = {}
                
                if self.board.selected_piece is None:
                    # First click: Select a piece at this square
                    for piece in self.board.pieces:
                        if piece.square == square and piece.color == self.board.current_player:
                            self.board.selected_piece = piece
                            print(f"Selected {self.board.selected_piece}")
                            self.board.print_available_moves_for_selected_piece()
                            break
                else:
                    piece = self.board.get_piece_on_square(square)
                    
                    if self.board.selected_piece == piece: 
                        self.board.selected_piece = None # disable selected piece if clicked again
                        return
                    
                    friendly_fire = False
                    # Second click: Try to move the selected piece
                    for square in self.board.squares:
                        if square.x == board_x and square.y == board_y:
                            square_to = square
                    for piece in self.board.pieces:
                        if square_to == piece.square and self.board.selected_piece.color == piece.color:
                            self.board.selected_piece = piece
                            friendly_fire = True
                            print(f"Selected {self.board.selected_piece}")
                            break  
                    if not friendly_fire and self.board.piece_manager.move_piece(self.board.selected_piece, square_to):
                        if not self.board.collapsed:
                            print(f"Moved {self.board.selected_piece}")
                            self.board.collapsed = False
                        self.board.selected_piece = None  # Deselect after moving
                        self.board.generate_possible_moves("b" if self.board.current_player == "b" else "w")
                        self.board.last_captured_piece = None
                        
    def handle_right_click(self, x, y):
        """Handles functionality when the user clicks the Right Mouse Button"""
        
        board_x, board_y = self.board.get_square_from_mouse(x, y)
        square_to = self.board.get_square_on_board(board_x, board_y)
        piece_already_created = False
        first_time_exception = False
        proceed = True
        
        # Check if the selected piece is not a pawn
        if self.board.selected_piece.piece_type.lower() != "p":
            # Check if the move is not a capture 
            if square_to not in self.board.occupied_squares:
                # Check if it is a possible move
                if (self.board.selected_piece, square_to) in self.board.possible_moves:
                    # Check if the list has anything yet
                    if self.board.quantum_pieces:
                        for original_piece, quantum_piece_list in self.board.quantum_pieces:
                            if original_piece == self.board.selected_piece and not original_piece.superposed:
                                piece_already_created = True
                                break
                    else:
                        if (self.board.count_for_piece(self.board.selected_piece) < 3):
                            first_time_exception = True
                            print("Square1 Selected: ", square_to)
                            quantum_piece = QuantumPiece(self.board.selected_piece.piece_type, self.board.selected_piece.color, square_to, self.board.images)
                            self.board.quantum_pieces.append((self.board.selected_piece, [quantum_piece]))
                        else:
                            print("The same piece type cannot be superposed more than 3 times at a time")
                else:
                    proceed = False
            else:
                proceed = False
            
            if not first_time_exception:      
                if proceed:      
                    if not piece_already_created:        
                        if (self.board.count_for_piece(self.board.selected_piece) < 3):        
                            # If the piece does not exist, create a new one and add it to the list
                            quantum_piece = QuantumPiece(self.board.selected_piece.piece_type, self.board.selected_piece.color, square_to, self.board.images)
                            print("Square1 Selected: ", square_to)
                            self.board.quantum_pieces.append((self.board.selected_piece, [quantum_piece]))
                        else:
                            print("The same piece type cannot be superposed more than 3 times at a time")
                    else:
                        # If it exists, add the square to the existing quantum piece's states if it's not already there
                        for original_piece, quantum_piece_list in self.board.quantum_pieces:
                            if original_piece == self.board.selected_piece and not original_piece.superposed:
                                # Check if square_to is already in the list
                                if not any(qp.square == square_to for qp in quantum_piece_list):
                                    print("Square2 Selected: ", square_to)
                                    quantum_piece = QuantumPiece(self.board.selected_piece.piece_type, self.board.selected_piece.color, square_to, self.board.images)
                                    quantum_piece_list.append(quantum_piece)
                        self.board.handle_superposition()
                        
    def handle_middle_click(self, x, y):
        """Handles Middle Mouse Clicks"""
        
        board_x, board_y = self.board.get_square_from_mouse(x, y)
        square = self.board.get_square_on_board(board_x, board_y)
        
        if square in self.board.occupied_squares:
            
            piece = self.board.get_piece_on_square(square)
            
            if (self.board.count_for_piece(piece) > 1):
                print("A Piece can be merged if they have only 2 superposed states")
            else:
                target_op = None  # Initialize target_op

                for op, qpl in self.board.quantum_pieces:
                    if piece in qpl and piece.color == self.board.current_player:
                        # Set target_op to the op of the first piece appended
                        if target_op is None:
                            target_op = op
                            
                        # Only append piece if it has the same op as target_op
                        if op == target_op and piece not in self.board.merging_pieces:
                            print("Selected ", piece)
                            self.board.merging_pieces.append(piece)
                            self.board.selected_pieces.append(piece)
                            
                if len(self.board.merging_pieces) == 2:
                    mp1, mp2 = self.board.merging_pieces

                    # Collect destinations for mp1 and mp2
                    mp1_destinations = {
                        destination for piece, destination in self.board.possible_moves
                        if piece == mp1 and destination not in self.board.occupied_squares
                    }

                    mp2_destinations = {
                        destination for piece, destination in self.board.possible_moves
                        if piece == mp2 and destination not in self.board.occupied_squares
                    }

                    # Find common destinations
                    self.board.common_destinations = mp1_destinations & mp2_destinations  # Intersection of both sets
                    print("Available Squares to Merge:", self.board.common_destinations if len(self.board.common_destinations) > 0 else "None")