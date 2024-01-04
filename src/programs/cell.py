from src.programs.test_errors import test_errors

class Cell:
    """
    La classe Cell contient les données relatives aux cases (valeur, état, etc...)
    """
    
    def __init__(self, value: int, state: str, sudoku_size: int):
        
        test_errors(sudoku_size, value = value, state = state)
        
        self.value = value
        self.state = state
        self.sudoku_size = sudoku_size
        
        self.is_in_conflict = False
    
    def set_value(self, value: int):
        """
        Met la valeur de la case à "value"
        """
        
        test_errors(self.sudoku_size, value = value)
        
        self.value = value

    def set_state(self, state: str):
        """
        Met l'état de la case à "state"
        """
        
        test_errors(state = state)
        
        self.state = state
        
    def set_conflicting_state(self, conflicting_state: bool):
        """
        Met la variable "is_in_conflict" à "conflicting_state"
        """
        
        assert type(conflicting_state) == bool, 'The "conflicting_state" argument must be a boolean'
        
        self.is_in_conflict = conflicting_state