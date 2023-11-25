import pygame

from src.programs.sudoku import Sudoku


class Game:
    
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.background_color = (0, 0, 0)
        self.sudoku = Sudoku(self)
        self.key_mapping = {  # mapping des touches du clavier pour ajouter/modifier les valeurs des cellules
            pygame.K_1:         1,
            pygame.K_2:         2,
            pygame.K_3:         3,
            pygame.K_4:         4,
            pygame.K_5:         5,
            pygame.K_6:         6,
            pygame.K_7:         7,
            pygame.K_8:         8,
            pygame.K_9:         9,
            pygame.K_KP_1:      1,
            pygame.K_KP_2:      2,
            pygame.K_KP_3:      3,
            pygame.K_KP_4:      4,
            pygame.K_KP_5:      5,
            pygame.K_KP_6:      6,
            pygame.K_KP_7:      7,
            pygame.K_KP_8:      8,
            pygame.K_KP_9:      9,
            pygame.K_BACKSPACE: 0,  # 0 correspond à une case vide (supprime la valeur  de la case)
            pygame.K_DELETE:    0,
            pygame.K_0:         0,
            pygame.K_KP_0:      0
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
                
                if event.key == pygame.K_l:
                    if self.sudoku.grid.get_cell_state(self.sudoku.selected_cell[0], self.sudoku.selected_cell[1]) != "superlocked":
                        self.sudoku.lock_selected_cell()
                        print(f'game.update(): cell {tuple(self.sudoku.selected_cell)} was locked')
                
                if event.key == pygame.K_u:
                    if self.sudoku.grid.get_cell_state(self.sudoku.selected_cell[0], self.sudoku.selected_cell[1]) != "superlocked":
                        self.sudoku.unlock_selected_cell()
                        print(f'game.update(): cell {tuple(self.sudoku.selected_cell)} was unlocked')

                
                if event.key in self.key_mapping:
                    selected_cell = self.sudoku.selected_cell
                    if selected_cell != [-1, -1]:
                        if self.sudoku.grid.get_cell_state(selected_cell[0], selected_cell[1]) == "unlocked":
                        
                            # récupère la valeur a affecter à partir du dictionnaire self.key_mapping (chaque touche est associée à un entier entre 1 et 9)
                            value = self.key_mapping[event.key]
                            
                            # modifie la valeur de la cellule selectionnée
                            self.sudoku.grid.set_cell(
                                selected_cell[0],
                                selected_cell[1],
                                value
                            )
                        elif self.sudoku.grid.get_cell_state(selected_cell[0], selected_cell[1]) == "locked":
                            print(f"grid.update(): cell {tuple(selected_cell)} is locked (press 'U' to Unlock)")
                        else: print(f"grid.update(): cell {tuple(selected_cell)} is superlocked")

            
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

        for x in range(self.sudoku.lign_number):
            for y in range(self.sudoku.column_number):
                if self.sudoku.grid.content[x][y].state == "superlocked":
                    # affichage case superlocked (case grisée)
                    rect = self.all_rect[x][y].copy()
                    rect.width -= 6
                    rect.height -= 6
                    rect.x += 3
                    rect.y += 3
                    pygame.draw.rect(
                        self.screen,
                        (200, 200, 200),
                        rect
                    )
        # affichage de la sélection (carré)
        if self.sudoku.selected_cell != [-1, -1]:  # carré de sélection
            pygame.draw.rect(
                self.screen,
                (120, 120, 120),
                self.all_rect[self.sudoku.selected_cell[0]][self.sudoku.selected_cell[1]]
            )

        for x in range(self.sudoku.lign_number):  # affichage des cases verrouillées
            for y in range(self.sudoku.column_number):
                # affichage case locked (affichage du cadenas)
                if self.sudoku.grid.content[x][y].state == "locked":
                    self.screen.blit(self.padlock_image, self.all_rect[x][y])
                
                # affichage du texte (numéro) pour chaque case
                self.screen.blit(
                    self.sudoku.grid.content[x][y].text.get_text(),
                    self.all_rect[x][y].center
                )
    
    def update_rect(self):
        """
        Calcul de la taille et des rectangles des cellules
        """
        
        self.grid_image = pygame.image.load("src/graphics/grid.png")
        
        if self.screen.get_width() >= self.screen.get_height():
            self.grid_image = pygame.transform.scale(
                self.grid_image,
                (self.screen.get_height(), self.screen.get_height())
            )
        
        else:
            self.grid_image = pygame.transform.scale(
                self.grid_image,
                (self.screen.get_width(), self.screen.get_width())
            )
        
        self.grid_image_rect = self.grid_image.get_rect()
        self.grid_image_rect.x = self.screen.get_width() / 2 - self.grid_image_rect.width / 2
        
        self.padlock_image = pygame.image.load("src/graphics/padlock.png")
        self.padlock_image = pygame.transform.scale(
            self.padlock_image,
            (self.grid_image_rect.width / 9 / 4, self.grid_image_rect.height / 9 / 4)
        )
        
        self.all_rect = [[
            pygame.Rect(
                self.grid_image_rect.x + self.grid_image_rect.width / 9 * x,
                self.grid_image_rect.y + self.grid_image_rect.height / 9 * y,
                self.grid_image_rect.width / 9,
                self.grid_image_rect.height / 9
            )
            for y in range(9)] for x in range(9)]

        for y in range(9):  # recalcule et réattribue les valeurs de la teille des textes
            for x in range(9):
                self.sudoku.grid.content[x][y].text.set_font_size(round(0.375 * self.all_rect[x][y].height))  # 0.375 est le rapport entre la taille d'un carré et la taille de la police
