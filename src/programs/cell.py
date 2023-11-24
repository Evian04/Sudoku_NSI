class Cell:
    
    def __init__(self):
        self.x = int()
        self.y = int()
        self.state = 'unlock' # possible values: unlock, lock, super_lock
        
        
    def get_value(self) -> int: pass
    
    def get_state(self) -> int: pass
    
    def put_value(self, value: int): pass
    
    def set_state(self, state: str): pass