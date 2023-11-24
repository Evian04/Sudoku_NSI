import pygame.font


class Cell:
    """
    classe Cell(ule), contient les données relatives aux cellules (valeur, etat, etc...)
    """
    def __init__(self, value: int, state: str):
        if type(value) != int:
            raise TypeError(f"The `value` argument must be an integer (type : {type(value)})")
        
        if value < 0 or value > 9:
            raise ValueError(f"The `value` argument must be between 0 and 9 (value : {value})")
        
        self.font_size = 30
        self.put_value(value)  # entre 0 et 9 (0 = case vide)
        self.set_state(state)  # valeurs possibles: "unlocked", "locked", "superlocked"
    
    def get_value(self) -> int:
        """
        Renvoi la valeur de la case
        """
        
        return self.value
    
    def get_state(self) -> int:
        """
        Renvoi l'état de la case
        """
        
        return self.state
    
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
            self.set_text(str(self.value), (0, 0, 0))
            
        else:
            self.set_text("", (0, 0, 0))

    
    def set_state(self, state: str):
        """
        Met l'état de la case sur `state`
        """
        
        if type(state) != str:
            raise TypeError(f"The `state` argument must be a string (type : {type(state)})")
        
        if not state in ["unlocked", "locked", "superlocked"]:
            raise ValueError(f"""The `state` argument must be "unlocked", "locked" or "superlock" (value : {state})""")
        
        self.state = state
    
    def set_text(self, text: str, color: tuple[int, int, int]) -> None:
        """
        Permet de créer un texte pour afficher la valeur de la cellule
        :param text: texte à afficher
        :param color: couleur du texte (RGB)
        """
        font = pygame.font.SysFont('Calibri', self.font_size)  # création d'une police pour afficher les chiffres
        self.text = font.render(text, True, color)  # création du texte (self.text est une Surface)
        
