import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide'  # Hides welcome message of pygame
import pygame
from settings.config import WIDTH, HEIGHT, COLOUR_NAMES
from pygame_manager.pygame_manager import clock
from data.board.quantumboard import QuantumBoard
from utils.utils import load_images

def main():
    """Main game loop."""
    
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    images = load_images()
    board = QuantumBoard(8, 8, images, screen)
    board.initialize_collapse_handler()
    board.initialize_mouse_click_handler()
    board.initialize_ui_handler(screen)
    board.ui_handler.draw_board()
    board.add_pieces()
    board.generate_possible_moves("w")
    
    running = True
    
    while running:
        screen.fill(COLOUR_NAMES["BLACK"])
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                handle_keydown(event, board, board.display_indexes)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                handle_mouse_click(event, board)
        
        board.ui_handler.draw_board()
        board.ui_handler.update_pieces()
        board.ui_handler.show_superposed_squares()
        board.ui_handler.draw_mergeable_squares()
        
        if board.selected_piece is not None:
            board.ui_handler.get_available_moves_for_selected_piece()
        if board.display_indexes:
            board.ui_handler.draw_indexes()
        if not board.possible_moves:
            board.ui_handler.draw_game_over(screen, board)
            
        pygame.display.flip()
        clock.tick(60)
        
    pygame.quit()

def handle_keydown(event, board, display_indexes):
    """Handles key press events."""
    
    if event.key == pygame.K_i: # Press i to view the square indexes
        board.display_indexes = not display_indexes
    elif event.key == pygame.K_p: # Press p to view the pieces on board
        for piece in board.pieces:
            print(piece)
    elif event.key == pygame.K_q: # Press q to view the quantum pieces
        print(board.quantum_pieces)
    elif event.key == pygame.K_o: # Press o to view the occupied squares on the board
        print(board.occupied_squares)
    elif event.key == pygame.K_m: # Press m to view all possible moves on the board
        print(board.possible_moves)
    elif event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5]: # Press 1/2/3/4/5 to set the relevant collapse method
        collapse_method = int(event.unicode)
        board.quantum_collapse_handler.set_collapse_method(collapse_method)

def handle_mouse_click(event, board):
    """Handles mouse click events."""
    
    x, y = pygame.mouse.get_pos()
    if event.button == 1: # Left Mouse click to move piece
        board.mouse_click_handler.handle_left_click(x, y)
    elif event.button == 2: # Right Mouse click to superpose piece
        board.mouse_click_handler.handle_middle_click(x, y)
    elif event.button == 3 and board.selected_piece is not None: # Middle Mouse click to merge superposed pieces
        board.mouse_click_handler.handle_right_click(x, y)
        
if __name__ == "__main__":
    main()