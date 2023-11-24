import pygame

from src.programs.sudoku import Sudoku

class Game:
    
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.sudoku = Sudoku(self)
        
        self.grid_image = pygame.transform.scale(pygame.image.load("src/graphics/grid.png"), (self.screen.get_height() - 10, self.screen.get_height() - 10))
        
        self.sudoku = Sudoku(self)
        
    def update(self, all_events):
        """
        
        :param all_events:
        :return:
        """
        self.display_elements()
    
    def display_elements(self):
        
        self.screen.blit(self.grid_image, self.grid_image.get_rect())
