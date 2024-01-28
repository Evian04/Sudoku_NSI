import tkinter.messagebox
import pygame
import json

from src.programs.sudoku import Sudoku
from src.programs.graphism import Graphism
from src.programs.test_errors import test_errors


class Game:
    """
    La classe Game permet de mettre à jour la fenêtre en mettant en relation les entrées
    de l'utilisateurs avec le contenu du sudoku et la gestion des graphismes
    """
    
    def __init__(self, screen: pygame.Surface, config_filepath: str):
        self._name: str = "Sudocool"
        self.screen: pygame.Surface = screen
        self._config_filepath: str = config_filepath  # chemin d'accès du fichier de configuration
        self._load_config_file()  # charge le fichier de configuration et met à jour l'attribut self.config_file
        
        self.do_quit: bool = False
        self.is_solving: bool = False
        
        self._do_display_during_solving: bool = self.get_config_value("do_display_during_solving")
        self._do_display_during_generating: bool = self.get_config_value("do_display_during_generating")
        
        self.values: str = "123456789ABCDEFG"  # Valeurs possibles pour les symboles (chiffre puis lettre)
        
        self.sudoku: Sudoku = Sudoku(self, grid_size=self.get_config_value("grid_size"))
        self.graphism: Graphism = Graphism(self, (0, 0, 0))
        
        self.title: str = f"{self._name} {self.sudoku.grid.size}x{self.sudoku.grid.size}"
        pygame.display.set_caption(self.title)  # Nom de la fenêtre
        
        self._key_mapping: dict[str] = {  # mapping des touches du clavier pour ajouter/modifier la valeur d'une case
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
        self._max_click_time: int = 250  # temps maximal entre deux clics pour être considéré comme un double clic
        self._current_time: int = 0
        self._last_clic: int = 0
        
        self.history: list[list[tuple[tuple[int, int], str]]] = list()
    
    def set_title(self, title: str = None, keep_base: bool = True):
        """
        defini le titre de la fenetre
        :param title: nouveau titre de la fenetre, si non spécifié utilise self.title
        :param keep_base: indique si self.title doit être utilisé, si c'est le cas, title sera ajouté à la fin
        """
        if title is None:
            title = self.title
            keep_base = False
        if self.sudoku.grid.get_is_editing():
            is_editing_text = " (mode edition)"
        else:
            is_editing_text = ""
        
        if keep_base:
            pygame.display.set_caption(self.title + is_editing_text + " " + title)
        else:
            pygame.display.set_caption(title + is_editing_text)
    
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
            
            # Si l'utilisateur effectue un clic gauche
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self._current_time = pygame.time.get_ticks()
                
                if self._current_time - self._last_clic < self._max_click_time and \
                        self.graphism.all_cell_rect[self.sudoku.selected_cell[0]][
                            self.sudoku.selected_cell[1]].collidepoint(pygame.mouse.get_pos()):
                    # double clic gauche - verrouiller ou déverrouiller une case (identique à Ctrl + L)
                    if self.sudoku.selected_cell == (-1, -1):
                        continue
                    
                    state = self.sudoku.grid.get_cell_state(self.sudoku.selected_cell)
                    
                    if state == 'unlocked':
                        self.sudoku.lock_selected_cell()
                    
                    elif state == 'locked':
                        self.sudoku.unlock_selected_cell()
                else:
                    # clic gauche simple - selectionner une case
                    self._last_clic = self._current_time
                    # Vérifier si le curseur de la souris est sur une case de la grille
                    for x in range(self.sudoku.grid.size):
                        for y in range(self.sudoku.grid.size):
                            if self.graphism.all_cell_rect[x][y].collidepoint(pygame.mouse.get_pos()):
                                # Sélectionner la case qui a été cliquée
                                self.sudoku.select_cell((x, y))
                    
                    if self.graphism.verification_button_rect.collidepoint(pygame.mouse.get_pos()):
                        self.graphism.reverse_display_conflicts()
                        self.update_config_file("do_check_values", self.graphism.do_display_conflicts)
                        self.graphism.update_verification_rect()
                    
                    elif self.graphism.solve_button_rect.collidepoint(pygame.mouse.get_pos()):
                        self.sudoku.solve_grid(self._do_display_during_solving)
                        self.sudoku.verify_grid()
                    
                    elif self.graphism.generate_button_rect.collidepoint(pygame.mouse.get_pos()):
                        self.sudoku.generate_grid(0.5, self._do_display_during_generating)
                        self.sudoku.verify_grid()
                    
                    elif self.graphism.open_button_rect.collidepoint(pygame.mouse.get_pos()):
                        self.sudoku.open_grid()
                    
                    elif self.graphism.save_button_rect.collidepoint(pygame.mouse.get_pos()):
                        self.sudoku.save_grid()
            
            if event.type == pygame.KEYDOWN:
                keys_pressed = pygame.key.get_pressed()
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
                
                if (keys_pressed[pygame.K_LCTRL] or keys_pressed[pygame.K_RCTRL]) and keys_pressed[pygame.K_c]:
                    # Ctrl + C - supprimer toutes les valeurs des cases déverrouillées
                    self.sudoku.clear()
                    self.sudoku.verify_grid()
                
                if (keys_pressed[pygame.K_LCTRL] or keys_pressed[pygame.K_RCTRL]) and keys_pressed[pygame.K_l]:
                    # Ctrl + L - verrouiller ou déverrouiller une case (s=identique au double clic))
                    if self.sudoku.selected_cell == (-1, -1):
                        continue
                    
                    state = self.sudoku.grid.get_cell_state(self.sudoku.selected_cell)
                    if state == 'unlocked':
                        self.sudoku.lock_selected_cell()
                    elif state == 'locked':
                        self.sudoku.unlock_selected_cell()
                
                if (keys_pressed[pygame.K_LCTRL] or keys_pressed[pygame.K_RCTRL]) and keys_pressed[pygame.K_e]:
                    # Ctrl + E - activer ou desactiver le mode Edition
                    self.sudoku.grid.set_is_editing()
                    self.set_title()  # ajoute ou non le texte relatif à l'edition, se base sur is_editing
                
                if self.sudoku.grid.get_is_editing() and keys_pressed[pygame.K_s] and (
                        not keys_pressed[pygame.K_LCTRL] and not keys_pressed[pygame.K_RCTRL]):
                    # touche S et si la grille est en edition - superlock ou unlock la case selectionnée
                    selected_cell = self.sudoku.selected_cell
                    if selected_cell == (-1, -1):
                        continue
                    if self.sudoku.grid.get_cell_state(selected_cell) == "unlocked":
                        if self.sudoku.grid.get_cell_value(selected_cell) != "0":
                            self.sudoku.grid.set_cell_state(selected_cell, "superlocked")
                        
                        else:
                            print(f"a superlocked cell must contain a value (cell coordinates:{selected_cell}")
                    
                    elif self.sudoku.grid.get_cell_state(selected_cell) == "superlocked":
                        self.sudoku.grid.set_cell_state(selected_cell, "unlocked")
                
                if self.sudoku.grid.get_is_editing() and (
                        keys_pressed[pygame.K_LCTRL] or keys_pressed[pygame.K_RCTRL]) and keys_pressed[pygame.K_s]:
                    # Ctrl + s - déverrouiller toutes les cases, y compris les superlocked
                    response = tkinter.messagebox.askyesnocancel("Voulez-vous déverrouiller toutes les cases",
                                                                 "Voulez-vous déverrouillez toutes les cases (état: unlocked) ?")
                    if response:
                        for x in range(self.sudoku.grid.size):
                            for y in range(self.sudoku.grid.size):
                                self.sudoku.grid.set_cell_state((x, y), "unlocked")
                if (keys_pressed[pygame.K_LCTRL] or keys_pressed[pygame.K_RCTRL]) and keys_pressed[pygame.K_z]:
                    # Ctrl + z - annuler la dernière action
                    self.restore_history_element()  # remet la valeur de la(es) dernière case(s) modifiées au même moment
                
                if event.key in self._key_mapping and not (keys_pressed[pygame.K_LCTRL] or keys_pressed[
                    pygame.K_RCTRL]):  # Si l'action est de modifier une case de la grille
                    # Si aucune case n'est sélectionnée, ne rien faire
                    if self.sudoku.selected_cell == (-1, -1):
                        continue
                    
                    # Si la case sélectionnée est "locked", afficher un message console
                    if self.sudoku.grid.get_cell_state(self.sudoku.selected_cell) == "locked":
                        print(f'Cell {self.sudoku.selected_cell} is already locked (press Ctrl+L to unlock)')
                        continue
                    
                    # récupère la valeur a affecter à partir du dictionnaire self.key_mapping (chaque touche est associée à un entier entre 0 et 9)
                    value = self._key_mapping[event.key]
                    
                    # Teste si la valeur n'est pas autorisé pour cette grille (trop grande ou inexistante)
                    if value not in self.values[:self.sudoku.grid.size] and value != "0":
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
        
        test_errors(self.sudoku.grid.size, coordinates=coordinates)
        
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
                self.graphism.display_elements()
                
                pygame.display.flip()
    
    def add_history_element(self, cell_coordinates: tuple[int, int], previous_value: str, index: int = None):
        """
        ajoute un élément à l'historique
        :param cell_coordinates: coordonnées de la cellule
        :param previous_value: dernière valeur de la cellule
        :param index: indice de l'élément à modifier dans l'historique, -1 est le dernier élément, si non spécifié, création d'un nouvel élément
        """
        test_errors(sudoku_size=self.sudoku.grid.size, coordinates=cell_coordinates, value=previous_value)
        if index:
            test_errors(generic_list=self.history, index=index)
            self.history[index].append((cell_coordinates, previous_value))
        else:
            self.history.append([(cell_coordinates, previous_value)])
    
    def get_history_element(self, index: int = -1) -> list[tuple[tuple[int, int], str]]:
        """
        recupère un élément de l'historique
        :param index: indice de l'élement à récupérer, -1 pour la dernière valeur
        :return: l'élement correspondant à l'indice sous la forme [(coordonnées, ancienne_valeur, nouvelle_valeur), ...]
        """
        test_errors(generic_list=self.history, index=index)
        if self.history:
            return self.history[index]
        else:
            return [((-1, -1), '0')]
    
    def restore_history_element(self, index: int = -1, do_deleted: bool = True):
        """
        restaure la(es) cellule(s) spécifiée(s) en index avec la(es) valeur(s) spécifiée(s) en index, elle(s) n'est(sont) pas enregidtrée(s)
        :param index: indice de la(es) case(s) à restaurer
        :param do_deleted: s'il faut supprimer cet élément

        """
        test_errors(generic_list=self.history, index=index)
        history_element = self.get_history_element(index)
        if history_element[0][0] == (-1, -1):  # signifie qu'il n'y a pas plus d'historique
            return False
        
        for coordinates, previous_value in history_element:
            self.sudoku.grid.set_cell_value(coordinates, previous_value)
        if do_deleted: self.remove_history_element(index)
    
    def remove_history_element(self, index: int = -1):
        test_errors(generic_list=self.history, index=index)
        self.history.pop(index)
    
    def _load_config_file(self):
        """
        Charge le fichier de configuration spécifié à self.config_filepath
        attribut self.config_file mis à jour
        """
        
        with open(self._config_filepath) as file:
            self.config_file = json.load(fp=file)
    
    def get_config_value(self, key: str):
        """
        recupère une valeur de configuration
        :param key: configuration à récupérer (clé)
        :return: valeur obtenue (différents types int, bool, etc)
        """
        
        test_errors(config_file=self.config_file, config_key=key)
        
        return self.config_file[key]
    
    def update_config_file(self, key: str, value):
        """
        met à jour le fichier de configuration
        :param key: clé de l'élément à mettre à jour
        :param value: nouvelle valeur
        """
        
        test_errors(config_file=self.config_file, config_key=key)
        
        self.config_file[key] = value
        
        with open(self._config_filepath, "w") as file:
            file.write(json.dumps(self.config_file))
