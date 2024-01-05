import pygame

import time

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
        
        self.do_display_during_solving = True
        
        self.values = "123456789ABCDEFGHIJKLMNOP"  # TEST # Valeurs possibles pour les symboles (chiffre puis lettre)

        self.sudoku = Sudoku(self, grid_size = grid_size)
        self.graphism = Graphism(self, (0, 0, 0))
        
        self.title = f"Sudoku {self.sudoku.grid.size}x{self.sudoku.grid.size}"
        pygame.display.set_caption(self.title)  # Nom de la fenêtre
        
        self.key_mapping = {  # mapping des touches du clavier pour ajouter/modifier la valeur d'une case
            pygame.K_1:         '1',
            pygame.K_2:         '2',
            pygame.K_3:         '3',
            pygame.K_4:         '4',
            pygame.K_5:         '5',
            pygame.K_6:         '6',
            pygame.K_7:         '7',
            pygame.K_8:         '8',
            pygame.K_9:         '9',
            pygame.K_KP_1:      '1',
            pygame.K_KP_2:      '2',
            pygame.K_KP_3:      '3',
            pygame.K_KP_4:      '4',
            pygame.K_KP_5:      '5',
            pygame.K_KP_6:      '6',
            pygame.K_KP_7:      '7',
            pygame.K_KP_8:      '8',
            pygame.K_KP_9:      '9',
            pygame.K_a:         "A",
            pygame.K_b:         "B",
            pygame.K_c:         "C",
            pygame.K_d:         "D",
            pygame.K_e:         "E",
            pygame.K_f:         "F",
            pygame.K_g:         "G",
            pygame.K_h:         "H",
            pygame.K_i:         "I",
            pygame.K_j:         "J",
            pygame.K_k:         "K",
            pygame.K_l:         "L",
            pygame.K_m:         "M",
            pygame.K_n:         "N",
            pygame.K_o:         "O",
            pygame.K_p:         "P",
            pygame.K_BACKSPACE: '0',  # 0 correspond à une case vide (supprime la valeur de la case)
            pygame.K_DELETE:    '0',
            pygame.K_0:         '0',
            pygame.K_KP_0:      '0'
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
            
            # Si la fenètre est redimensionnée
            if event.type == pygame.WINDOWRESIZED:
                # Mettre à jour la position / dimensions des éléments de la fenêtre
                self.graphism.update_rect()
                pygame.display.flip()
                
            # Ne pas vérifier les autres event si la résolution est en cours (économie performance)
            if self.is_solving:
                continue
            
            # Si l'utilisateur effectue un clique gauche
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # Vérifier si le curseur de la souris est sur une case de la grille
                for x in range(self.sudoku.grid.size):
                    for y in range(self.sudoku.grid.size):
                        if self.graphism.all_cell_rect[x][y].collidepoint(pygame.mouse.get_pos()):
                            # Sélectionner la case qui a été cliquée
                            self.sudoku.select_cell((x, y))
                
                if self.graphism.verification_button_rect.collidepoint(pygame.mouse.get_pos()):
                    self.graphism.reverse_display_conflicts()
                    self.graphism.update_verification_rect()
                
                elif self.graphism.solve_button_rect.collidepoint(pygame.mouse.get_pos()):
                    self.sudoku.solve_grid(self.do_display_during_solving)
                    self.sudoku.verify_grid()
                
                elif self.graphism.generate_button_rect.collidepoint(pygame.mouse.get_pos()):
                    self.sudoku.generate_grid()
                    
                elif self.graphism.open_button_rect.collidepoint(pygame.mouse.get_pos()):
                    self.sudoku.open_grid()
                    
                elif self.graphism.save_button_rect.collidepoint(pygame.mouse.get_pos()):
                    self.sudoku.save_grid()
            
            if event.type == pygame.KEYDOWN:
                touches = pygame.key.get_pressed()
                if touches[pygame.K_ESCAPE]:
                    self.sudoku.deselect_cell()
                
                if touches[pygame.K_LEFT]:
                    self.sudoku.move_selected_cell("left")
                
                if touches[pygame.K_RIGHT]:
                    self.sudoku.move_selected_cell("right")
                
                if touches[pygame.K_UP]:
                    self.sudoku.move_selected_cell("up")
                
                if touches[pygame.K_DOWN]:
                    self.sudoku.move_selected_cell("down")
                
                if (touches[pygame.K_LCTRL] or touches[pygame.K_RCTRL]) and touches[pygame.K_c]:
                    self.sudoku.clear()
                    self.sudoku.verify_grid()
                
                if (touches[pygame.K_LCTRL] or touches[pygame.K_RCTRL]) and touches[pygame.K_l]:
                    if self.sudoku.selected_cell == (-1, -1):
                        continue
                    
                    state = self.sudoku.grid.get_cell_state(self.sudoku.selected_cell)
                    
                    if state == 'unlocked':
                        self.sudoku.lock_selected_cell()
                        
                    elif state == 'locked':
                        self.sudoku.unlock_selected_cell()

                if event.key in self.key_mapping: # Si l'action est de modifier une case de la grille
                    
                    # Si aucune case n'est sélectionnée, ne rien faire
                    if self.sudoku.selected_cell == (-1, -1):
                        continue
                    
                    # Si la case sélectionnée est "superlocked", afficher un message console
                    if self.sudoku.grid.get_cell_state(self.sudoku.selected_cell) == "superlocked":
                        print(f"Cell {self.sudoku.selected_cell} is superlocked, you cannot change its value")
                        continue
                    
                    # Si la case sélectionnée est "locked", afficher un message console
                    if self.sudoku.grid.get_cell_state(self.sudoku.selected_cell) == "locked":
                        print(f'Cell {self.sudoku.selected_cell} is locked (press "l" to unlock)')
                        continue
                        
                    # récupère la valeur a affecter à partir du dictionnaire self.key_mapping (chaque touche est associée à un entier entre 0 et 9)
                    value = self.key_mapping[event.key]
                    if value not in self.values[:self.sudoku.grid.size] and value != "0": # cette valeur n'est pas autorisé pour cette grille (trop grande ou inexistante)
                        continue
                    # modifie la valeur de la case selectionnée
                    self.sudoku.set_selected_cell_value(value)
                    
                    # vérifie si cette valeur entre en conflit avec d'autres valeurs de la grille
                    self.sudoku.verify_grid()
        
        if do_display: pygame.display.flip()
    
    def cell_update(self, coordinates: tuple[int, int], do_display: bool = True):
        """
        Met à jour une case uniquement (gain de performance), utilisée lors de la résolution
        """
        
        test_errors(self.sudoku.grid.size, coordinates = coordinates)
        
        if do_display:
            self.graphism.display_cell_elements(coordinates)
            pygame.display.flip()
        
        all_events = pygame.event.get()
        
        for event in all_events:
            if event.type == pygame.QUIT:
                self.do_quit = True
                return
            
            if event.type == pygame.WINDOWRESIZED:
                self.graphism.update_rect()
                self.graphism.display_elements()
                
                pygame.display.flip()