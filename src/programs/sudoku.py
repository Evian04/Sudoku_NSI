import pygame

from src.programs.grid import Grid

class Sudoku:
    
    def __init__(self, game):
        self.game = game
        self.grid = Grid()
        self.selected_cell = [-1, -1] # Coordonnées de la case sélectionnée, [-1, -1] si aucune case
    
    def select_cell(self, x: int, y: int):
        """
        Selectionne la case de coordonnées (x, y)
        """
        
        if type(x) != int:
            raise TypeError(f"The `x` argument must be an integer (type : {type(x)})")
        
        if type(y) != int:
            raise TypeError(f"The `y` argument must be an integer (type : {type(y)})")
        
        if x < 0 or x > 8:
            raise ValueError(f"The `x` argument must be between 0 and 8")
        
        if y < 0 or y > 8:
            raise ValueError(f"The `y` argument must be between 0 and 8")
        
        self.selected_cell = [x, y]
        
    def deselect_cell(self):
        """
        Déselectionne la case sélectionnée
        """
        
        self.selected_cell = [-1, -1]
    
    def load_grid(self, new_grid): pass
        
    def lock_cell(self, x: int, y: int): pass
    
    def unlock_cell(self, x: int, y: int): pass
        
    def verify_grid(self): pass
        
    def solve_grid(self): pass