import pygame

from src.programs.sudoku import Sudoku


class Game:
    
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.background_color = (0, 0, 0)
        self.sudoku = Sudoku(self)
        self.key_mapping = {  # mapping des touches du clavier pour ajouter/modifier les valeurs des cellules
            pygame.K_1: 1,
            pygame.K_2: 2,
            pygame.K_3: 3,
            pygame.K_4: 4,
            pygame.K_5: 5,
            pygame.K_6: 6,
            pygame.K_7: 7,
            pygame.K_8: 8,
            pygame.K_9: 9
        }
        self.update_rect()
    
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
                
                if event.key in self.key_mapping:
                    if self.sudoku.selected_cell != [-1, -1]:
                        selected_cell = self.sudoku.selected_cell
                        value = self.key_mapping[
                            event.key]  # récupère la valeur a affecter à partir du dictionnaire self.key_mapping (chaque touche est associée à un entier entre 1 et 9)
                        self.sudoku.grid.set_cell(selected_cell[0], selected_cell[1],
                                                  value)  # modifie la valeur de la cellule selectionnée
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                for x in range(9):
                    for y in range(9):
                        if self.all_rect[x][y].collidepoint(pygame.mouse.get_pos()):
                            self.sudoku.select_cell(x, y)
            
            if event.type == pygame.WINDOWRESIZED:
                self.update_rect()
    
    def display_elements(self):
        """
        Permet de placer les éléments à afficher sur le brouillon de l'écran
        """
        self.screen.blit(self.grid_image, self.grid_image_rect)
        
        if self.sudoku.selected_cell != [-1, -1]:  # carré de seléction
            pygame.draw.rect(self.screen, (80, 80, 80),
                             self.all_rect[self.sudoku.selected_cell[0]][self.sudoku.selected_cell[1]])
        
        for y in range(len(self.sudoku.grid.content)):  # texte pour afficher les valeurs des cellules
            for x in range(len(self.sudoku.grid.content[y])):
                self.screen.blit(self.sudoku.grid.content[x][y].text, self.all_rect[x][y].center)
    
    def update_rect(self):
        """
        Calcul de la taille et des rectangles des cellules
        """
        self.grid_image = pygame.transform.scale(pygame.image.load("src/graphics/grid.png"),
                                                 (self.screen.get_height(), self.screen.get_height()))
        self.grid_image_rect = self.grid_image.get_rect()
        self.grid_image_rect.x = self.screen.get_width() / 2 - self.grid_image_rect.width / 2
        
        self.all_rect = [[
            pygame.Rect(
                self.grid_image_rect.x + self.grid_image_rect.width / 9 * x,
                self.grid_image_rect.y + self.grid_image_rect.height / 9 * y,
                self.grid_image_rect.width / 9,
                self.grid_image_rect.height / 9
            for y in range(9)] for x in range(9)]
