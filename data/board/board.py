from settings.config import COLOUR_NAMES
from data.square.square import Square
from data.pieces.king import King
from data.pieces.knight import Knight
from data.pieces.bishop import Bishop
from data.pieces.rook import Rook
from data.pieces.queen import Queen
from data.pieces.pawn import Pawn
from settings.config import SQUARE_SIZE, BOARD_OFFSET_X, BOARD_OFFSET_Y 

class Board:
    """The main object in this project. Board class containing the rows, columns, images, fen position and most of the main functions.
    """
    
    def __init__(self, rows, columns, images, screen):
        self.rows = rows
        self.columns = columns
        self.squares = []
        self.occupied_squares = []
        self.colors = [COLOUR_NAMES["LIGHT_BLUE"], COLOUR_NAMES["BLACK"]]
        self.pieces = []
        self.images = images
        self.screen = screen
        self.display_indexes = False
        self.initial_fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"
        self.add_squares()
        self.selected_piece = None
        self.possible_moves = []
        self.current_player = "w"

    def add_squares(self):
        """Add the squares to the board"""
        
        #Adds all the squares with the necessary values to the Board's list of squares.
        idx = 1
        for y in range(self.columns):
            for x in range(self.rows):
                square = Square(x, y, idx)
                self.squares.append(square)
                idx += 1
            
    def add_pieces(self):
        """Add pieces to the board"""
        
        #Add all pieces to the Board's list of pieces
        row_pieces = []
        board_line = self.initial_fen.strip()
        ranks = board_line.split("/")

        for rank in ranks:
            split_strings = [char for char in rank]
            row_pieces.append(split_strings)
            
        for y, rank in enumerate(row_pieces):
            x = 0
            for char in rank:
                if char.isdigit():
                    x += int(char)
                else:
                    for square in self.squares:
                        if square.x == x and square.y == 7 - y:
                            sqr = square
                            sqr.occupied = True
                            break
                    if char == "k" or char == "K":
                        piece = King(char, "w" if char.isupper() else "b", sqr, self.images)
                    elif char == "n" or char == "N":
                        piece = Knight(char, "w" if char.isupper() else "b", sqr, self.images)
                    elif char == "b" or char == "B":
                        piece = Bishop(char, "w" if char.isupper() else "b", sqr, self.images)
                    elif char == "r" or char == "R":
                        piece = Rook(char, "w" if char.isupper() else "b", sqr, self.images)
                    elif char == "q" or char == "Q":
                        piece = Queen(char, "w" if char.isupper() else "b", sqr, self.images)
                    else:
                        piece = Pawn(char, "w" if char.isupper() else "b", sqr, self.images)
                    self.pieces.append(piece)
                    self.occupied_squares.append(sqr)
                    x += 1
                                                                                                            
    def generate_fen(self):
        """Generate the fen string of the position"""
        
        #Generates a fen string of the current position. Not used but was very helpful when debugging. 
        fen = ''
        empty_count = 0

        for y in range(7, -1, -1):  #Iterate from the highest rank to the lowest
            for x in range(8):
                piece_found = False
                for piece in self.pieces:
                    if piece.square.x == x and piece.square.y == y:
                        if empty_count > 0:
                            fen += str(empty_count)
                            empty_count = 0
                        fen += piece.piece_type
                        piece_found = True
                        break
                if not piece_found:
                    empty_count += 1

            if empty_count > 0:
                fen += str(empty_count)
                empty_count = 0

            if y != 0:
                fen += '/'

        return fen
    
    def get_square_from_mouse(self, x, y):
        """Get the square using the mouse click position"""
        
        # Translate mouse position to board coordinates
        board_x = (x - BOARD_OFFSET_X) // SQUARE_SIZE
        board_y = 7 - (y - BOARD_OFFSET_Y) // SQUARE_SIZE
        return board_x, board_y
    
    def get_square_on_board(self, x, y):
        """Get the square based the coordinates"""
        
        for square in self.squares:
            if square.x == x and square.y == y:
                return square      
            
    def get_opponent_king_square(self, my_color):
        """Returns the square of the opponent's king"""
        
        opponent_king_color = "w" if my_color == "b" else "b"
        
        for piece in self.pieces:
            if piece.piece_type.lower() == "k" and piece.color == opponent_king_color:
                return piece.square
            
    def calculate_distance(self, square1, square2):
        """Calculates Manhattan distance between two squares."""
        return abs(square1.x - square2.x) + abs(square1.y - square2.y)                      
                
    def generate_possible_moves(self, current_player):
        """Generates a list of all possible moves at a given position."""
        
        global king_in_check
        
        #Empty lists that will contain very import data 
        self.possible_moves = []
        opponent_king_squares = []
        opponent_attacking_squares = []
        all_attacking_squares = []
        pieces_saying_check = []
        captured_piece = None

        #Function to check if a square is attacked by the opponent
        def is_square_attacked(square, opponent_moves):
            return any(attack_square == square for attack_square in opponent_moves)
        
        #Add the squares adjacent to the opponent's king
        for piece in self.pieces:
            if piece.piece_type.lower() == "k" and ((current_player == 'w' and piece.color == 'b') or (current_player == 'b' and piece.color == 'w')):
                opponent_king_moves = [(1, 0), (0, 1), (-1, 0), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]
                for dx, dy in opponent_king_moves:
                    x = piece.square.x + dx
                    y = piece.square.y + dy
                    if 0 <= x < 8 and 0 <= y < 8:
                        opponent_king_squares.append(Square(x, y, y * 8 + x + 1))
                        
        def get_attacking_squares():
            #Determine all possible attacking moves of the opponent
            for piece in self.pieces:
                if (current_player == 'w' and piece.color == 'b') or (current_player == 'b' and piece.color == 'w'):
                    if piece.piece_type.lower() in ["r", "n", "b", "q", "p"]:
                        directions = {
                            'r': [(0, 1), (1, 0), (0, -1), (-1, 0)],
                            'n': [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)],
                            'b': [(1, 1), (1, -1), (-1, 1), (-1, -1)],
                            'q': [(1, 0), (0, 1), (-1, 0), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)],
                            'p': [(1, -1), (-1, -1)] if piece.color == 'b' else [(1, 1), (-1, 1)]
                        }[piece.piece_type.lower()]

                        for dx, dy in directions:
                            x, y = piece.square.x, piece.square.y
                            while True:
                                x += dx
                                y += dy
                                if 0 <= x < 8 and 0 <= y < 8:
                                    next_square = Square(x, y, y * 8 + x + 1)
                                    for p in self.pieces:
                                        if p.square == next_square:
                                            attacking_piece = piece
                                            all_attacking_squares.append((attacking_piece, next_square))

                                    opponent_attacking_squares.append(next_square)
                                    if piece.piece_type.lower() in ['n', 'p']:
                                        break  #Knights and pawns move only once in each direction
                                    if next_square in self.occupied_squares:
                                        break  #Stop if an occupied square is encountered
                                else:
                                    break
                                
        get_attacking_squares()

        # Find the current player's king
        current_king = None
        for piece in self.pieces:
            if piece.piece_type.lower() == "k" and ((current_player == 'w' and piece.color == 'w') or (current_player == 'b' and piece.color == 'b')):
                current_king = piece
                break
                    
        def if_check(square, opponent_moves):
            #Check if the king is in check and returns the bool
            for attack_square in opponent_moves:
                attacking_piece, s = attack_square
                if s == square:
                    pieces_saying_check.append(attacking_piece)
                    king_in_check = True
                    return True
            king_in_check = False
            return False
        
        king_in_check = if_check(current_king.square, all_attacking_squares)
            
        def can_capture_checking_piece(piece):
            # Check if the checking piece can be captured
            for checking_piece in pieces_saying_check:
                if checking_piece.piece_type == piece.piece_type and checking_piece.square == piece.square:
                    return True

            return False

        def can_move_resolve_check(move):
            # Temporary apply the move
            original_square = move[0].square
            target_square = move[1]
            piece = move[0]

            self.occupied_squares.remove(original_square)
            piece.square = target_square
            self.occupied_squares.append(target_square)

            # Recalculate opponent attacking squares after the move
            recalculated_opponent_attacking_squares = []
            for opponent_piece in self.pieces:
                if (current_player == 'w' and opponent_piece.color == 'b') or (current_player == 'b' and opponent_piece.color == 'w'):
                    if opponent_piece.piece_type.lower() in ["r", "n", "b", "q", "p"]:
                        directions = {
                            'r': [(0, 1), (1, 0), (0, -1), (-1, 0)],
                            'n': [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)],
                            'b': [(1, 1), (1, -1), (-1, 1), (-1, -1)],
                            'q': [(1, 0), (0, 1), (-1, 0), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)],
                            'p': [(1, -1), (-1, -1)] if opponent_piece.color == 'b' else [(1, 1), (-1, 1)]
                        }[opponent_piece.piece_type.lower()]

                        for dx, dy in directions:
                            x, y = opponent_piece.square.x, opponent_piece.square.y
                            while True:
                                x += dx
                                y += dy
                                if 0 <= x < 8 and 0 <= y < 8:
                                    next_square = Square(x, y, y * 8 + x + 1)
                                    recalculated_opponent_attacking_squares.append(next_square)
                                    if opponent_piece.piece_type.lower() in ['n', 'p']:
                                        break  # Knights and pawns move only once in each direction
                                    if next_square in self.occupied_squares:
                                        break  #Stopp if an occupied square is encountered
                                else:
                                    break

            #Check if the king is still in check
            king_safe = not is_square_attacked(current_king.square, recalculated_opponent_attacking_squares)

            # Revert the move
            self.occupied_squares.remove(target_square)
            piece.square = original_square
            self.occupied_squares.append(original_square)

            return king_safe

        # Generate possible moves for the current player
        for piece in self.pieces:
            if (current_player == 'w' and piece.color == 'w') or (current_player == 'b' and piece.color == 'b'):
                if piece.piece_type == "p":  # black pawn
                    # Move forward by 1
                    forward_square = Square(piece.square.x, piece.square.y - 1, piece.square.idx - 8)
                    if forward_square not in self.occupied_squares:
                        move = (piece, forward_square)
                        if (not king_in_check or can_move_resolve_check(move)):
                            self.possible_moves.append((piece, forward_square))
                    
                    # Move forward by 2 if it's the first move
                    if piece.square.y == 6:  # Black pawn initial row
                        double_forward_square = Square(piece.square.x, piece.square.y - 2, piece.square.idx - 16)
                        if double_forward_square not in self.occupied_squares and forward_square not in self.occupied_squares:
                            move = (piece, double_forward_square)
                            if (not king_in_check or can_move_resolve_check(move)):
                                self.possible_moves.append((piece, double_forward_square))

                    # Capture left
                    if piece.square.x > 0:
                        capture_left_square = Square(piece.square.x - 1, piece.square.y - 1, piece.square.idx - 9)
                        if capture_left_square in [p.square for p in self.pieces if p.color == "w"]:
                            move = (piece, capture_left_square)
                            for p in self.pieces:
                                if p.square == capture_left_square:
                                    captured_piece = p
                            if captured_piece != None and (not king_in_check or can_move_resolve_check(move) or can_capture_checking_piece(captured_piece)):
                                self.possible_moves.append((piece, capture_left_square))

                    # Capture right
                    if piece.square.x < 7:
                        capture_right_square = Square(piece.square.x + 1, piece.square.y - 1, piece.square.idx - 7)
                        if capture_right_square in [p.square for p in self.pieces if p.color == "w"]:
                            move = (piece, capture_right_square)
                            for p in self.pieces:
                                if p.square == capture_right_square:
                                    captured_piece = p
                            if captured_piece != None and (not king_in_check or can_move_resolve_check(move) or can_capture_checking_piece(captured_piece)):
                                self.possible_moves.append((piece, capture_right_square))
                                
                elif piece.piece_type == "P":  # white pawn
                    # Move forward by 1
                    forward_square = Square(piece.square.x, piece.square.y + 1, piece.square.idx + 8)
                    if forward_square not in self.occupied_squares:
                        move = (piece, forward_square)
                        if (not king_in_check or can_move_resolve_check(move)):
                            self.possible_moves.append((piece, forward_square))

                    # Move forward by 2 if it's the first move
                    if piece.square.y == 1:  # White pawn initial row
                        double_forward_square = Square(piece.square.x, piece.square.y + 2, piece.square.idx + 16)
                        if double_forward_square not in self.occupied_squares and forward_square not in self.occupied_squares:
                            move = (piece, double_forward_square)
                            if (not king_in_check or can_move_resolve_check(move)):
                                self.possible_moves.append((piece, double_forward_square))

                    # Capture left
                    if piece.square.x > 0:
                        capture_left_square = Square(piece.square.x - 1, piece.square.y + 1, piece.square.idx + 7)
                        if capture_left_square in [p.square for p in self.pieces if p.color == "b"]:
                            move = (piece, capture_left_square)
                            for p in self.pieces:
                                if p.square == capture_left_square:
                                    captured_piece = p
                                    if captured_piece != None and (not king_in_check or can_move_resolve_check(move) or can_capture_checking_piece(captured_piece)):
                                        self.possible_moves.append((piece, capture_left_square))

                    # Capture right
                    if piece.square.x < 7:
                        capture_right_square = Square(piece.square.x + 1, piece.square.y + 1, piece.square.idx + 9)
                        if capture_right_square in [p.square for p in self.pieces if p.color == "b"]:
                            move = (piece, capture_right_square)
                            for p in self.pieces:
                                if p.square == capture_right_square:
                                    captured_piece = p
                                    if captured_piece != None and (not king_in_check or can_move_resolve_check(move) or can_capture_checking_piece(captured_piece)):
                                        self.possible_moves.append((piece, capture_right_square))
                                            
                elif piece.piece_type.lower() in ["r", "n", "b", "q"]:  # rooks, knights, bishops, queens
                    directions = {
                        'r': [(0, 1), (1, 0), (0, -1), (-1, 0)],  # Rook directions
                        'n': [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)],  # Knight moves
                        'b': [(1, 1), (1, -1), (-1, 1), (-1, -1)],  # Bishop directions
                        'q': [(1, 0), (0, 1), (-1, 0), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]  # Queen directions
                    }[piece.piece_type.lower()]

                    for dx, dy in directions:
                        x, y = piece.square.x, piece.square.y
                        while True:
                            x += dx
                            y += dy
                            if 0 <= x < 8 and 0 <= y < 8:
                                next_square = Square(x, y, y * 8 + x + 1)
                                move = (piece, next_square)
                                if next_square not in self.occupied_squares:
                                    if (not king_in_check or can_move_resolve_check(move)):
                                        self.possible_moves.append((piece, next_square))
                                    if piece.piece_type.lower() == 'n':  # Knights move only once in each direction
                                        break
                                else:
                                    # Capture an opponent's piece
                                    if next_square in [p.square for p in self.pieces if p.color != piece.color]:
                                        for p in self.pieces:
                                            if p.square == next_square:
                                                captured_piece = p
                                        if captured_piece != None and (not king_in_check or can_move_resolve_check(move) or can_capture_checking_piece(captured_piece)):
                                            self.possible_moves.append((piece, next_square))
                                    break
                            else:
                                break

                elif piece.piece_type.lower() == "k":  # both color kings
                    king_moves = [(1, 0), (0, 1), (-1, 0), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]  # All adjacent squares
                    for dx, dy in king_moves:
                        x = piece.square.x + dx
                        y = piece.square.y + dy
                        if 0 <= x < 8 and 0 <= y < 8:
                            next_square = Square(x, y, y * 8 + x + 1)
                            move = (piece, next_square)
                            if next_square not in self.occupied_squares and next_square not in opponent_king_squares and not is_square_attacked(next_square, opponent_attacking_squares):
                                if (not king_in_check or can_move_resolve_check(move)):
                                    self.possible_moves.append((piece, next_square))
                            else:
                                # Capture an opponent's piece
                                if next_square in [p.square for p in self.pieces if p.color != piece.color] and next_square not in opponent_king_squares and not is_square_attacked(next_square, opponent_attacking_squares):
                                    for p in self.pieces:
                                        if p.square == next_square:
                                            captured_piece = p
                                    if (not king_in_check or can_move_resolve_check(move) or can_capture_checking_piece(captured_piece)):
                                        self.possible_moves.append((piece, next_square))
        
    def print_available_moves_for_selected_piece(self):
        """Prints available moves of the selected piece"""
        
        for piece, square_to in self.possible_moves:
            if self.selected_piece == piece:
                print("Avialable move: ", square_to)
                                
    def get_piece_on_square(self, square):
        """Returns the piece on a square"""
        
        for piece in self.pieces:
            if piece.square == square:
                return piece