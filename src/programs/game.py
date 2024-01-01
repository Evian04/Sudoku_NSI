import pygame

from src.programs.sudoku import Sudoku
from src.programs.graphism import Graphism
from src.programs.test_errors import test_errors


class Game:
    
    def __init__(self, screen: pygame.Surface, grid_size: int):
        self.screen = screen
        self.do_quit = False
        self.is_solving = False
        
        self.graphism = Graphism(self, (0, 0, 0))
        
        self.sudoku = Sudoku(self, grid_size = grid_size)
        self.title = f"Sudoku {self.sudoku.grid.size}x{self.sudoku.grid.size}"
        pygame.display.set_caption("Sudoku")  # Nom de la fenêtre
        
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
        self.graphism.update_rect()
    
    def cell_update(self, coordinates: tuple[int, int], do_display: bool = True, all_events: list[pygame.event.Event] = None):
        """
        mise à jour rapide d'une cellule uniquement, utilisée lors de la résolution
        :param coordinates: coordonnée de la cellule à mettre à jour
        :param all_events: ensemble des évenements en cours
        """
        test_errors(coordinates=coordinates)
        if not all_events: all_events = pygame.event.get()
        
        if do_display: self.graphism.cell_display_element(coordinates)
        
        for event in all_events:
            if event.type == pygame.QUIT:
                self.do_quit = True
                return
            
            if event.type == pygame.WINDOWRESIZED:
                self.graphism.update_rect()
                self.graphism.display_elements()
                # met à jour l'écran ici que si do_display est à False (éviter de le faire 2 fois)
                if not do_display: pygame.display.flip()
                
        if do_display: pygame.display.flip()
    
    def update(self, do_display: bool = True):
        """
        Exécute les actions nécessaires au bon fonctionnement du jeu
        """
        if do_display: self.graphism.display_elements()

        all_events = pygame.event.get()
        
        # Pour tous les évènements qui ont eu lieu depuis la dernière mise à jour de la fenêtre
        for event in all_events:
            
            # Si l'un des évènements est de quitter la fenêtre
            if event.type == pygame.QUIT:
                # Mettre la variable indiquant s'il faut fermer la fenêtre à True
                self.do_quit = True
                return
            
            # Si l'un des évènements est un redimensionnement de a fenêtre
            if event.type == pygame.WINDOWRESIZED:
                # Mettre à jour la position des éléments de la fenêtre
                self.graphism.update_rect()
                # met à jour l'écran ici que si do_display est à False (éviter de le faire 2 fois)
                if not do_display: pygame.display.flip()
            
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
                    if self.sudoku.selected_cell == (-1, -1):
                        continue
                    
                    state = self.sudoku.grid.get_cell_state(self.sudoku.selected_cell)
                    
                    if state == 'unlocked':
                        self.sudoku.lock_selected_cell()
                        
                    elif state == 'locked':
                        self.sudoku.unlock_selected_cell()
                
                if event.key == pygame.K_s:
                    pygame.display.set_caption(self.title + " (solving...)")
                    self.sudoku.solve_grid()
                    pygame.display.set_caption(self.title)
                
                if event.key == pygame.K_d:
                    self.sudoku.reverse_display_conflicts()
                
                if event.key == pygame.K_c:
                    self.sudoku.clear()
                
                if event.key == pygame.K_g:
                    pygame.display.set_caption(self.title + " (generating...)")
                    self.sudoku.generate_grid(4)
                    pygame.display.set_caption(self.title)

                if event.key in self.key_mapping:
                    selected_cell = self.sudoku.selected_cell
                    if selected_cell != (-1, -1):  # si une cellule est selectionnée
                        if self.sudoku.grid.get_cell_state(selected_cell) == "unlocked":
                            
                            # récupère la valeur a affecter à partir du dictionnaire self.key_mapping (chaque touche est associée à un entier entre 1 et 9)
                            value = self.key_mapping[event.key]
                            
                            # modifie la valeur de la cellule selectionnée
                            self.sudoku.set_selected_cell_value(value)
                            self.sudoku.verify_selected_cell()  # vérifie si cette valeur est déjà présente sur la ligne, colonne, carré
                        
                        elif self.sudoku.grid.get_cell_state(selected_cell) == "locked":
                            print(f"grid.update(): cell {tuple(selected_cell)} is locked (press 'U' to Unlock)")
                        else:
                            print(f"grid.update(): cell {tuple(selected_cell)} is superlocked")
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                for x in range(self.sudoku.grid.size):
                    for y in range(self.sudoku.grid.size):
                        if self.graphism.all_cell_rect[x][y].collidepoint(pygame.mouse.get_pos()):
                            self.sudoku.select_cell((x, y))
        
        if do_display: pygame.display.flip()
    
    def verify(self):
        """
        Vérifie et applique les modifications (changement de couleurs) si des cases sont identiques sur des lignes, colonnes, carrés
        """
