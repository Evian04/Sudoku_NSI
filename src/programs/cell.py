from src.programs.text import Text
from src.programs.test_errors import test_errors

class Cell:
    """
    La classe Cell contient les données relatives aux cases (valeur, état, etc...)
    """
    
    def __init__(self, value: int, state: str):
        
        test_errors(value = value, state = state)
        
        self.text = Text("", "Arial", 30, (0, 0, 0))  # crée l'objet texte
        self.state = None
        self.set_value(value)  # entre 0 et 9 (0 = case vide)
        self.set_state(state)  # valeurs possibles: "unlocked", "locked", "superlocked"
    
    def get_value(self) -> int:
        """
        Renvoi la valeur de la case
        """
        
        return self.value
    
    def get_state(self) -> str:
        """
        Renvoi l'état de la case
        """
        
        return self.state

    def get_text(self) -> Text:
        """
        Renvoi le text de la case
        """
        
        return self.text
    
    def set_value(self, value: int):
        """
        Met la valeur de la case à `value`
        """
        
        test_errors(value = value)
        
        self.value = value
        
        if self.value != 0:
            self.text.set_text(str(self.value))
            
        else:
            self.text.set_text("")

    def set_state(self, state: str):
        """
        Met l'état de la case sur `state`
        """
        
        test_errors(state = state)
        
        self.state = state
        
    def set_color(self, color: tuple[int, int, int]):
        """
        Met la couleur de la case à `color`
        """
        
        test_errors(color = color)
        
        self.text.set_color(color)