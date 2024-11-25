import pygame
from pygame_manager.pygame_manager import font
from settings.config import SQUARE_SIZE, BOARD_SIZE, GAP_X, GAP_Y
from settings.config import COLOUR_NAMES

class UIHandler:
    def __init__(self, screen, board):
        self.screen = screen
        self.board = board

    def draw_board(self):
        """Draw the board"""
        
        # Draws a border around the board
        border_thickness = 3
        pygame.draw.rect(self.screen, COLOUR_NAMES["WHITE"],
                        (GAP_X - border_thickness, GAP_Y - border_thickness,
                        BOARD_SIZE + 2 * border_thickness, BOARD_SIZE + 2 * border_thickness),
                        border_thickness)
        
        # Draws the chessboard centered on the screen
        for row in range(self.board.rows):
            for col in range(self.board.columns):
                color = self.board.colors[(row + col) % 2]
                x = GAP_X + col * SQUARE_SIZE
                y = GAP_Y + row * SQUARE_SIZE
                pygame.draw.rect(self.screen, color, [x, y, SQUARE_SIZE, SQUARE_SIZE])

        # Draw rank and file labels along the edges
        for i in range(8):
            rank_text = font.render(str(8 - i), True, COLOUR_NAMES["WHITE"])
            file_text = font.render(chr(ord('a') + i), True, COLOUR_NAMES["WHITE"])           
            # Display rank on the left
            self.screen.blit(rank_text, (GAP_X - 20, GAP_Y + i * SQUARE_SIZE + SQUARE_SIZE // 2 - rank_text.get_height() // 2))
            # Display file at the bottom
            self.screen.blit(file_text, (GAP_X + i * SQUARE_SIZE + SQUARE_SIZE // 2 - file_text.get_width() // 2, GAP_Y + BOARD_SIZE + 5))
            
    def draw_indexes(self):
        """Draw the indexes of the squares on the board"""
        
        #Draw the indexes of each box if toggled. (Press 'i')
        if self.board.display_indexes:
            for square in self.board.squares:
                idx_text = font.render(str(square.idx), True, COLOUR_NAMES["RED"])
                text_rect = idx_text.get_rect(center=(GAP_X + square.x * SQUARE_SIZE + SQUARE_SIZE // 2, GAP_Y + (7 - square.y) * SQUARE_SIZE + SQUARE_SIZE // 2))
                self.screen.blit(idx_text, text_rect)
                
    def update_pieces(self):
        """Update the positions of the pieces"""
        
        # Draw each piece on the board, adjusting for flip
        for piece in self.board.pieces:
            piece.draw(self.screen)
            
    def get_available_moves_for_selected_piece(self):
        """Gets available moves of the selected piece"""
        
        for piece, square_to in self.board.possible_moves:
            if self.board.selected_piece == piece:
                self.draw_highlight(square_to)
                
    def draw_highlight(self, square):
        """Draws a border over the selected piece and circle on a square to indicate a possible move."""
        
        center_x = GAP_X + (square.x * SQUARE_SIZE) + SQUARE_SIZE // 2
        center_y = GAP_Y + ((7 - square.y) * SQUARE_SIZE) + SQUARE_SIZE // 2
        radius = SQUARE_SIZE // 4
        # Draw a circle
        pygame.draw.circle(self.screen, COLOUR_NAMES["GREEN"], (center_x, center_y), radius)
        # Draw a border
        pygame.draw.rect(self.screen, COLOUR_NAMES["LIGHT_WHITE"], (GAP_X + self.board.selected_piece.square.x * SQUARE_SIZE, GAP_Y + (7 - self.board.selected_piece.square.y) * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 3)
        
    def show_superposed_squares(self):
        """Highlights Superposed Pieces' Squares in Red"""
        
        for _, quantum_piece_list in self.board.quantum_pieces:
            for piece in quantum_piece_list:
                if piece in self.board.pieces:
                    pygame.draw.rect(self.screen, COLOUR_NAMES["RED"], (GAP_X + piece.square.x * SQUARE_SIZE, GAP_Y + (7 - piece.square.y) * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 3)
                    
    def draw_mergeable_squares(self):
        """Draws all the squares two superposed pieces can merge to"""
        
        if len(self.board.merging_pieces) == 2:
            for square in self.board.common_destinations:
                center_x = GAP_X + (square.x * SQUARE_SIZE) + SQUARE_SIZE // 2
                center_y = GAP_Y + ((7 - square.y) * SQUARE_SIZE) + SQUARE_SIZE // 2
                radius = SQUARE_SIZE // 4
                # Draw a circle
                pygame.draw.circle(self.screen, COLOUR_NAMES["GREEN"], (center_x, center_y), radius)
                
            for piece in self.board.merging_pieces:
                # Draw a border
                pygame.draw.rect(self.screen, COLOUR_NAMES["LIGHT_WHITE"], (GAP_X + piece.square.x * SQUARE_SIZE, GAP_Y + (7 - piece.square.y) * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 3)
    