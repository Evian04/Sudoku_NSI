import pygame

from src.programs.sudoku import Sudoku
from src.programs.test_errors import test_errors


class Game:
    
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.background_color = (0, 0, 0)
        self.sudoku = Sudoku(self)
        self.is_solving = False
        self.do_quit = False
        self.key_mapping = {  # mapping des touches du clavier pour ajouter/modifier la valeur d'une cellule
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
    
    def cell_update(self, coordinates:tuple[int, int], all_events: list[pygame.event.Event] = None):
        """
        mise à jour rapide d'une cellule uniquement, utilisée lors de la résolution
        :param coordinates: coordonnée de la cellule à mettre à jour
        :param all_events: ensemble des évenements en cours
        """
        test_errors(coordinates=coordinates)
        if not all_events: all_events = pygame.event.get()
        
        self.cell_display_element(coordinates)
        
        for event in all_events:
            if event.type == pygame.QUIT:
                self.do_quit = True
                return
        
            if event.type == pygame.WINDOWRESIZED:
                self.update_rect()
                self.display_elements()
        
        
        pygame.display.flip()
        
    def cell_display_element(self, coordinates: tuple[int, int]):
        """
        mise à jour rapide d'une cellule uniquement, utilisée lors de la résolution
        :param coordinates: coordonnées de la cellule à mettre à jour
        """
        # Test de préconditions
        test_errors(coordinates=coordinates)

        x, y = coordinates
        # Dimensions de la case à mettre à jour en fonction de la grille
        image_rect_area = pygame.Rect(
            self.grid_image_rect.width / 9 * x,
            self.grid_image_rect.height / 9 * y,
            self.grid_image_rect.width / 9,
            self.grid_image_rect.height / 9)
        
        # Affichage du fond d'écran de la case
        self.screen.blit(self.grid_image, self.all_rect[x][y], area = image_rect_area)
        
        # Affichage du cadena si la case est "locked"
        if self.sudoku.grid.get_cell_state((x, y)) == "locked":
            self.screen.blit(self.padlock_image, self.all_rect[x][y], area = image_rect_area)
        
        # affichage du texte (numéro) pour chaque cellule
        self.screen.blit(
            self.sudoku.grid.get_cell((x, y)).text.get_text(),
            self.all_rect[x][y].center
        )
    
    def update(self):
        """
        Exécute les actions nécessaires au bon fonctionnement du jeu
        """
        
        self.display_elements()
        
        # Pour tous les évènements qui ont eu lieu depuis la dernière mise à jour de la fenêtre
        for event in pygame.event.get():
            
            # Si l'un des évènements est de quitter la fenêtre
            if event.type == pygame.QUIT:
                # Mettre la variable indiquant s'il faut fermer la fenêtre à True
                self.do_quit = True
                return
            
            # Si l'un des évènements est un redimensionnement de a fenêtre
            if event.type == pygame.WINDOWRESIZED:
                # Mettre à jour la position des éléments de la fenêtre
                self.update_rect()
                
            if self.is_solving:  # ne pas vérifier les autres event si la résolution est en cours (economie performance)
                continue
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.sudoku.deselect_cell()
                
                if event.key == pygame.K_LEFT:
                    self.sudoku.move_selected_cell("left")
                
                if event.key == pygame.K_RIGHT:
                    self.sudoku.move_selected_cell("right")
                
                if event.key == pygame.K_UP:
                    self.sudoku.move_selected_cell("up")
                
                if event.key == pygame.K_DOWN:
                    self.sudoku.move_selected_cell("down")
                
                if event.key == pygame.K_l:
                    self.sudoku.lock_selected_cell()
                
                if event.key == pygame.K_u:
                    self.sudoku.unlock_selected_cell()

                if event.key == pygame.K_s:
                    
                    pygame.display.set_caption("Sudoku (solving...)")
                    self.sudoku.solve_grid()
                    pygame.display.set_caption("Sudoku")
                    
                
                if event.key == pygame.K_d:
                    self.sudoku.reverse_display_conflicts()
                    
                if event.key == pygame.K_c:
                    self.sudoku.clear()

                if event.key in self.key_mapping:
                    selected_cell = self.sudoku.selected_cell
                    if selected_cell != (-1, -1): # si une cellule est selectionnée
                        if self.sudoku.grid.get_cell_state(selected_cell) == "unlocked":
                        
                            # récupère la valeur a affecter à partir du dictionnaire self.key_mapping (chaque touche est associée à un entier entre 1 et 9)
                            value = self.key_mapping[event.key]
                            
                            # modifie la valeur de la cellule selectionnée
                            self.sudoku.set_selected_cell_value(value)
                            self.sudoku.verify_selected_cell() # vérifie si cette valeur est déjà présente sur la ligne, colonne, carré
                            
                        elif self.sudoku.grid.get_cell_state(selected_cell) == "locked":
                            print(f"grid.update(): cell {tuple(selected_cell)} is locked (press 'U' to Unlock)")
                        else: print(f"grid.update(): cell {tuple(selected_cell)} is superlocked")
                
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                for x in range(9):
                    for y in range(9):
                        if self.all_rect[x][y].collidepoint(pygame.mouse.get_pos()):
                            self.sudoku.select_cell((x, y))

        pygame.display.flip()
    
    def display_elements(self):
        """
        Permet de placer les éléments à afficher sur le brouillon de l'écran
        """
        
        # Affichage du fond d'écran
        pygame.draw.rect(self.screen, self.background_color, self.screen.get_rect())
        
        self.screen.blit(self.grid_image, self.grid_image_rect)

        for x in range(9):
            for y in range(9):
                if self.sudoku.grid.get_cell_state((x, y)) == "superlocked":
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
        if self.sudoku.selected_cell != (-1, -1):  # carré de sélection
            pygame.draw.rect(
                self.screen,
                (120, 120, 120),
                self.all_rect[self.sudoku.selected_cell[0]][self.sudoku.selected_cell[1]]
            )

        for x in range(9):
            for y in range(9):
                # affichage case locked (affichage du cadenas)
                if self.sudoku.grid.get_cell((x, y)).state == "locked":  # affichage des cases verrouillées
                    self.screen.blit(self.padlock_image, self.all_rect[x][y])
                
                # affichage du texte (numéro) pour chaque cellule
                self.screen.blit(
                    self.sudoku.grid.get_cell((x, y)).text.get_text(),
                    self.all_rect[x][y].center
                )
    
    def update_rect(self):
        """
        Calcul de la taille et des coordonnées des cellules
        """
        
        # Charge l'image de la grille
        self.grid_image = pygame.image.load("src/graphics/grid.png")
        
        # Si la longueur de la fenêtre est plus grande que sa largeur
        if self.screen.get_width() >= self.screen.get_height():
            # Dimensionner la grille en fonction de la hauteur de la fenêtre
            self.grid_image = pygame.transform.scale(
                self.grid_image,
                (self.screen.get_height(), self.screen.get_height())
            )
        
        else:
            # Sinon dimensionner la grille en fonction de la largeur de la fenêtre
            self.grid_image = pygame.transform.scale(
                self.grid_image,
                (self.screen.get_width(), self.screen.get_width())
            )
        
        # Variable stockant les coordonnées et les dimensions de la grille
        self.grid_image_rect = self.grid_image.get_rect()
        self.grid_image_rect.x = self.screen.get_width() / 2 - self.grid_image_rect.width / 2
        
        # Chargement de l'image du cadenas
        self.padlock_image = pygame.image.load("src/graphics/padlock.png")
        # Redimensionne l'image du cadenas à 1/4 de la hauteur et de la largeur d'un case
        self.padlock_image = pygame.transform.scale(
            self.padlock_image,
            (self.grid_image_rect.width / 9 / 4, self.grid_image_rect.height / 9 / 4)
        )
        
        # Variable contenant les coordonnées et les dimensions de toutes les cases de la grille
        self.all_rect = [[
            pygame.Rect(
                self.grid_image_rect.x + self.grid_image_rect.width / 9 * x,
                self.grid_image_rect.y + self.grid_image_rect.height / 9 * y,
                self.grid_image_rect.width / 9,
                self.grid_image_rect.height / 9
            )
            for y in range(9)] for x in range(9)]

        # recalcule et réattribue les valeurs de la taille des textes
        for x in range(9):
            for y in range(9):
                self.sudoku.grid.get_cell((x, y)).text.set_font_size(round(0.375 * self.all_rect[x][y].height))  # 0.375 est le rapport entre la taille d'un carré et la taille de la police
        
    def verify(self):
        """
        Vérifie et applique les modifications (changement de couleurs) si des cases sont identiques sur des lignes, colonnes, carrés
        """