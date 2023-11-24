import pygame

from src.programs.sudoku import Sudoku

class Game:
    
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        
        self.sudoku = Sudoku()
        
    def update(self, all_events: pygame.event.Event): pass
    
    def display_elements(self): pass