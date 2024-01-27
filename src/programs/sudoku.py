import random
import time
import tkinter
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter.messagebox import askyesnocancel
import pygame

from src.programs.grid import Grid
from src.programs.test_errors import test_errors


class Sudoku:
    """
    La classe "Sudoku" permet d'effectuer des actions complexes sur la grille,
    telles que la résoudre, en charger une depuis un fichier, ou encore en générer une nouvelle
    """
    
    def __init__(self, game, grid_size: int):
        test_errors(grid_size)
        
        self.game = game
        self.grid = Grid(self.game.values, grid_size)
        self.selected_cell = (-1, -1)  # Coordonnées de la case sélectionnée, (-1, -1) si aucune case
        self.conflicting_cells: list[tuple[int, int]] = list()
    
    def select_cell(self, coordinates: tuple[int, int]):
        """
        Selectionne la case de coordonnées (x, y)
        """
        
        # Test des préconditions
        test_errors(self.grid.size, coordinates=coordinates)
        
        # Code de la fonction
        self.selected_cell = coordinates
    
    def deselect_cell(self):
        """
        Dessélectionne la case sélectionnée
        """
        
        # Code de la fonction
        self.selected_cell = (-1, -1)
    
    def move_selected_cell(self, direction: str):
        """
        Déplace les coordonnées de la case sélctionnées vers la direction indiquée
        """
        
        # Test des préconditions
        assert type(direction) == str, f"The `direction` argument must be a string (type : {type(direction)})"
        assert direction in ["left", "right", "up",
                             "down"], f'The `direction` argument must be "left", "right", "up" or "down" (value : {direction})'
        
        # Code de la fonction
        # Si aucune case n'est sélectionnée
        if self.selected_cell == (-1, -1):
            # Ne rien faire
            return
        
        match direction:
            
            case "left":
                # Si l'utilisateur demande de déplacer la sélection vers la gauche, mais qu'elle est déjà au maximum de cette direction
                if self.selected_cell[0] == 0:
                    # Alors ne rien faire
                    return
                
                # Sinon déplacer la sélection d'un cran vers la gauche
                self.selected_cell = (self.selected_cell[0] - 1, self.selected_cell[1])
            
            case "right":
                # Si l'utilisateur demande de déplacer la sélection vers la droite, mais qu'elle est déjà au maximum de cette direction
                if self.selected_cell[0] == self.grid.size - 1:
                    # Alors ne rien faire
                    return
                
                # Sinon déplacer la sélection d'un cran vers la droite
                self.selected_cell = (self.selected_cell[0] + 1, self.selected_cell[1])
            
            case "up":
                # Si l'utilisateur demande de déplacer la sélection vers le haut, mais qu'elle est déjà au maximum de cette direction
                if self.selected_cell[1] == 0:
                    # Alors ne rien faire
                    return
                
                # Sinon déplacer la sélection d'un cran vers le haut
                self.selected_cell = (self.selected_cell[0], self.selected_cell[1] - 1)
            
            case "down":
                # Si l'utilisateur demande de déplacer la sélection vers le bas, mais qu'elle est déjà au maximum de cette direction
                if self.selected_cell[1] == self.grid.size - 1:
                    # Alors ne rien faire
                    return
                
                # Sinon déplacer la sélection d'un cran vers le bas
                self.selected_cell = (self.selected_cell[0], self.selected_cell[1] + 1)
        
        # Test des postconditions
        test_errors(self.grid.size, coordinates=self.selected_cell)
    
    def set_selected_cell_value(self, value: str):
        """
        Met la valeur de la case sélectionnée à `value`
        """
        
        # Test des préconditions
        assert self.selected_cell != (-1, -1), "You must select a cell in order to set its value"
        test_errors(self.grid.size, coordinates=self.selected_cell, value=value)
        
        # Code de la fonction
        self.grid.set_cell_value(self.selected_cell, value)
    
    def set_selected_cell_color(self, color: tuple[int, int, int]):
        """
        Met la couleur de la case sélectionnée à `color`
        """
        
        # Test des préconditions
        test_errors(color=color)
        
        # Code de la fonction
        self.grid.set_cell_color(self.selected_cell, color)
    
    def update_grid(self, list_values: list[list[str]] = None, list_states: list[list[str]] = None):
        """
        Modifie la taille de la grille
        :param list_values: optionnel: valeurs des cellules de la grille
        :param list_states: optionnel: états des cellules de la grille
        """
        
        if list_values:
            grid_size = len(list_values)
        else:
            grid_size = self.grid.size
            list_values = [['0' for _ in range(grid_size)] for _ in range(grid_size)]
        
        test_errors(grid_size)
        
        if not list_states:
            list_states = [['unlocked' for _ in range(grid_size)] for _ in range(grid_size)]
        
        test_errors(grid_size, list_values=list_values, list_states=list_states, possibles_values=self.game.values)
        self.grid.update_attributes(grid_size, list_values, list_states)
        self.game.graphism.update_grid_attributes(grid_size)  # mise à jour affichage
        
        self.game.title = f"{self.game.name} {grid_size}x{grid_size}"
        #pygame.display.set_caption(self.game.title)  # Nom de la fenêtre
        self.game.set_title()
        self.game.update_config_file(key="grid_size", value=grid_size)
    
    def open_grid(self):
        """
        Charge une grille à partir d'un fichier
        """
        
        # Ouvre une fenêtre de dialogue permettant à l'utilisateur de choisir le fichier à charger
        file_path = askopenfilename(
            initialdir="src/save_folder",
            initialfile="model_2.sdk",
            title=f"Ouvrir un {self.game.name} sous...",
            filetypes=[("Sudoku file", "*.sdk")]
        )
        
        # Dans le cas où l'utilisateur n'a pas sélectionné de fichier
        if not file_path:
            # Affiche un message en console et ne fait rien d'autre
            print("No file selected for opening, Empty grid...")
            return
        
        # Récupère le contenu du fichier sélectionné
        with open(file_path, "rt") as file:
            file_content = file.read()
        
        # Sépare les valeurs et les états des cases dans deux sous-listes
        file_content = file_content.split("\n\n")
        # Formate la liste des valeurs au format list[list[int]]
        list_values = [
            [line[i] for line in file_content[0].split("\n")]
            for i in range(len(file_content[0].split("\n")[0]))
        ]
        # Formate la liste des états au format list[list[str]]
        convert_state = {"0": "unlocked", "1": "locked", "2": "superlocked"}
        list_states = [
            [convert_state.get(line[i], "unlocked") for line in file_content[1].split("\n")]
            for i in range(len(file_content[1].split("\n")[0]))
        ]
        
        if len(list_values) != self.grid.size:
            response = askyesnocancel("Changement taille Sudoku",
                                      f"Voulez-vous changer la taille du sudoku\nLes données non sauvegardées seront perdues")
            if not response:
                return None  # signifie que l'utilisateur souhaite garder la taille actuelle de son sudoku
            else:
                self.update_grid(list_values, list_states)
        
        # Test postconditions
        test_errors(self.grid.size, list_values=list_values, list_states=list_states, possibles_values=self.game.values)
        
        # Remplace le contenu de la grille par le contenu lu dans le fichier
        self.grid.set_content(list_values, list_states)
        self.verify_grid()
        print("fin open")
    
    def save_grid(self):
        """
        /!\ Enregistre la grille actuelle dans un fichier Avec ou sans les valeurs saisies par utilisateur
        """
        
        # Récupère le chemin du fichier à sauvegarder
        filepath = asksaveasfilename(
            initialdir="src/save_folder/",
            initialfile='saved_sudoku.sdk',
            title=f"Enregistrer un {self.game.name} sous...",
            filetypes=[("Sudoku file", "*.sdk")]
        )
        
        # Si l'utilisateur n'a rien entré
        if not filepath:
            # Afficher un message dans la console et ne rien faire d'autre
            print('No file selected for saving')
            return False
        
        # convertit toutes les valeurs des cases en string
        double_list_values = [
            [str(line[i].value) for line in self.grid.content]
            for i in range(len(self.grid.content))
        ]
        # convertit la double liste en liste simple (une string par linee)
        list_values = ["".join(line) for line in double_list_values]
        
        # convertit la liste en une string
        str_content = "\n".join(list_values)
        
        convert_state = {"unlocked": "0", "locked": "1", "superlocked": "2"}  # Dictionnaire de conversion
        
        # convertit toutes les valeurs des celules en string avec le dictionnaire de conversion
        double_list_state = [
            [convert_state[line[i].state] for line in self.grid.content]
            for i in range(len(self.grid.content))
        ]
        # convertit la double liste en liste simple (une string par ligne)
        list_state = ["".join(line) for line in double_list_state]
        
        # additionne les deux (valeurs, états)
        str_content += "\n\n" + "\n".join(list_state)  # "\n\n" pour séparer les valeurs et les états des cases
        
        # écrit le contenu obtenu dans un fichier
        with open(filepath, "w") as file:
            file.write(str_content)
    
    def lock_selected_cell(self):
        """
        Verrouille la case sélectionnée, la valeur de la case ne pourra plus être modifiée
        """
        
        # Test de préconditions
        assert self.selected_cell != (-1, -1), "You must select a cell in order to lock it"
        test_errors(self.grid.size, coordinates=self.selected_cell)

        print(f"Cell {self.selected_cell} is locked")
        # Code de la fonction
        # Si la case sélectionnée est "superlocked"
        if self.grid.get_cell_state(self.selected_cell) == "superlocked":
            # Ne rien faire
            return
        
        # Sinon, mettre l'état de la case sélectionnée à "locked"
        self.grid.set_cell_state(self.selected_cell, "locked")
    
    def unlock_selected_cell(self):
        """
        Déverrouille la case sélectionnée, la valeur de la case pourra de nouveau être modifiée
        """
        
        # Test de préconditions
        assert self.selected_cell != (-1, -1), "You must select a cell in order to unlock it"
        test_errors(self.grid.size, coordinates=self.selected_cell)
        
        print(f"cell {self.selected_cell} is unlocked")

        # Code de la fonction
        # Si la case sélectionnée est "superlocked"
        if self.grid.get_cell_state(self.selected_cell) == "superlocked":
            # Ne rien faire
            return
        
        # Sinon, mettre l'état de la case sélectionnée à "unlocked"
        self.grid.set_cell_state(self.selected_cell, "unlocked")
    
    def is_valid(self) -> bool:
        """
        Renvoi True si la grille ne comporte aucune erreurs, et False si elle en comporte au moins une
        """
        
        # Pour tout les formats de grille possibles (lignes, colonnes et carrés)
        for grid_format in [self.grid.get_all_values_as(format) for format in ["lines", "columns", "squares"]]:
            for x in range(self.grid.size):
                # for n in range(1, 1 + self.grid.size):
                for n in self.game.values[:self.grid.size]:
                    # Si l'un des sous-groupes de ce format compte plusieur fois le même chiffre
                    if grid_format[x].count(n) > 1:
                        # Renvoyer False
                        return False
        
        # Si aucun doublon n'a été trouvé, renvoyer True
        return True
    
    def verify_grid(self):
        """
        Vérifie dans toute la grille si des cases sont en conflit
        """
        
        tmp_conflicting_cells = list()  # Liste temporaire dans laquelle seront stockées les coordonnées des cases en conflits
        
        # Pour tous les formats possibles
        for format in ["lines", "columns", "squares"]:
            all_values = self.grid.get_all_values_as(format)
            all_coordinates = self.grid.get_all_coordinates_as(format)
            
            for x in range(self.grid.size):
                group_values = all_values[x]
                groupe_coordinates = all_coordinates[x]
                
                for n in self.game.values[:self.grid.size]:
                    if group_values.count(n) > 1 and n != 0:
                        
                        for y in range(self.grid.size):
                            if group_values[y] == n and not groupe_coordinates[y] in tmp_conflicting_cells:
                                tmp_conflicting_cells.append(groupe_coordinates[y])
                    
                    else:
                        for y in range(self.grid.size):
                            if group_values[y] == n and groupe_coordinates[y] in self.conflicting_cells:
                                self.conflicting_cells.remove(groupe_coordinates[y])
        
        for x in range(self.grid.size):
            for y in range(self.grid.size):
                
                if (x, y) in tmp_conflicting_cells and not (x, y) in self.conflicting_cells:
                    self.conflicting_cells.append((x, y))
        
        self.update_cells_conflicting_state()
    
    def update_cells_conflicting_state(self):
        for x in range(self.grid.size):
            for y in range(self.grid.size):
                self.grid.set_cell_conflicting_state((x, y), (x, y) in self.conflicting_cells)
    
    def generate_grid(self, prop_cells_to_let, do_display: bool, do_show_messagebox: bool = True):
        """
        Génère une grille de sudoku résolu
        :param prop_cells_to_let: proportion de cases à laisser (= difficulté)
        :param do_display: mettre à jour graphiquement les cases lors de la génération
        met à jour self.grid
        """
        
        assert type(
            prop_cells_to_let) == float, f'The "prop_cells_to_let" argument must be a float between 0 and 1 (type: {type(prop_cells_to_let)})'
        assert 0 <= prop_cells_to_let <= 1, f'The "prop_cells_to_let" argument must be a float between 0 and 1 (value: {prop_cells_to_let})'
        assert type(do_display) == bool, f'The "do_display" argument must be a boolean (type : {type(do_display)})'
        
        if len(self.grid.get_all_empty_cells()) != self.grid.cells_count:  # verifie si la grille contient des données
            is_to_discard = askyesnocancel("Sauvegarde grille ?",
                                           "Voulez vous continuer SANS sauvegarder la grille avant la génération ?\nLes données non sauvegardées seront perdues")
            if is_to_discard is False:  # bouton oui
                self.save_grid()
            elif is_to_discard is None:  # bouton cancel
                return False  # annulation opération
        
        print("generating...")
        starting_time = time.time()
        self.update_grid()  # vide la grille, déverrouille toutes les cases (attention, modifie le titre de la fenetre)
        #pygame.display.set_caption(self.game.title + " (génération...)")
        self.game.set_title("(génération...)")
        # génère une grille valide aléatoirement
        if not self.backtracking_solving(do_display, do_choice_randomly=True):  # signifie fermeture de la fenetre
            print('closing')
            return False
        
        # Pochoir (test plusieurs configurattion jusqu'a en trouver une correct)
        backup_grid = self.grid.get_all_values()  # copie la grille (sauvegarde)
        # définir les cases à laisser
        number_of_cells_to_remove = round((1 - prop_cells_to_let) * self.grid.cells_count)
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
                self.game.cell_update(cell, do_display)
                cells_to_remove_list.append(cell)
            solutions_numbers = self.count_possible_solutions(do_display=do_display, do_stop_sup_1=True)
            if self.game.do_quit:
                return False
            
            if solutions_numbers == 1:
                for cell in self.grid.get_all_coordinates_simple_list():
                    if cell in cells_to_remove_list:
                        self.grid.set_cell_value(cell, "0")
                        self.game.cell_update(cell, do_display)
                    
                    else:
                        self.grid.set_cell_state(cell, "superlocked")
                        self.game.cell_update(cell, do_display)
                    resolved = True
            
            else:
                # print(f"grille contient plus d'une solution ({solutions_numbers} solutions), génération d'un nouveauu pochoir")
                # restaure la grille
                self.grid.set_content(backup_grid, list_states=[['unlocked' for _ in range(self.grid.size)] for _ in
                                                                range(self.grid.size)])
                self.game.update(do_display)
                # définir les cases à laisser
                prop_cells_to_let += 0.03  # augmente de 3% le taux de cases laissées (diminue le nombre de boucle nécessaire, accélère la génération)
                number_of_cells_to_remove = round((1 - prop_cells_to_let) * self.grid.cells_count)
        
        self.game.update()
        executing_time = round(time.time() - starting_time, 2)
        remaining_cells = self.grid.cells_count - number_of_cells_to_remove
        percentage = round(100 - ((number_of_cells_to_remove / self.grid.cells_count) * 100), 2)
        print(f'generating executing time: {executing_time}s - {remaining_cells} cases restantes ({percentage}%)')
        if do_show_messagebox: tkinter.messagebox.showinfo("Génération terminée",
                                                           f"{' ' * 20}Génération effectué avec succès\n"
                                                           f"{' ' * 20}temps d'éxecution: {executing_time}s\n"
                                                           f"{' ' * 20}cases restantes: {remaining_cells} cases ({percentage}%)\n"
                                                           f"{' ' * 100}")
        #pygame.display.set_caption(self.game.title)
        self.game.set_title()
    
    def solve_grid(self, do_display: bool = True):
        """
        Résout le Sudoku, tient compte des valeurs entrées pas l'utilisateur, seulement les cases présentes originalement
        """
        
        assert type(do_display) == bool, f'The "do_display" argument must be a boolean (type : {type(do_display)})'
        
        starting_time = time.time()
        #pygame.display.set_caption(self.game.title + " (résolution...)")
        self.game.set_title("(résolution...)")
        print('solving...')
        # self.put_obvious_solutions()
        self.game.graphism.display_elements()
        
        self.clear_inputs()
        
        if not self.is_valid():
            print("Invalid input, cannot solve the sudoku")
        
        elif self.backtracking_solving(do_display):
            print("Sudoku solved successfully")
            print(f'solving executing time: {round(time.time() - starting_time, 2)}s')
        
        
        else:
            print("Cannot solve the sudoku")
            print(f'solving executing time: {round(time.time() - starting_time, 2)}s')
         
        self.game.set_title()
        #pygame.display.set_caption(self.game.title)
    
    def solve_generated_grid(self):
        """
        Résout le Sudoku, tient compte ou non des valeurs entrées pas l'utilisateur, seulement les cases présentes originalement
        """
        
        if not self.is_valid():
            return False
        
        if self.backtracking_solving(False):
            return True
        
        else:
            return False
    
    def clear_inputs(self):
        """
        Supprime toutes les valeurs entrées par l'utilisateur
        """
        
        for x in range(self.grid.size):
            for y in range(self.grid.size):
                
                if self.grid.get_cell_state((x, y)) != "superlocked":
                    self.grid.set_cell_state((x, y), "unlocked")
                    self.grid.set_cell_value((x, y), '0')
    
    def clear(self):
        """
        supprime toutes les valeurs des cases autres que les superlocked et les locked
        """
        for x in range(self.grid.size):
            for y in range(self.grid.size):
                
                if self.grid.get_cell_state((x, y)) == "unlocked":
                    self.grid.set_cell_value((x, y), '0')
    
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
    
    def count_possible_solutions(self, do_display: bool = False, do_stop_sup_1: bool = False) -> int:
        """
        Fonction récurusive qui compte le nombre de solutions possibles dans le sudoku
        Renvoi -1 si la fenêtre doit être fermée, et le nombre de solutions possibles dans les autres cas
        :param: do_stop_sup_1: indique si le programme doit s'arreter si il dépasse 1 (indique rapidement si il y a plus d'une solutionn)
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
            self.game.cell_update(cell_coordinates, do_display)
            
            # Si la grille est complète et valide, ajouter 1 au compteur des solutions rencontrées
            if self.grid.is_full():
                encountered_solutions += 1
                if do_stop_sup_1 and encountered_solutions > 1:
                    return encountered_solutions
            
            else:
                if do_stop_sup_1 and encountered_solutions > 1:
                    return encountered_solutions
                encountered_solutions += self.count_possible_solutions(do_display=do_display,
                                                                       do_stop_sup_1=do_stop_sup_1)
                if self.game.do_quit:
                    # Arrêter le programme
                    return -1
                
                if do_stop_sup_1 and encountered_solutions > 1:
                    return encountered_solutions
            
            self.grid.set_cell_value(cell_coordinates, "0")
            self.game.cell_update(cell_coordinates, do_display)
        
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
            """cells_to_fill = [
                [self.grid.get_possible_values(coordinates), coordinates]
                if self.grid.get_cell_state(coordinates) != 'superlocked' and self.grid.get_cell_value(coordinates) == '0'
                else []
                for cell in modified_cells_coordinates + [last_cell_coordinates]
                for format in ["lines", "columns", "squares"]
                for coordinates in self.grid.get_group_coordinates(cell, format)
            ]"""
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
                            possibles_values = self.grid.get_possible_values(coordinates)
                            if self.grid.get_cell_state(coordinates) != 'superlocked' and self.grid.get_cell_value(
                                    coordinates) == '0':
                                grid_possibilities[coordinates[1] * self.grid.size + coordinates[0]] = [possibles_values, coordinates]
                            else:
                                grid_possibilities[coordinates[1] * self.grid.size + coordinates[0]] = []
                
            cells_to_fill = grid_possibilities

            
            """for coordinates in self.grid.get_all_coordinates_as(format):
                possibles_values = self.grid.get_possible_values(coordinates)
                if self.grid.get_cell_state(coordinates) != 'superlocked' and self.grid.get_cell_value(coordinates) == '0':
                    grid_possibilities[coordinates[1] * self.grid.size + coordinates[0]] = [possibles_values, coordinates]
                else:
                    grid_possibilities[coordinates[1] * self.grid.size + coordinates[0]] = []
            """
                
            
            """ for cell in [last_cell_coordinates] + modified_cells_coordinates:
                for format in ["lines", "columns", "squares"]:
                    for coordinates in self.grid.get_group_coordinates(cell, format):
                        print(i)
                        i+=1
                        possibles_values = self.grid.get_possible_values(coordinates)
                        if self.grid.get_cell_state(coordinates) != 'superlocked' and self.grid.get_cell_value(coordinates) == '0':
                            grid_possibilities[coordinates[1] * self.grid.size + coordinates[0]] = [possibles_values, coordinates]
                        else:
                            grid_possibilities[coordinates[1] * self.grid.size + coordinates[0]] = []"""

            

        
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
