class Cell:
    
    def __init__(self):
        self.value = int()  # entre 0 et 9 (0 = case vide)
        self.state = 'unlocked'  # valeurs possibles: unlocked, locked, superlocked
    
    def get_value(self) -> int: pass
    
    def get_state(self) -> int: pass
    
    def put_value(self, value: int): pass
    
    def set_state(self, state: str): pass
