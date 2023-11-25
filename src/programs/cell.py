from  src.programs.text import Text
class Cell:
    """
    La classe Cell contient les données relatives aux cases (valeur, état, etc...)
    """
    
    def __init__(self, value: int, state: str):
        
        if type(value) != int:
            raise TypeError(f"The `value` argument must be an integer (type : {type(value)})")
        
        if value < 0 or value > 9:
            raise ValueError(f"The `value` argument must be between 0 and 9 (value : {value})")
        
        self.text = Text('', 'Arial', 30, (0, 0, 0))  # crée l'objet texte
        self.state = None
        self.put_value(value)  # entre 0 et 9 (0 = case vide)
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
        Renvois le text de la case
        """
        
        return self.text
    
    def put_value(self, value: int):
        """
        Met la valeur de la case à `value`
        """
        
        if type(value) != int:
            raise TypeError(f"The `value` argument must be an integer (type : {type(value)})")
        
        if value < 0 or value > 9:
            raise ValueError(f"The `value` argument must be between 0 and 9 (value : {value})")
        
        self.value = value
        
        if self.value != 0:
            self.text.set_text(str(self.value))
            
        else:
            self.text.set_text("")

    
    def set_state(self, state: str):
        """
        Met l'état de la case sur `state`
        """
        
        if type(state) != str:
            raise TypeError(f"The `state` argument must be a string (type : {type(state)})")
        
        if not state in ["unlocked", "locked", "superlocked"]:
            raise ValueError(f"""The `state` argument must be "unlocked", "locked" or "superlock" (value : {state})""")
        
        self.state = state
        
    def set_color(self, color: tuple[int, int, int]):
        """
        Met la couleur de la case à `color`
        """
        
        if type(color) != tuple:
            raise TypeError(f"The `color` argument must be a tuple (type : {type(color)})")
        
        if len(color) != 3:
            raise ValueError(f"The `color` argument must have a length of 3 (length : {color})")
        
        self.text.set_color(color)