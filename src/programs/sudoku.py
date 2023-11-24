import pygame

from src.programs.grid import Grid

class Sudoku:
    
    def __init__(self, game):
        self.game = game
        self.grid = Grid()
        
    def solve_grid(self): pass