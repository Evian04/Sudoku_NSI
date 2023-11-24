class Cell:
    
    def __init__(self, value: int, state: str):
        if type(value) != int:
            raise TypeError(f"The `value` argument must be an integer (type : {type(value)})")
        
        if type(state) != str:
            raise TypeError(f"The `state` argument must be a string (type : {type(state)})")
        
        if value < 0 or value > 9:
            raise ValueError(f"The `value` argument must be between 0 and 9 (value : {value})")
        
        if not state in ["unlocked", "locked", "superlocked"]:
            raise ValueError(f"The `state` argument must be \"unlocked\", \"locked\" or \"superlock\" (value : {state})")
        
        self.value = value # entre 0 et 9 (0 = case vide)
        self.state = state # valeurs possibles: unlocked, locked, superlocked
    
    def get_value(self) -> int:
        
        """
        Renvois la valeur de la case
        """
        
        return self.value
    
    def get_state(self) -> int:
        
        """
        Renvois l'état de la case
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
    
    def set_state(self, state: str):
        
        """
        Met l'état de la case sur`state`
        """
        
        if type(state) != str:
            raise TypeError(f"The `state` argument must be a string (type : {type(state)})")
        
        if not state in ["unlocked", "locked", "superlocked"]:
            raise ValueError(f"The `state` argument must be \"unlocked\", \"locked\" or \"superlock\" (value : {state})")
        
        self.state = state