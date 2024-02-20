import tkinter.messagebox
import pygame
import json

from src.programs.sudoku import Sudoku
from src.programs.graphism import Graphism
from src.programs.test_errors import test_errors


class Game:
    """
    La classe Game permet de mettre en relation les entrées de l'utilisateurs avec la grille du sudoku et la gestion de l'affichage
    """
    
    def __init__(self, screen: pygame.Surface):
        self.do_quit = False
        self.screen: pygame.Surface = screen
        
        self.is_solving = False
        self.is_options_open = False
        
        self.load_config_file()  # charge le fichier de configuration et met à jour l'attribut self.config_file
        self.do_display_during_solving = self.get_config_value("do_display_during_solving")
        
        self.possible_values = "123456789ABCDEFG"  # Valeurs possibles pour les symboles (chiffre puis lettre)
        
        self.sudoku = Sudoku(self, 9)
        self.graphism = Graphism(
            self,
            self.sudoku.grid.size,
            (0, 0, 0),
            self.get_config_value("texture_pack"),
            self.get_config_value("do_display_conflicts")
        )
        
        self.name = "Sudokool"
        self.update_title()
        
        self.key_mapping: dict[str] = {  # mapping des touches du clavier pour ajouter/modifier la valeur d'une case
            pygame.K_1:         '1',
            pygame.K_KP_1:      '1',
            pygame.K_2:         '2',
            pygame.K_KP_2:      '2',
            pygame.K_3:         '3',
            pygame.K_KP_3:      '3',
            pygame.K_4:         '4',
            pygame.K_KP_4:      '4',
            pygame.K_5:         '5',
            pygame.K_KP_5:      '5',
            pygame.K_6:         '6',
            pygame.K_KP_6:      '6',
            pygame.K_7:         '7',
            pygame.K_KP_7:      '7',
            pygame.K_8:         '8',
            pygame.K_KP_8:      '8',
            pygame.K_9:         '9',
            pygame.K_KP_9:      '9',
            pygame.K_a:         "A",
            pygame.K_b:         "B",
            pygame.K_c:         "C",
            pygame.K_d:         "D",
            pygame.K_e:         "E",
            pygame.K_f:         "F",
            pygame.K_g:         "G",
            
            pygame.K_BACKSPACE: "0",  # 0 correspond à une case vide (supprime la valeur de la case)
            pygame.K_DELETE:    "0",
            pygame.K_0:         "0",
            pygame.K_KP_0:      "0"
        }
        
        self.graphism.update_rect()
    
    def update_title(self, title: str = ""):
        """
        defini le titre de la fenetre
        :param title: nouveau titre de la fenetre, si non spécifié utilise self.title
        """
        
        if title == "":
            pygame.display.set_caption(self.name + f"{self.sudoku.grid.size}x{self.sudoku.grid.size} - " + self.sudoku.game_mode)
            
        else:
            pygame.display.set_caption(title)
    
    def update(self, do_display: bool = True):
        """
        Exécute les actions nécessaires au bon fonctionnement du jeu
        """
        
        if do_display:
            if self.is_options_open:
                self.graphism.display_options_elements()
                
            else:
                self.graphism.display_main_elements()
        
        all_events = pygame.event.get()
        is_ctrl_pressed = pygame.key.get_pressed()[pygame.K_LCTRL] or pygame.key.get_pressed()[pygame.K_RCTRL]
        
        # Pour tous les évènements qui ont eu lieu depuis la dernière mise à jour de la fenêtre
        for event in all_events:
            
            if event.type == pygame.QUIT:
                self.do_quit = True
                return
            
            # Si la fenètre est redimensionnée
            elif event.type == pygame.WINDOWRESIZED:
                # Mettre à jour la position / dimensions des éléments de la fenêtre
                self.graphism.update_rect()
                pygame.display.flip()
            
            # Ne pas vérifier les autres event si la résolution est en cours (économie performance)
            if self.is_solving:
                continue
            
            # Si l'utilisateur clique sur l'écran
            elif event.type == pygame.MOUSEBUTTONDOWN:
                
                mouse_pos = pygame.mouse.get_pos()
                
                # Si le menu d'options est ouvert
                if self.is_options_open:
                    
                    # S'il s'agit d'un clique gauche
                    if event.button == pygame.BUTTON_LEFT:
                        
                        if self.graphism.dimensions_button_rect.collidepoint(mouse_pos):
                            
                            if self.sudoku.grid.size == 4:
                                is_action_successful = self.sudoku.new_empty_grid(9)
                            
                            elif self.sudoku.grid.size == 9:
                                is_action_successful = self.sudoku.new_empty_grid(16)
                            
                            else:
                                is_action_successful = self.sudoku.new_empty_grid(4)
                            
                            if is_action_successful:
                                self.graphism.update_grid_attributes(self.sudoku.grid.size)
                                self.graphism.update_dimensions_button_rect()
                        
                        elif self.graphism.generate_button_rect.collidepoint(mouse_pos):
                            self.sudoku.generate_grid(0.5)
                            self.sudoku.verify_grid()
                        
                        elif self.graphism.game_mode_button_rect.collidepoint(mouse_pos):
                            self.sudoku.reverse_game_mode()
                            self.graphism.update_game_mode_button_rect()
                        
                        elif self.graphism.change_textures_button_rect.collidepoint(mouse_pos):
                            self.graphism.ask_texture_pack()
                        
                        elif self.graphism.display_errors_button_rect.collidepoint(mouse_pos):
                            self.graphism.reverse_display_conflicts()
                            self.graphism.update_display_errors_button_rect()
                            self.set_config_value("do_display_conflicts", self.graphism.do_display_conflicts)
                        
                        elif self.graphism.display_solving_button_rect.collidepoint(mouse_pos):
                            self.do_display_during_solving = not self.do_display_during_solving
                            self.graphism.update_display_solving_button_rect()
                
                # Si le menu principal est affiché
                else:
                    # S'il s'agit d'un clique gauche
                    if event.button == pygame.BUTTON_LEFT:
                        # Si le curseur de la souris est sur une case de la grille
                        for x in range(self.sudoku.grid.size):
                            for y in range(self.sudoku.grid.size):
                                if self.graphism.all_cell_rect[x][y].collidepoint(mouse_pos):
                                    # Sélectionner la case qui a été cliquée
                                    self.sudoku.select_cell((x, y))
                        
                        if self.graphism.solve_button_rect.collidepoint(mouse_pos):
                            self.sudoku.solve_grid(self.do_display_during_solving)
                            self.sudoku.verify_grid()
                        
                        elif self.graphism.save_button_rect.collidepoint(mouse_pos):
                            self.sudoku.save_grid()
                        
                        elif self.graphism.open_button_rect.collidepoint(mouse_pos):
                            self.sudoku.open_grid()
                        
                        elif self.graphism.options_button_rect.collidepoint(mouse_pos):
                            self.is_options_open = True

                    # Si l'utilisateur effectue un clique droit
                    elif event.button == pygame.BUTTON_RIGHT:
                        
                        for x in range(self.sudoku.grid.size):
                            for y in range(self.sudoku.grid.size):
                                
                                # Si la souris est sur l'une des cases de la grille
                                if self.graphism.all_cell_rect[x][y].collidepoint(mouse_pos):
                                    
                                    # Inverser l'état de verrouillage de la case en question
                                    self.sudoku.reverse_cell_lock((x, y))
            
            if event.type == pygame.KEYDOWN:
                
                if event.key == pygame.K_ESCAPE:
                    
                    if self.is_options_open:
                        self.is_options_open = False
                        
                    else:
                        self.sudoku.deselect_cell()
                
                if event.key == pygame.K_LEFT:
                    self.sudoku.move_selected_cell("left")
                
                if event.key == pygame.K_RIGHT:
                    self.sudoku.move_selected_cell("right")
                
                if event.key == pygame.K_UP:
                    self.sudoku.move_selected_cell("up")
                
                if event.key == pygame.K_DOWN:
                    self.sudoku.move_selected_cell("down")
                
                if event.key == pygame.K_c and is_ctrl_pressed:
                    # Ctrl + C - supprime toutes les valeurs des cases déverrouillées
                    self.sudoku.clear()
                    self.sudoku.verify_grid()
                
                if event.key == pygame.K_l and is_ctrl_pressed:
                    # Si aucune case n'est sélectionnées, ne rien faire
                    if self.sudoku.selected_cell == (-1, -1):
                        continue
                    
                    # Ctrl + L - Verrouille ou déverrouille une case (identique au clique droit)
                    self.sudoku.reverse_selected_cell_lock()
                
                if event.key == pygame.K_z and is_ctrl_pressed:
                    # Ctrl + z : annuler la dernière action
                    self.sudoku.move_index_history("backward")
                
                if event.key == pygame.K_y and is_ctrl_pressed:
                    # Ctrl + y : restaurer l'action annulée
                    self.sudoku.move_index_history("forward")
                
                if event.key == pygame.K_m and is_ctrl_pressed:
                    self.sudoku.reverse_game_mode()
                    self.update_title()
                
                if event.key in self.key_mapping and not is_ctrl_pressed:
                    # Si aucune case n'est sélectionnée, ne rien faire
                    if self.sudoku.selected_cell == (-1, -1):
                        continue
                    
                    # Si la valeur n'est pas compatible avec la taille de la grille actuelle, ne rien faire
                    if not self.key_mapping[event.key] in "0" + self.possible_values[:self.sudoku.grid.size]:
                        continue
                    
                    # récupère la valeur à affecter à partir du dictionnaire self.key_mapping
                    value = self.key_mapping[event.key]
                    
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
                return False
            
            if event.type == pygame.WINDOWRESIZED:
                self.graphism.update_rect()
                self.graphism.display_main_elements()
                
                pygame.display.flip()
    
    def load_config_file(self):
        """
        Charge le fichier de configuration spécifié à self.config_filepath
        attribut self.config_file mis à jour
        """
        
        with open("src/config.json") as file:
            self.config_file = json.load(fp = file)
    
    def get_config_value(self, key: str):
        """
        recupère une valeur de configuration
        :param key: configuration à récupérer (clé)
        :return: valeur obtenue (différents types int, bool, etc)
        """
        
        test_errors(config_file = self.config_file, config_key = key)
        
        return self.config_file[key]
    
    def set_config_value(self, key: str, value):
        """
        met à jour le fichier de configuration
        :param key: clé de l'élément à mettre à jour
        :param value: nouvelle valeur
        """
        
        test_errors(config_file = self.config_file, config_key = key, config_value = value)
        
        self.config_file[key] = value
        
        with open("src/config.json", "w") as file:
            file.write(json.dumps(self.config_file))
