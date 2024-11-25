from abc import ABC, abstractmethod
import random
import time
from data.pieces.piece import Piece

class CollapseStrategy(ABC):
    """Base class for collapse strategies"""
    @abstractmethod
    def collapse(self, quantum_piece_list, board):
        pass
    
class RandomCollapse(CollapseStrategy):
    """Simple random collapse method where a random piece is selected"""
    
    def collapse(self, quantum_piece_list, board):
        start_time = time.perf_counter()
        selected_piece = random.choice(quantum_piece_list)
        end_time = time.perf_counter()
        elapsed_time = end_time - start_time
        elapsed_time_microseconds = elapsed_time * 1_000_000
        print(f"Time taken: {elapsed_time_microseconds:.2f} microseconds")
        
        return selected_piece

class ProximityCollapse(CollapseStrategy):
    """Promixisty Collapse Method where the piece closest to the opponent's king is selected"""
    
    def collapse(self, quantum_piece_list, board): 
        start_time = time.perf_counter()
        target_square = board.get_opponent_king_square(board.selected_piece.color)
        
        # Dictionary to store distance of each position from target_square
        proximity_map = {}

        for piece in quantum_piece_list:
            distance = board.calculate_distance(piece.square, target_square)
            proximity_map[piece] = distance

        # Sort by proximity (lower distances are closer)
        closest_piece = min(proximity_map, key=proximity_map.get)
        end_time = time.perf_counter()
        elapsed_time = end_time - start_time
        elapsed_time_microseconds = elapsed_time * 1_000_000
        print(f"Time taken: {elapsed_time_microseconds:.2f} microseconds")
        
        return closest_piece

class EntropyBasedCollapse(CollapseStrategy):
    """Collapse based on entropy."""
    
    def collapse(self, quantum_piece_list, board):
        start_time = time.perf_counter()
        
        # Calculate average distance to other potential positions (for concentration)
        entropy_scores = {}
        for piece in quantum_piece_list:
            distances = [
                board.calculate_distance(piece.square, other_piece.square)
                for other_piece in quantum_piece_list if other_piece != piece
            ]
            average_distance = sum(distances) / len(distances) if distances else 0
            # Entropy is inversely related to clustering (smaller distances -> lower entropy)
            entropy_scores[piece] = 1 / (average_distance + 0.001)  # Avoid division by zero
            
        # Normalize entropy scores to probabilities
        total_entropy = sum(entropy_scores.values())
        probabilities = {piece: score / total_entropy for piece, score in entropy_scores.items()}

        # Choose piece based on entropy-weighted probabilities
        pieces, weights = zip(*probabilities.items())
        collapsed_piece = random.choices(pieces, weights=weights, k=1)[0]
        end_time = time.perf_counter()
        elapsed_time = end_time - start_time
        elapsed_time_microseconds = elapsed_time * 1_000_000
        print(f"Time taken: {elapsed_time_microseconds:.2f} microseconds")
        
        return collapsed_piece

class DeterministicCollapse(CollapseStrategy):
    """Deterministic Collapse Method where the piece closest to the center is selected"""
    
    def collapse(self, quantum_piece_list, board):
        start_time = time.perf_counter()
        CENTER_SQUARE = (3.5, 3.5)
        
        def distance_to_center(piece):
            return abs(piece.square.x - CENTER_SQUARE[0]) + abs(piece.square.y - CENTER_SQUARE[1])

        quantum_piece_list.sort(key=distance_to_center)
        end_time = time.perf_counter()
        elapsed_time = end_time - start_time
        elapsed_time_microseconds = elapsed_time * 1_000_000
        print(f"Time taken: {elapsed_time_microseconds:.2f} microseconds")
        
        return quantum_piece_list[0]

class ProbabilityWeightedCollapse(CollapseStrategy):
    """Probability Weighted Collapse Method where moves capturing better pieces have a higher chance of being selected"""
    
    def collapse(self, quantum_piece_list, board):
        start_time = time.perf_counter()
        #Probability Distributed for pieces being captured
        PIECE_TYPE_PROBABILITIES = {
            "p": 0.1,
            "k": 0.0,
            "b": 0.2,
            "n": 0.2,
            "r": 0.15,
            "q": 0.25,
            "na": 0.1
        }
        
        #Create a second list 
        new_list = []
        
        #Dictionary to hold links between dummy pieces and original piece
        piece_links = {}
        
        #Add last captured pieces if not na to the list and dictionary
        for qp in quantum_piece_list:
            if qp.square == board.last_captured_piece.square:
                piece_links[board.last_captured_piece] = qp
                new_list.append(board.last_captured_piece)
            else:
                new_p = Piece("na", qp.color, qp.square, board.images)
                piece_links[new_p] = qp
                new_list.append(new_p)
        
        # Extract probabilities for each piece in the new list
        weights = [PIECE_TYPE_PROBABILITIES[piece.piece_type.lower()] for piece in new_list]
        
        # Use random.choices to perform weighted selection
        selected_piece = random.choices(new_list, weights=weights, k=1)[0]
        
        # Select the original piece
        selected_piece = piece_links[selected_piece]
        
        end_time = time.perf_counter()
        elapsed_time = end_time - start_time
        elapsed_time_microseconds = elapsed_time * 1_000_000
        print(f"Time taken: {elapsed_time_microseconds:.2f} microseconds")

        return selected_piece