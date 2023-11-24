import pygame

from src.programs.sudoku import Sudoku

class Game:
    
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.sudoku = Sudoku(self)
        
        self.grid_image = pygame.image.load("src/graphics/grid.png")
        
    def update(self, all_events: pygame.event.Event):
        
        self.display_elements()
    
    def display_elements(self):
        
        self.screen.blit(self.grid_image, self.grid_image.get_rect())