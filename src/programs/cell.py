from src.programs.test_errors import test_errors

class Cell:
    """
    La classe Cell contient les données relatives aux cases (valeur, état, etc...)
    """
    
    def __init__(self, value: str, state: str, sudoku_size: int):
        
        # Test préconditions
        test_errors(sudoku_size, value=value, state=state)
        
        self.value = value
        self.state = state
        self.sudoku_size = sudoku_size
        
        self.is_in_conflict = False
    
    def set_value(self, value: str):
        """
        Met la valeur de la case à "value"
        """
        
        # Test préconditions
        test_errors(self.sudoku_size, value=value)
        
        self.value = value

    def set_state(self, state: str):
        """
        Met l'état de la case à "state"
        """
        
        # Test préconditions
        test_errors(state=state)
        
        self.state = state
        
    def set_conflicting_state(self, conflicting_state: bool):
        """
        Met la variable "is_in_conflict" à "conflicting_state"
        """
        
        # Test préconditions
        test_errors(boolean=conflicting_state)
        
        self.is_in_conflict = conflicting_state