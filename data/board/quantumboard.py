from .board import Board
from data.pieces.piece import Piece
from data.handlers.quantumcollapsehandler import QuantumCollapseHandler
from data.handlers.mouseclickhandler import MouseClickHandler
from data.handlers.uihandler import UIHandler

class QuantumBoard(Board):
    """The Board Class but with Quantum Mechanics"""
    
    def __init__(self, rows, columns, images, screen):
        super().__init__(rows, columns, images, screen)
        self.quantum_pieces = []
        self.last_captured_piece = None
        self.collapsed = False
        self.removed_superposed_pieces = []
        self.merging_pieces = []
        self.common_destinations = {}
        self.selected_pieces = []
        self.quantum_collapse_handler = None
        self.mouse_click_handler = None
        self.piece_manager = None
        self.ui_handler = None
        
    def initialize_collapse_handler(self):
        self.quantum_collapse_handler = QuantumCollapseHandler(self)
        
    def initialize_mouse_click_handler(self):
        self.mouse_click_handler = MouseClickHandler(self)
        
    def initialize_ui_handler(self, screen):
        self.ui_handler = UIHandler(screen, self)
                                                                                
    def handle_superposition(self):
        """Oversees functionality when a Piece is Superposed"""
        
        # Remove entries with only one superposed square
        self.quantum_pieces = [(piece, squares) for piece, squares in self.quantum_pieces if len(squares) == 2]
        
        print("Piece Superposed!")
        for original_piece, quantum_piece_list in self.quantum_pieces:
            # Ensure the selected piece has corresponding quantum states before modifying
            if original_piece == self.selected_piece and not original_piece.superposed:
                original_piece.superposed = True
                for piece in quantum_piece_list:
                    self.pieces.append(piece)
                    self.occupied_squares.append(piece.square)
                    print(original_piece, " has moved to: ", piece.square)
                    
                # Remove original piece from occupied squares and pieces list
                if original_piece.square in self.occupied_squares:
                    self.occupied_squares.remove(original_piece.square)
                if original_piece in self.pieces:
                    self.pieces.remove(original_piece)
                    
                # Clear selection and switch turn
                self.selected_piece = None
                self.current_player = "b" if self.current_player == "w" else "w"
                self.generate_possible_moves(self.current_player)
                
    def generate_possible_moves(self, current_player):
        """Generates a list of all possible moves for the current player, accounting for quantum states and additional quantum rules."""
        
        # Call the superclass method to add standard moves.
        super().generate_possible_moves(current_player)
        
        # Iterate over pieces in quantum states to adjust moves.
        for _, piece_list in self.quantum_pieces:
            for piece in piece_list:
                # Loop through each possible move to filter based on quantum rules.
                for piece_from, square_to in list(self.possible_moves):
                    # Check if this move affects a quantum piece in superposition.
                    if piece.square == square_to and piece_from.piece_type.lower() == "p" and piece.color != self.current_player:
                        # Remove any moves where pawns would capture a quantum piece in superposition.
                        self.possible_moves.remove((piece_from, square_to))

    def handle_measurement_for_QC_QQ(self, moved_piece, target_square):
        """Oversees work of Quantum Pieces capturing both Classical and Quantum Pieces"""

        for original_piece, quantum_piece_list in self.quantum_pieces:
            if original_piece.superposed:
                if moved_piece in quantum_piece_list:
                    self.collapse_for_QC_QQ(quantum_piece_list, target_square, original_piece)
                    self.collapsed = True
                    break
                
    def handle_measurement_for_CQ(self, target_square):
        """Oversees work of Classical Pieces capturing Quantum Pieces"""
        
        for original_piece, quantum_piece_list in self.quantum_pieces:
            if original_piece.superposed:
                for p in quantum_piece_list:
                    if p.square == target_square:
                        p.removed = True
                        self.collapse_for_CQ(quantum_piece_list, original_piece, p)
                        self.collapsed = True
                        break
                            
    def collapse_for_QC_QQ(self, quantum_piece_list, target_square, original_piece):    
        """Collapse method for Quantum pieces capturing both Classical and other Quantum Pieces"""
        
        count_of_quantum_pieces = 0
        for mp, qpl in self.quantum_pieces:
            for qp in qpl:
                if qp in self.pieces:
                    count_of_quantum_pieces +=1      
                     
        #Remove related quantum pieces on the board to keep it clean
        for qp in quantum_piece_list:
            for p in self.pieces:
                if p == qp:
                    self.occupied_squares.remove(p.square)
                    self.pieces.remove(p)
                                                        
        if count_of_quantum_pieces == 1 or count_of_quantum_pieces == 2: #Standard collapse between 2 superposed piece
            for op, p in self.removed_superposed_pieces:
                for mp, qpl in self.quantum_pieces:
                    if op == mp:
                        qpl.append(p)
                        
            print("Choosing between: ", quantum_piece_list)
            final_piece = self.quantum_collapse_handler.execute_collapse(quantum_piece_list)
            print("Collapsed! Piece Chosen: ", final_piece)
            collapsed_piece = Piece(final_piece.piece_type, final_piece.color, final_piece.square, self.images)
            if final_piece.removed:
               collapsed_piece.removed = True 

            if not collapsed_piece.removed:
                if collapsed_piece.square == target_square:
                    self.pieces.append(collapsed_piece)
                    self.occupied_squares.append(collapsed_piece.square)
                else:
                    for p in self.pieces:
                        if p.square == collapsed_piece.square:
                            self.pieces.remove(p)
                    self.occupied_squares.append(target_square)
                    self.pieces.append(self.last_captured_piece)
                    self.pieces.append(collapsed_piece)
                    self.occupied_squares.append(collapsed_piece.square)

            else:
                self.occupied_squares.append(target_square)
                self.pieces.append(self.last_captured_piece)   
                
            for op, list in self.quantum_pieces:
                if op == original_piece and op.superposed:
                    self.quantum_pieces.remove((op, list))
                    
        else: #More than 2 quantum peices on board so quantum mechanics change

            for op, qpl in self.quantum_pieces:
                for p in qpl:
                    if p.removed:
                        qpl.remove(p)
                        self.removed_superposed_pieces.append((op, p))
                        
            found = False
            
            for main_piece, qp_list in self.quantum_pieces:
                for superposed_piece in quantum_piece_list:
                    if main_piece.superposed:
                        if superposed_piece == main_piece:
                            quantum_piece_list.remove(superposed_piece)
                            quantum_piece_list.extend(qp_list)
                            found = True
                            break
            
            if not found:
                associated_pieces = {}
                
                for main_piece, qp_list in self.quantum_pieces:
                    if original_piece in qp_list:
                        if original_piece not in associated_pieces:
                            associated_pieces[original_piece] = []

                        for piece in qp_list:
                            if piece != original_piece:
                                associated_pieces[original_piece].append(piece)
                                
                    if main_piece == original_piece:
                        if original_piece not in associated_pieces:
                            associated_pieces[original_piece] = []
                        associated_pieces[original_piece].extend(qp_list)
            
                quantum_piece_list = associated_pieces[original_piece]
                
                for main_piece, qp_list in self.quantum_pieces:
                    if original_piece in qp_list:
                        self.quantum_pieces.remove((main_piece, qp_list))
                        self.quantum_pieces.append((main_piece, quantum_piece_list))
                        
                for op, qpl in self.quantum_pieces:
                    for _, qpl1 in self.quantum_pieces:
                        if op in qpl1:
                            for p in qpl1:
                                if p != op:
                                    qpl.append(p)
                            
            print("Choosing between: ", quantum_piece_list)
            final_piece = self.quantum_collapse_handler.execute_collapse(quantum_piece_list)
            print("Collapsed! Piece Chosen: ", final_piece)
            staying_piece = Piece(final_piece.piece_type, final_piece.color, final_piece.square, self.images)

            if staying_piece.square == target_square:
                self.pieces.append(staying_piece)
                self.occupied_squares.append(staying_piece.square)
                for piece in quantum_piece_list:
                    if piece != staying_piece:
                        if piece.square in self.occupied_squares:
                            self.occupied_squares.remove(piece.square)
                        if piece in self.pieces:
                            self.pieces.remove(piece)
                            
                to_remove = []
                for op, qp_list in self.quantum_pieces:
                    if op == original_piece or any(piece in quantum_piece_list for piece in qp_list):
                        to_remove.append((op, qp_list))
                            
                for item in to_remove:
                    self.quantum_pieces.remove(item)
                        
            else:
                self.pieces.append(self.last_captured_piece)
                self.occupied_squares.append(self.last_captured_piece.square)
                self.occupied_squares.append(staying_piece.square)
                if not found:
                    for op, list in self.quantum_pieces:
                        if list == quantum_piece_list:
                            for p in list[:]:
                                if p.square == target_square:
                                    list.remove(p)
                                elif p not in self.pieces:
                                    self.pieces.append(p)
                                    self.occupied_squares.append(p.square)
                        
                for op, list in self.quantum_pieces:
                    if op == original_piece and op.superposed:
                        self.quantum_pieces.remove((op, list))
                        
    def collapse_for_CQ(self, quantum_piece_list, original_piece, captured_piece):
        """Reworking the relevant lists so that Classical Pieces capturing Quantum Pieces is correctly done"""
        
        if len(self.quantum_pieces) == 1:
            pass
        else:
            for _, qp_list in self.quantum_pieces:
                if original_piece in qp_list:
                    qp_list.remove(original_piece)
                    qp_list.extend(quantum_piece_list)
                    qp_list.remove(captured_piece)
                    
            for op, qpl in self.quantum_pieces:
                if op == original_piece:
                    self.quantum_pieces.remove((op, qpl))
    
    def count_for_piece(self, piece):
        """Returns the number of superposed pieces of the same type"""
        
        count = 0
        
        for op, _ in self.quantum_pieces:
            if piece.piece_type == op.piece_type:
                count += 1
                
        return count