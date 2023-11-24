import pygame

from src.programs.sudoku import Sudoku

class Game:
    
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.background_color = (0, 0, 0)
        self.sudoku = Sudoku(self)
        
        self.grid_image = pygame.transform.scale(pygame.image.load("src/graphics/grid.png"), (self.screen.get_height(), self.screen.get_height()))
        self.grid_image_rect = self.grid_image.get_rect()
        self.grid_image_rect.x = self.screen.get_width() / 2 - self.grid_image_rect.width / 2
        
        self.all_rect = [[
            pygame.Rect(
                self.grid_image_rect.x + self.grid_image_rect.width / 9 * x,
                self.grid_image_rect.y + self.grid_image_rect.height / 9 * y,
                self.grid_image_rect.width / 9,
                self.grid_image_rect.height / 9
            )
        for y in range(9)] for x in range(9)]
        
    def update(self, all_events: list[pygame.event.Event]):
        """
        Exécute les actions nécessaires au bon fonctionnement du jeu
        """
        
        pygame.draw.rect(self.screen, self.background_color, self.screen.get_rect())
        
        self.display_elements()
        
        for event in all_events:
            
            if event.type == pygame.KEYDOWN:
                
                if event.key == pygame.K_ESCAPE:
                    self.sudoku.deselect_cell()
                    
                if event.key == pygame.K_LEFT:
                    if self.sudoku.selected_cell != [-1, -1]:
                        if self.sudoku.selected_cell[0] > 0:
                            self.sudoku.selected_cell[0] -= 1
                
                if event.key == pygame.K_RIGHT:
                    if self.sudoku.selected_cell != [-1, -1]:
                        if self.sudoku.selected_cell[0] < 8:
                            self.sudoku.selected_cell[0] += 1
                    
                if event.key == pygame.K_UP:
                    if self.sudoku.selected_cell != [-1, -1]:
                        if self.sudoku.selected_cell[1] > 0:
                            self.sudoku.selected_cell[1] -= 1
                
                if event.key == pygame.K_DOWN:
                    if self.sudoku.selected_cell != [-1, -1]:
                        if self.sudoku.selected_cell[1] < 8:
                            self.sudoku.selected_cell[1] += 1
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                for x in range(9):
                    for y in range(9):
                        if self.all_rect[x][y].collidepoint(pygame.mouse.get_pos()):
                            self.sudoku.select_cell(x, y)
    
    def display_elements(self):
        
        self.screen.blit(self.grid_image, self.grid_image_rect)

        if self.sudoku.selected_cell != [-1, -1]:
            pygame.draw.rect(self.screen, (80, 80, 80), self.all_rect[self.sudoku.selected_cell[0]][self.sudoku.selected_cell[1]])