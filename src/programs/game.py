import pygame

from src.programs.sudoku import Sudoku
from src.programs.graphism import Graphism
from src.programs.test_errors import test_errors


class Game:
    """
    La classe Game permet de mettre à jour la fenêtre en mettant en relation les entrées
    de l'utilisateurs avec le contenu du sudoku et la gestion des graphismes
    """
    
    def __init__(self, screen: pygame.Surface, grid_size: int):
        self.screen = screen
        self.do_quit = False
        self.is_solving = False
        
        self.graphism = Graphism(self, (0, 0, 0))
        
        self.sudoku = Sudoku(self, grid_size = grid_size)
        self.title = f"Sudoku {self.sudoku.grid.size}x{self.sudoku.grid.size}"
        pygame.display.set_caption(self.title)  # Nom de la fenêtre
        
        self.key_mapping = {  # mapping des touches du clavier pour ajouter/modifier la valeur d'une case
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
    
    def update(self, do_display: bool = True):
        """
        Exécute les actions nécessaires au bon fonctionnement du jeu
        """
        if do_display: self.graphism.display_elements()

        all_events = pygame.event.get()
        
        # Si l'un des évènements est de fermer la fenêtre
        if pygame.QUIT in [event.type for event in all_events]:
            # Mettre la variable indiquant s'il faut fermer la fenêtre à True
            self.do_quit = True
            return
        
        # Pour tous les évènements qui ont eu lieu depuis la dernière mise à jour de la fenêtre
        for event in all_events:
            
            # Si l'un des évènements est un redimensionnement de a fenêtre
            if event.type == pygame.WINDOWRESIZED:
                # Mettre à jour la position des éléments de la fenêtre
                self.graphism.update_rect()
                # met à jour l'écran ici que si do_display est à False (éviter de le faire 2 fois)
                if not do_display: pygame.display.flip()
            
            if self.is_solving:  # ne pas vérifier les autres event si la résolution est en cours (économie performance)
                continue
            
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for x in range(self.sudoku.grid.size):
                    for y in range(self.sudoku.grid.size):
                        if self.graphism.all_cell_rect[x][y].collidepoint(pygame.mouse.get_pos()):
                            self.sudoku.select_cell((x, y))
                
                if self.graphism.verification_button_rect.collidepoint(pygame.mouse.get_pos()):
                    self.graphism.reverse_display_conflicts()
                    self.graphism.update_buttons_rect()
                
                elif self.graphism.solve_button_rect.collidepoint(pygame.mouse.get_pos()):
                    self.sudoku.solve_grid()
                
                elif self.graphism.generate_button_rect.collidepoint(pygame.mouse.get_pos()):
                    self.sudoku.generate_grid()
                    
                elif self.graphism.open_button_rect.collidepoint(pygame.mouse.get_pos()):
                    self.sudoku.open_grid()
                    
                elif self.graphism.save_button_rect.collidepoint(pygame.mouse.get_pos()):
                    self.sudoku.save_grid()
            
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
                
                if event.key == pygame.K_c:
                    self.sudoku.clear()

                if event.key in self.key_mapping: # Si l'action est de modifier une case de la grille
                    
                    if self.sudoku.selected_cell == (-1, -1): # Si aucune case n'est sélectionnée
                        continue # Ne rien faire
                        
                    if self.sudoku.grid.get_cell_state(self.sudoku.selected_cell) == "unlocked":
                        
                        # récupère la valeur a affecter à partir du dictionnaire self.key_mapping (chaque touche est associée à un entier entre 0 et 9)
                        value = self.key_mapping[event.key]
                        
                        # modifie la valeur de la case selectionnée
                        self.sudoku.set_selected_cell_value(value)
                        self.sudoku.verify_selected_cell()  # vérifie si cette valeur est déjà présente sur la ligne, colonne, carré
                    
                    elif self.sudoku.grid.get_cell_state(self.sudoku.selected_cell) == "locked":
                        print(f"grid.update(): cell {tuple(self.sudoku.selected_cell)} is locked (press 'U' to Unlock)")
                        
                    else:
                        print(f"grid.update(): cell {tuple(self.sudoku.selected_cell)} is superlocked")
        
        if do_display: pygame.display.flip()
    
    def cell_update(self, coordinates: tuple[int, int], do_display: bool = True, all_events: list[pygame.event.Event] = None):
        """
        mise à jour rapide d'une case uniquement, utilisée lors de la résolution
        :param coordinates: coordonnée de la case à mettre à jour
        :param all_events: ensemble des évenements en cours
        """
        test_errors(self.sudoku.grid.size, coordinates=coordinates)
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