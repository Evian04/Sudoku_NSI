import random
import time
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter.messagebox import askyesnocancel, showinfo

from src.programs.grid import Grid
from src.programs.test_errors import test_errors


class Sudoku:
    """
    La classe "Sudoku" permet d'effectuer des actions complexes sur la grille,
    telles que la résoudre, en charger une depuis un fichier, ou encore en générer une nouvelle
    """
    
    def __init__(self, game, grid_size: int):
        
        # Test préconditions
        test_errors(grid_size)
        
        self.is_grid_saved = False
        self.game = game
        
        self.game_mode = "editing"
        
        self.grid = Grid(grid_size)
        
        self.history: list[Grid] = [self.grid.copy()]
        self.history_index = 0
        
        self.save_state_conversion = {"unlocked": "0", "locked": "1", "superlocked": "2"}
        self.load_state_conversion = {"0": "unlocked", "1": "locked", "2": "superlocked"}
        
        self.selected_cell = (-1, -1)  # Coordonnées de la case sélectionnée, (-1, -1) si aucune case
        self.conflicting_cells: list[tuple[int, int]] = list()
    
    def reverse_game_mode(self):
        """
        Met le mode de jeu sur "playing" s'il était sur "editing" et inversement
        """
        
        if self.game_mode == "playing":
            self.game_mode = "editing"
            
        else:
            self.game_mode = "playing"
        
        # Test postconditions
        test_errors(game_mode = self.game_mode)
    
    def set_game_mode(self, game_mode: str):
        """
        Attribue à la variable "game_mode" la valeur indiquée
        """
        
        # Test préconditions
        test_errors(game_mode = game_mode)
        
        self.game_mode = game_mode
        print(f"The game mode was set to {game_mode}")
    
    def select_cell(self, coordinates: tuple[int, int]):
        """
        Selectionne la case de coordonnées (x, y)
        """
        
        # Test préconditions
        test_errors(self.grid.size, coordinates = coordinates)
        
        # Code de la fonction
        self.selected_cell = coordinates
    
    def deselect_cell(self):
        """
        Déselectionne la case sélectionnée
        """
        
        # Code de la fonction
        self.selected_cell = (-1, -1)
    
    def move_selected_cell(self, direction: str):
        """
        Déplace les coordonnées de la case sélctionnées vers la direction indiquée
        """
        
        # Test des préconditions
        test_errors(direction = direction)
        
        # Si aucune case n'est sélectionnée
        if self.selected_cell == (-1, -1):
            return
        
        match direction:
            
            case "left":
                # Si la sélection est au bord de la grille dans la direction indiquée
                if self.selected_cell[0] == 0:
                    return
                
                # Déplacer la sélection d'une case vers la gauche
                self.selected_cell = (self.selected_cell[0] - 1, self.selected_cell[1])
            
            case "right":
                # Si la sélection est au bord de la grille dans la direction indiquée
                if self.selected_cell[0] == self.grid.size - 1:
                    return
                
                # Déplacer la sélection d'une case vers la droite
                self.selected_cell = (self.selected_cell[0] + 1, self.selected_cell[1])
            
            case "up":
                # Si la sélection est au bord de la grille dans la direction indiquée
                if self.selected_cell[1] == 0:
                    return
                
                # Déplacer la sélection d'une case vers le haut
                self.selected_cell = (self.selected_cell[0], self.selected_cell[1] - 1)
            
            case "down":
                # Si la sélection est au bord de la grille dans la direction indiquée
                if self.selected_cell[1] == self.grid.size - 1:
                    return
                
                # Déplacer la sélection d'une case vers le bas
                self.selected_cell = (self.selected_cell[0], self.selected_cell[1] + 1)
        
        # Test des postconditions
        test_errors(self.grid.size, coordinates = self.selected_cell)
    
    def set_selected_cell_value(self, value: str):
        """
        Met la valeur de la case sélectionnée à "value"
        """
        
        # Test des préconditions
        test_errors(self.grid.size, coordinates = self.selected_cell, value = value)
        
        if self.game_mode == "playing" and self.grid.get_cell_state(self.selected_cell) in ["locked", "superlocked"]:
            print(
                f"The cell {self.selected_cell} is {self.grid.get_cell_state(self.selected_cell)}, You cannot change its value while playing"
            )
            
            return
        
        self.grid.set_cell_value(self.selected_cell, value)
        print(f"The value of the cell {self.selected_cell} was set to {value}")
        
        self.save_grid_in_history()
        self.is_grid_saved = False
     
    def reverse_selected_cell_lock(self):
        """
        Inverse l'état de verrouillage de la case sélectionnée
        """
        
        # Test préconditions
        test_errors(coordinates = self.selected_cell)
        
        self.reverse_cell_lock(self.selected_cell)
    
    def reverse_cell_lock(self, coordinates: tuple[int, int]):
        """
        Inverse l'état de verrouillage de la case indiquée
        """
        
        # Test préconditions
        test_errors(self.grid.size, coordinates = coordinates)
        
        is_grid_changed = False
        
        # Si le mode de jeu est sur "playing"
        if self.game_mode == "playing":
            match self.grid.get_cell_state(coordinates):
                
                # Si la case est "unlocked"
                case "unlocked":
                    # Mettre l'état de la case à "locked"
                    self.grid.set_cell_state(coordinates, "locked")
                    print(f"The cell {coordinates} was locked")
                    is_grid_changed = True
                
                # Si la case est "locked"
                case "locked":
                    # Mettre l'état de la case à "unlocked"
                    self.grid.set_cell_state(coordinates, "unlocked")
                    print(f"The cell {coordinates} was unlocked")
                    is_grid_changed = True
                
                # Si la case est "superlocked"
                case "superlocked":
                    # Afficher un message d'erreur dans la console
                    print(f'The cell {coordinates} is superlocked, you cannot change its value while being in "playing" gam mode')
        
        # Si le mode de jeu est sur "editing"
        else:
            match self.grid.get_cell_state(coordinates):
                
                # Si la case est "unlocked"
                case "unlocked":
                    # Mettre l'état de la case à "superlocked"
                    self.grid.set_cell_state(coordinates, "superlocked")
                    print(f"The cell {coordinates} was superlocked")
                    is_grid_changed = True
                
                # Si la case est "locked"
                case "locked":
                    # Mettre l'état de la case à "unlocked"
                    self.grid.set_cell_state(coordinates, "unlocked")
                    print(f"The cell {coordinates} was unlocked")
                    is_grid_changed = True
                
                # Si la case est "superlocked"
                case "superlocked":
                    # Mettre l'état de la case à "unlocked"
                    self.grid.set_cell_state(coordinates, "unlocked")
                    print(f"The cell {coordinates} was unlocked")
                    is_grid_changed = True
        
        self.save_grid_in_history()
        self.is_grid_saved = False
    
    def save_grid_in_history(self):
        """
        Sauvegarde la grille courante dans l'historique
        """
        
        # Si l'utilisateur est remonté dans l'historique, effacer les états de la grille qui ont été annulés
        if self.history_index < len(self.history) - 1:
            self.history = self.history[:self.history_index + 1]
            
        self.history.append(self.grid.copy())
        self.history_index = len(self.history) - 1
    
    def is_history_move_possible(self, move: str) -> bool:
        """
        Permet de savoir si il est possible d'aller en avant ou en arrière dans l'historique
        """
        
        # Test préconditions
        test_errors(history_move = move)
        
        if move == "backward":
            return self.history_index != 0
        
        elif move == "forward":
            return self.history_index != len(self.history) - 1
    
    def move_index_history(self, move: str):
        """
        Permet de se déplacer dans l'historique.
        move = "backward"  : Annule la dernière action
        move = "forward"   : Rétablie l'action annulée
        """
        
        # Test préconditions
        test_errors(history_move = move)
        
        if move == "backward":
            self.history_index -= 1
            
            if self.history_index < 0:
                self.history_index = 0
        
        elif move == "forward":
            self.history_index += 1
            
            if self.history_index >= len(self.history):
                self.history_index = len(self.history) -1
            
        self.grid = self.history[self.history_index].copy()
    
    def clear_history(self):
        """
        Vide l'historique.
        Fonction utilisée lors du chargement / génération d'une nouvelle grille / ouverture d'une nouvelle grille
        """
        
        self.history = [self.grid.copy()]
        self.history_index = 0
    
    def new_empty_grid(self, grid_size: int):
        """
        Génère une nouvelle grille vide avec la taille indiquée
        Renvois True si la grille a bien été crée, et False si l'action a été annulée
        """
        
        # Test préconditions
        test_errors(sudoku_size = grid_size)
        
        if not self.is_grid_saved and not self.grid.is_empty():
            do_save = askyesnocancel(
                "Sauvegarder la grille",
                f"Une nouvelle grille vierge de taille {grid_size}x{grid_size} va être générer et les données de la grille actuelle seront définitivement perdues.\nVoulez-vous sauvegarder la grille ?"
            )
            
            if do_save == None:
                return False
            
            if do_save:
                self.save_grid()
        
        self.clear_history()
        self.grid = Grid(grid_size)
        return True
    
    def open_grid(self):
        """
        Charge une grille à partir d'un fichier
        """
        
        # Ouvre une fenêtre de dialogue permettant à l'utilisateur de choisir le fichier à charger
        file_path = askopenfilename(
            initialdir = "src/save_folder",
            initialfile = "model_2.sdk",
            title = "Ouvrir",
            filetypes=[("Sudoku file", "*.sdk")]
        )
        
        # Dans le cas où l'utilisateur n'a pas sélectionné de fichier
        if not file_path:
            # Affiche un message en console et ne fait rien d'autre
            print("No file selected")
            return
        
        # Récupère le contenu du fichier sélectionné
        with open(file_path, "r") as file:
            file_content = file.read()
        
        # Formate le contenu du fichier dans les variables grid_size, all_values et all_states
        
        file_content = file_content.split("\n\n")
        
        grid_size = int(file_content[0])
        
        all_values = [[value for value in line] for line in file_content[1].split("\n")]
        all_states = [[self.load_state_conversion[state] for state in line] for line in file_content[2].split("\n")]
        
        # Test postconditions
        test_errors(grid_size, list_values = all_values, list_states = all_states)
        
        # Remplace le contenu de la grille par le contenu lu dans le fichier
        self.grid.reset_attributes(grid_size, all_values, all_states)
        
        print("Grid succesfully opened")
        
        self.is_grid_saved = True
        self.verify_grid()
        self.clear_history()
        self.set_game_mode("playing")
        self.game.update_title()
    
    def save_grid(self):
        """
        Enregistre la grille actuelle dans un fichier
        """
        
        # Récupère le chemin du fichier à sauvegarder
        filepath = asksaveasfilename(
            initialdir = "src/save_folder/",
            initialfile = 'saved_sudoku.sdk',
            title = f"Enregistrer",
            filetypes = [("Sudoku file", "*.sdk")]
        )
        
        # Si l'utilisateur n'a rien entré
        if not filepath:
            return
        
        # Formate les valeurs des cases de la grille en chaine de charactère
        all_values = "\n".join(["".join(line) for line in self.grid.get_all_values()])
        
        # Formate les états des cases de la grille en chaine de charactère
        all_states = "\n".join(["".join([self.save_state_conversion[state] for state in line]) for line in self.grid.get_all_states()])
        
        all_content = str(self.grid.size) + "\n\n" + all_values + "\n\n" + all_states
        
        # Ecrit le contenu obtenu dans un fichier
        with open(filepath, "w") as file:
            file.write(all_content)
            
        self.is_grid_saved = True
        print("Grid saved succesfully")
    
    def is_valid(self) -> bool:
        """
        Renvoie True si la grille ne comporte aucune erreurs, et False si elle en comporte au moins une
        """
        
        # Pour toutes les organisations de grille possibles (en lignes, en colonnes et en carrés)
        for all_values in [self.grid.get_all_values_as(format) for format in ["lines", "columns", "squares"]]:
            
            # Parcourir les sous-listes de cet ensemble de valeurs
            for sub_all_values in all_values:
                
                # Pour toutes les valeurs de case possible
                for value in self.game.possible_values[:self.grid.size]:
                    
                    # Si la valeur apparait plusieur fois dans la sous-liste
                    if sub_all_values.count(value) > 1:
                        return False
        
        # Si aucun doublon n'a été trouvé, renvoyer True
        return True
    
    def verify_grid(self):
        """
        Enregistre dans la variable "self.conflicting_cells" l'ensemble des coordonnées des cases en conflit
        """
        
        tmp_conflicting_cells = list()  # Liste temporaire dans laquelle seront stockées les coordonnées des cases en conflits
        
        # Pour tous les formats possibles
        for format in ["lines", "columns", "squares"]:
            all_values = self.grid.get_all_values_as(format)
            all_coordinates = self.grid.get_all_coordinates_as(format)
            
            # Parcourir les coordonnées en x possibles
            for x in range(self.grid.size):
                
                # Récupérer les groupes de valeurs et de coordonnées correspondant
                group_values = all_values[x]
                groupe_coordinates = all_coordinates[x]
                
                # Pour toutes les valeurs possibles
                for value in self.game.possible_values[:self.grid.size]:
                    
                    # Si cette valeur apparait plusieur fois dans le groupe de valeurs
                    if group_values.count(value) > 1:
                        
                        # Enregistrer dans "tmp_conflicting_cells" les coordonnées des cases ayant la valeur doublon
                        for y in range(self.grid.size):
                            if group_values[y] == value and not groupe_coordinates[y] in tmp_conflicting_cells:
                                tmp_conflicting_cells.append(groupe_coordinates[y])
                    
                    # Si la valeur n'apparait pas plusieur fois dans le groupe de valeurs
                    else:
                        # Supprimer les coordonnées des cases ayant cette valeur de la variable "self.conflicting_cells"
                        for y in range(self.grid.size):
                            if group_values[y] == value and groupe_coordinates[y] in self.conflicting_cells:
                                self.conflicting_cells.remove(groupe_coordinates[y])
        
        # Mise en commun de "tmp_conflicting_cells" et de "self.conflicting_cells"
        for x in range(self.grid.size):
            for y in range(self.grid.size):
                
                if (x, y) in tmp_conflicting_cells and not (x, y) in self.conflicting_cells:
                    self.conflicting_cells.append((x, y))
        
        self.update_cells_conflicting_state()
    
    def update_cells_conflicting_state(self):
        """
        Met à jour la variable "is_in_conflict" de toutes les cases de la grille
        """
        
        for x in range(self.grid.size):
            for y in range(self.grid.size):
                self.grid.set_cell_conflicting_state((x, y), (x, y) in self.conflicting_cells)
    
    def generate_grid(self, cell_frequency: float, do_show_messagebox: bool = True):
        """
        Génère une grille de sudoku
        :param cells_frequency: proportion de cases à laisser (= difficulté)
        met à jour self.grid
        """
        
        # Test préconditions
        test_errors(frequency = cell_frequency)
        
        if not self.is_grid_saved and len(self.grid.get_all_empty_cells()) < self.grid.cells_count:  # verifie si la grille contient des données
            do_save = askyesnocancel(
                "Sauvegarde",
                "Voulez vous générer une nouvelle grille sans sauvegarder ?\nLes données non sauvegardées seront perdues"
            )
            
            # Boutton annuler
            if do_save == None:
                return
            
            # Boutton oui
            if do_save:
                self.save_grid()
        
        print("generating...")
        self.game.update_title("Génération ...")
        starting_time = time.time()
        
        # Génère une nouvelle grille vide
        self.new_empty_grid(self.grid.size)
        
        # génère une grille complète et valide aléatoirement
        self.backtracking_solving(False, do_choice_randomly = True)
        
        if self.game.do_quit:
            return
        
        # Pochoir (test plusieurs configurattion jusqu'a en trouver une correct)
        backup_grid = self.grid.get_all_values()  # copie la grille (sauvegarde)
        # définir les cases à laisser
        number_of_cells_to_remove = round((1 - cell_frequency) * self.grid.cells_count)
        resolved = False
        while not resolved:
            cells_to_remove_list = list()  # liste des cellules modifiées
            cell = (0, 0)
            start = True
            for _ in range(number_of_cells_to_remove):
                while self.grid.get_cell_value(cell) == "0" or start:  # start est la conditon pour démarrer le while
                    start = False
                    cell = (random.randint(0, self.grid.size - 1), random.randint(0, self.grid.size - 1))
                
                self.grid.set_cell_value(cell, "0")
                self.game.cell_update(cell, False)
                cells_to_remove_list.append(cell)
            solutions_numbers = self.count_possible_solutions(True)
            if self.game.do_quit:
                return False
            
            if solutions_numbers == 1:
                for cell in self.grid.get_all_coordinates_simple_list():
                    if cell in cells_to_remove_list:
                        self.grid.set_cell_value(cell, "0")
                        self.game.cell_update(cell, False)
                    
                    else:
                        self.grid.set_cell_state(cell, "superlocked")
                        self.game.cell_update(cell, False)
                    resolved = True
            
            else:
                # restaure la grille
                self.grid.set_content(
                    backup_grid, list_states=[['unlocked' for _ in range(self.grid.size)] for _ in range(self.grid.size)]
                )
                self.game.update(False)
                # définir les cases à laisser
                cell_frequency += 0.03  # augmente de 3% le taux de cases laissées (diminue le nombre de boucle nécessaire, accélère la génération)
                number_of_cells_to_remove = round((1 - cell_frequency) * self.grid.cells_count)
        
        self.set_game_mode("playing")
        self.game.update_title()
        self.game.update()
        
        executing_time = round(time.time() - starting_time, 2)
        remaining_cells = self.grid.cells_count - number_of_cells_to_remove
        percentage = round(100 - ((number_of_cells_to_remove / self.grid.cells_count) * 100), 2)
        print(f'Temps de génération: {executing_time}s - {remaining_cells} cases restantes ({percentage}%)')
        
        if do_show_messagebox: showinfo(
            "Génération terminée",
            f"{' ' * 20}Génération effectué avec succès\n"
            f"{' ' * 20}temps d'éxecution: {executing_time}s\n"
            f"{' ' * 20}cases restantes: {remaining_cells} cases ({percentage}%)\n"
            f"{' ' * 100}"
        )
    
    def solve_grid(self, do_display: bool = True):
        """
        Résout le Sudoku, tient compte des valeurs entrées pas l'utilisateur, seulement les cases présentes originalement
        """
        
        # Test préconditions
        test_errors(boolean = do_display)
        
        starting_time = time.time()
        
        if do_display:
            self.game.update_title("Résolution ...")
        
        print('solving...')
        self.game.graphism.display_main_elements()
        
        self.set_game_mode("playing")
        self.clear_inputs(False)
        
        if not self.is_valid():
            print("Invalid input, cannot solve the sudoku")
        
        elif self.backtracking_solving(do_display):
            print("Sudoku solved successfully")
            print(f'Solving executing time: {round(time.time() - starting_time, 2)}s')
        
        else:
            print("Cannot solve the sudoku")
            print(f'Solving executing time: {round(time.time() - starting_time, 2)}s')
         
        self.game.update_title()
        #pygame.display.set_caption(self.game.title)
    
    def solve_generated_grid(self):
        """
        Résout le Sudoku, ne tient pas compte des valeurs entrées pas l'utilisateur, seulement les cases présentes originalement
        """
        
        if not self.is_valid():
            return False
        
        if self.backtracking_solving(False):
            return True
        
        else:
            return False
    
    def clear(self):
        """
        supprime toutes les valeurs des cases autres que les superlocked et les locked
        """
        
        is_grid_changed = False
        
        for x in range(self.grid.size):
            for y in range(self.grid.size):
                
                if self.grid.get_cell_state((x, y)) == "unlocked" and self.grid.get_cell_value((x, y)) != "0":
                    self.grid.set_cell_value((x, y), "0")
                    is_grid_changed = True
        
        if is_grid_changed:
            print("\nThe grid was cleared")
            self.save_grid_in_history()
            self.is_grid_saved = False
    
    def clear_inputs(self, do_save_in_history: bool):
        """
        Supprime toutes les valeurs entrées par l'utilisateur
        """
        
        # Test préconditions
        test_errors(boolean = do_save_in_history)
        
        is_grid_changed = False
        
        for x in range(self.grid.size):
            for y in range(self.grid.size):
                
                if self.game_mode == "editing" or self.grid.get_cell_state((x, y)) != "superlocked":
                    if self.grid.get_cell_state((x, y)) != "unlocked" or self.grid.get_cell_value((x, y)) != "0":
                        self.grid.set_cell_state((x, y), "unlocked")
                        self.grid.set_cell_value((x, y), '0')
                        is_grid_changed = True
        
        if is_grid_changed and do_save_in_history:
            print("\nThe grid was cleared")
            self.save_grid_in_history()
            self.is_grid_saved = False
    
    def put_obvious_solutions(self, do_display: bool = True) -> list[tuple[int, int]]:
        """
        Met dans la grille les chiffres évidentes (les case où il n'y a qu'une valeur possible)
        Renvoi la liste des coordonnées des cases modifiées
        """
        
        modified_cells = list()
        while True:
            is_algorithm_finished = True
            
            cells_to_check = self.grid.get_all_empty_cells()
            
            for cell_coordinates in cells_to_check:
                cell_possible_values = self.grid.get_possible_values(cell_coordinates)
                if len(cell_possible_values) == 1:
                    self.grid.set_cell_value(cell_coordinates, cell_possible_values[0])
                    self.game.cell_update(cell_coordinates, do_display=do_display)
                    modified_cells.append(cell_coordinates)
                    is_algorithm_finished = False
            
            if is_algorithm_finished:
                break
        
        return modified_cells
    
    def count_possible_solutions(self, do_stop_sup_1: bool = False) -> int:
        """
        Fonction récurusive qui compte le nombre de solutions possibles dans le sudoku
        Renvoi -1 si la fenêtre doit être fermée, et le nombre de solutions possibles dans les autres cas
        :param: do_stop_sup_1: indique si le programme doit s'arreter si il dépasse 1 (indique rapidement si il y a plus d'une solution)
        """
        if self.game.do_quit:
            return -1
        
        encountered_solutions = 0
        
        # récupère les valeurs possibles de toutes les cases [liste des valeurs possibles, coordonnées]
        cells_to_fill = [
            [self.grid.get_possible_values((x, y)), (x, y)]
            if self.grid.get_cell_state((x, y)) != 'superlocked' and self.grid.get_cell_value((x, y)) == '0'
            else []
            for y in range(self.grid.size) for x in range(self.grid.size)
        ]
        
        # supprime tous les éléments [] = cases superlocked ou cases avec déjà des valeurs
        cells_to_fill = list(filter(lambda x: x != [], cells_to_fill))
        
        if len(cells_to_fill) == 0:
            return 0
        
        # tri les cases de la liste en fonction du nombre de valeurs possibles
        minimum = min([len(element[0]) for element in cells_to_fill])
        cells_to_fill = list(filter(lambda x: len(x[0]) == minimum, cells_to_fill))
        
        # Récupère les coordonnées et valeurs possibles de la cases ayant le moins de valeurs possibles
        cell_possible_values, cell_coordinates = cells_to_fill[0]
        
        # Pour chaque valeur possible de la case en question
        for value in cell_possible_values:
            # Mettre la valeur dans la case
            self.grid.set_cell_value(cell_coordinates, value)
            self.game.cell_update(cell_coordinates, False)
            
            # Si la grille est complète et valide, ajouter 1 au compteur des solutions rencontrées
            if self.grid.is_full():
                encountered_solutions += 1
                if do_stop_sup_1 and encountered_solutions > 1:
                    return encountered_solutions
            
            else:
                if do_stop_sup_1 and encountered_solutions > 1:
                    return encountered_solutions
                encountered_solutions += self.count_possible_solutions(do_stop_sup_1)
                if self.game.do_quit:
                    # Arrêter le programme
                    return -1
                
                if do_stop_sup_1 and encountered_solutions > 1:
                    return encountered_solutions
            
            self.grid.set_cell_value(cell_coordinates, "0")
            self.game.cell_update(cell_coordinates, False)
        
        return encountered_solutions
    
    def backtracking_solving(self, do_display: bool, do_choice_randomly: bool = False, last_cell_coordinates: tuple[int, int]=None, grid_possibilities: list[list[list,tuple[int, int]]] = None) -> bool:
        """
        Fonction récursive qui résout le Sudoku en testant toutes les possibilités
        Renvoi True si la grille courante est possible à résoudre, et False si elle ne l'est pas
        :param do_choice_randomly: place les valeurs
        """
        
        # Si l'utilisateur ferme la fenêtre
        if self.game.do_quit:
            # Arrêter le programme
            return False
        
        if self.grid.is_full():
            # Si la grille est remplie, renvoyer True si elle est résolue, et False si la résolution n'est pas valide
            return self.is_valid()
        
        # met les valeurs évidentes des cases
        #modified_cells_coordinates = []
        modified_cells_coordinates = self.put_obvious_solutions(do_display)

        #if True:
        if not last_cell_coordinates or self.grid.size <= 9:  # test si il s'agit du premier appel de la méthode OU que la grille fait neuf ou moins, si ce n'es tpas le cas, utilise une méthode de résolution alternative (trop longue en 9x9
            # récupère les valeurs possibles de toutes les cases [liste des valeurs possibles, coordonnées] si c'est la première itération
            cells_to_fill = [
                [self.grid.get_possible_values((x, y)), (x, y)]
                if self.grid.get_cell_state((x, y)) != 'superlocked' and self.grid.get_cell_value((x, y)) == '0'
                else []
                for y in range(self.grid.size) for x in range(self.grid.size)
            ]
            # défini grid_possibilities
            grid_possibilities = cells_to_fill
            #print(grid_possibilities)
            
        else:
            # récupère les valeurs possibles de toutes les cases qui sont sur la même ligne, colonne ou carré que la dernière case modifiée et/ou sur la même ligne, colonne, carrée que la dernière case modifiée (last_cell_coordinates)
            grid_possibilities = grid_possibilities.copy()
            # défini grid_possibilities
            #print("last_cell_coordinates + modified_cells_coordinates",[last_cell_coordinates] + modified_cells_coordinates)
            #i = 0
            #print(modified_cells_coordinates)
            coordinates_list: list[tuple[int, int]] = list()
            for actual_coordinates in [last_cell_coordinates] + modified_cells_coordinates:
                for format in ["columns", "lines", "squares"]:
                    for coordinates in self.grid.get_group_coordinates(actual_coordinates, format):
                        if coordinates not in coordinates_list:
                            #print(i)
                            #i += 1
                            coordinates_list.append(coordinates)
                            possible_values = self.grid.get_possible_values(coordinates)
                            if self.grid.get_cell_state(coordinates) != 'superlocked' and self.grid.get_cell_value(
                                    coordinates) == '0':
                                grid_possibilities[coordinates[1] * self.grid.size + coordinates[0]] = [possible_values, coordinates]
                            else:
                                grid_possibilities[coordinates[1] * self.grid.size + coordinates[0]] = []
                
            cells_to_fill = grid_possibilities

        # supprime tous les éléments [] = cases superlocked ou cases avec déjà des valeurs
        cells_to_fill = list(filter(lambda x: x != [], cells_to_fill))
        
        # Si il n'y a pas de case vide
        if len(cells_to_fill) == 0:
            # Renvoyer la validité du sudoku obtenu
            return self.is_valid()
        
        # tri les cases de la liste en fonction du nombre de valeurs possibles
        minimum = min([len(element[0]) for element in cells_to_fill])
        cells_to_fill = list(filter(lambda x: len(x[0]) == minimum, cells_to_fill))
        
        if do_choice_randomly:  # arrangement des cases aléatoires dans le nombre de solution minimales
            random.shuffle(cells_to_fill)
        
        # Récupère les coordonnées et valeurs possibles de la cases ayant le moins de valeurs possibles
        cell_possible_values, cell_coordinates = cells_to_fill[0]
        
        if do_choice_randomly:  # arrangement des valeurs aléatoires dans les valeurs possibles
            random.shuffle(cell_possible_values)
        
        # Pour toutes les valeurs possibles de la case
        for value in cell_possible_values:
            # Met la valeur de la case à "value"
            self.grid.set_cell_value(cell_coordinates, value)
            grid_possibilities[cell_coordinates[1] * self.grid.size + cell_coordinates[0]] = []

            # affiche la valeur
            self.game.cell_update(cell_coordinates, do_display)
            
            # Si la fonction récursive renvois une réponse positive, alors faire remonter la réponse
            
            if self.backtracking_solving(do_display, last_cell_coordinates=cell_coordinates, grid_possibilities=grid_possibilities):
                return True
            
            # Sinon retirer la valeur mise dans la case
            else:
                if self.game.do_quit:
                    # Arrêter le programme
                    return False
                
                self.grid.set_cell_value(cell_coordinates, '0')
                self.game.cell_update(cell_coordinates, do_display)  # Met à jour l'affichage du contenu de la case
        
        # Enlève toutes les valeurs "évidentes" mises au préalable
        for coordinates in modified_cells_coordinates:
            self.grid.set_cell_value(coordinates, '0')

        # Renvoyer False car cela signifie qu'aucune solution n'a été trouvé
        return False
