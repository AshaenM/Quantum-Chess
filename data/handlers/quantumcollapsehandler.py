from data.handlers.collapsestrategyhandler import (
    RandomCollapse,
    ProximityCollapse,
    EntropyBasedCollapse,
    DeterministicCollapse,
    ProbabilityWeightedCollapse,
)
    
class QuantumCollapseHandler:
    def __init__(self, board):
        self.board = board
        self.collapse_methods = {
            1: RandomCollapse(),
            2: ProximityCollapse(),
            3: EntropyBasedCollapse(),
            4: DeterministicCollapse(),
            5: ProbabilityWeightedCollapse()
        }
        self.selected_collapse_strategy = self.collapse_methods[1] # Default to RandomCollapse

    def set_collapse_method(self, method_id):
        """Set the collapse strategy dynamically."""
        if method_id in self.collapse_methods:
            self.selected_collapse_strategy = self.collapse_methods[method_id]
            print(f"Collapse method set to: {type(self.selected_collapse_strategy).__name__}")
        else:
            print("Invalid collapse method selected.")

    def execute_collapse(self, quantum_piece_list):
        """Execute the selected collapse strategy."""
        return self.selected_collapse_strategy.collapse(quantum_piece_list, self.board)