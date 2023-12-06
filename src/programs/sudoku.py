import time
from tkinter.filedialog import askopenfilename, asksaveasfilename
import pygame

from src.programs.grid import Grid
from src.programs.test_errors import test_errors


class Sudoku:
    
    def __init__(self, game):
        self.game = game
        self.grid = Grid()
        self.selected_cell = (-1, -1)  # Coordonnées de la case sélectionnée, (-1, -1) si aucune case
        self.conflicting_cells: list[tuple[int, int]] = list()
        self.do_display_conflicts = True
    
    def reverse_display_conflicts(self):
        """
        Cette fonction inverse l'état de la variable booléenne `self.do_display_conflicts`
        """
        
        self.do_display_conflicts = not self.do_display_conflicts
        self.verify_selected_cell()
    
    def select_cell(self, coordinates: tuple[int, int]):
        """
        Selectionne la case de coordonnées (x, y)
        """
        
        # Test des préconditions
        test_errors(coordinates=coordinates)
        
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
                if self.selected_cell[0] == 8:
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
                if self.selected_cell[1] == 8:
                    # Alors ne rien faire
                    return
                
                # Sinon déplacer la sélection d'un cran vers le bas
                self.selected_cell = (self.selected_cell[0], self.selected_cell[1] + 1)
        
        # Test des postconditions
        test_errors(coordinates=self.selected_cell)
    
    def set_selected_cell_value(self, value: int):
        """
        Met la valeur de la case sélectionnée à `value`
        """
        
        # Test des préconditions
        assert self.selected_cell != (-1, -1), "You must select a cell in order to set its value"
        test_errors(coordinates=self.selected_cell, value=value)
        
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
    
    def load_grid(self):
        """
        Charge une grille à partir d'un fichier
        """
        
        # Ouvre une fenêtre de dialogue permettant à l'utilisateur de choisir le fichier à charger
        file_path = askopenfilename(
            initialdir="src/save_folder",
            initialfile="model_2.sdk",
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
            [int(line[i]) for i in range(len(file_content[0].split("\n")[0]))]
            for line in file_content[0].split("\n")
        ]
        
        # Formate la liste des états au format list[list[str]]
        convert_state = {"0": "unlocked", "1": "locked", "2": "superlocked"}
        list_states = [
            [convert_state.get(line[i], "0") for i in range(len(file_content[1].split("\n")[0]))]
            for line in file_content[1].split("\n")
        ]
        
        # Test postconditions
        test_errors(list_values=list_values, list_states=list_states)
        
        # Remplace le contenu de la grille par le contenu lu dans le fichier
        self.grid.set_content(list_values, list_states)
    
    def save_grid(self):
        """
        /!\ Enregistre la grille actuelle dans un fichier Avec ou sans les valeurs saisies par utilisateur ?
        """
        
        # Récupère le chemin du fichier à sauvegarder
        filepath = asksaveasfilename(
            initialdir="src/save_folder/",
            initialfile='saved_sudoku.sdk',
            filetypes=[("Sudoku file", "*.sdk")]
        )
        
        # Si l'utilisateur n'a rien entré
        if not filepath:
            # Afficher un message dans la console et ne rien faire d'autre
            print('No file selected for saving')
            return False
        
        # convertit toutes les valeurs des cellules en string
        double_list_values = [[str(cell.value) for cell in line] for line in self.grid.content]
        
        # convertit la double liste en liste simple (une string par linee)
        list_values = ["".join(line) for line in double_list_values]

        # convertit la liste en une string
        str_content = "\n".join(list_values)
        
        convert_state = {"unlocked": "0", "locked": "1", "superlocked": "2"}  # Dictionnaire de conversion
        
        # convertit toutes les valeurs des celules en string avec le dictionnaire de conversion
        double_list_state = [[convert_state[cell.state] for cell in line] for line in self.grid.content]
        
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
        test_errors(coordinates=self.selected_cell)
        
        # Code de la fonction
        # Si la case sélectionnée est "superlocked"
        if self.grid.get_cell_state(self.selected_cell) == "superlocked":
            # Ne rien faire
            return
        
        # Sinon, mettre l'état de la case sélectionnée à "unlocked"
        self.grid.set_cell_state(self.selected_cell, "unlocked")
    
    def clear(self):
        """
        Enlève toutes les cases qui ne sont pas superlocked
        """
        
        for x in range(9):
            for y in range(9):
                if self.grid.get_cell_state((x, y)) == "unlocked":
                    self.grid.set_cell_value((x, y), 0)
    
    def is_valid(self) -> bool:
        """
        Renvoi True si la grille ne comporte aucune erreurs, et False si elle en comporte au moins une
        """
        
        # Pour tout les formats de grille possibles (lignes, colonnes et carrés)
        for grid_format in [self.grid.get_content_as(format) for format in ["lines", "columns", "squares"]]:
            for x in range(9):
                for n in range(1, 10):
                    
                    # Si l'un des sous-groupes de ce format compte plusieur fois le même chiffre
                    if grid_format[x].count(n) > 1:
                        # Renvoyer False
                        return False
        
        # Si aucun doublon n'a été trouvé, renvoyer True
        return True
    
    def verify_selected_cell(self):
        """
        Cette fonction est appelée à chaque fois que l'utilisateur met à jour la valeur d'une case (retourn False si aucyne selection n'existe)
        Si la nouvelle valeur de cette case est entre 1 et 9, la fonction vérifie si elle n'entre pas en conflit avec d'autres valeurs
        Si la nouvelle valeur de cette case est 0, la fonction vérifie si cela annule de précédents conflits
        """
        if self.selected_cell == (-1, -1):
            return False  # pas de case séléctionnée
        tmp_conflicting_cells = list()  # Liste temporaire dans laquelle seront stockées les coordonnées des cases en conflits
        
        # Pour tous les formats possibles
        for format in ["lines", "columns", "squares"]:
            # Récupère les valeurs et les coordonnées du groupe correspondant à ce format
            group_coordinates = self.grid.get_coordinates_group(self.selected_cell, format)
            group_values = self.grid.get_cell_group(self.selected_cell, format)
            
            # Enlève toutes les cases vide de la liste des cases en conflit
            for cell_coordinates in group_coordinates:
                if self.grid.get_cell_value(cell_coordinates) == 0 and cell_coordinates in self.conflicting_cells:
                    self.conflicting_cells.remove(cell_coordinates)
            
            # Pour toutes les valeurs n possibles
            for n in range(1, 10):
                
                # Si la valeur est en conflit avec d'autres dans le groupe courant
                if group_values.count(n) > 1:
                    # Pour toutes les cases du groupe courant
                    for cell_coordinates in group_coordinates:
                        # Si la case a pour valeur n
                        if self.grid.get_cell_value(cell_coordinates) == n:
                            # Ajouter la case à la liste temporaire des cases en conflit
                            tmp_conflicting_cells.append(cell_coordinates)
                
                # Si au contraire la valeur n'est pas en conflit avec d'autres dans le groupe courant
                else:
                    # Pour toutes les cases du groupe courant
                    for cell_coordinates in group_coordinates:
                        # Si la case a pour valeur n mais qu'elle est dans la liste des cases en conflit
                        if self.grid.get_cell_value(
                                cell_coordinates) == n and cell_coordinates in self.conflicting_cells:
                            # Retirer la case de la liste des cases en conflit
                            self.conflicting_cells.remove(cell_coordinates)
        
        # Pour toutes les cases qui sont en conflits
        for cell_coordinates in tmp_conflicting_cells:
            # Si la case n'est pas dans la liste des cases en conflits
            if not cell_coordinates in self.conflicting_cells:
                self.conflicting_cells.append(cell_coordinates)
        
        # Affichage des couleurs sur le texte
        for x in range(9):
            for y in range(9):
                if self.do_display_conflicts and (x, y) in self.conflicting_cells:
                    self.grid.set_cell_color((x, y), (255, 0, 0))
                
                else:
                    self.grid.set_cell_color((x, y), (0, 0, 0))
    
    def generate_grid(self):
        """
        Génère une grille de sudoku à résoudre
        :return: grid
        """
    
    def solve_grid(self):
        """
        Résout le Sudoku, ne tient pas compte des valeurs entrée pas l'utilisateur, seulement les cases présentes originalement
        :return:
        """
        starting_time = time.time()
        print('solving...')
        self.clear_inputs()
        # self.put_obvious_solutions()
        if self.backtracking_solving():
            print("Sudoku solved successfully")
            print("executing time:", time.time() - starting_time)
        
        else:
            print("Cannot solve the sudoku")
    
    def clear_inputs(self):
        """
        Supprime toutes les valeurs entrées par l'utilisateur
        Fonction appelée uniquement par sole_grid()
        """
        
        for x in range(9):
            for y in range(9):
                
                if self.grid.get_cell_state((x, y)) != "superlocked":
                    self.grid.set_cell_state((x, y), "unlocked")
                    self.grid.set_cell_value((x, y), 0)
    
    def put_obvious_solutions(self):
        """
        Met dans la grille les chiffres évidents (les case où il n'y a qu'un chiffre possible)
        """
        
        while True:
            is_algorithm_finished = True
            
            cells_to_check = self.grid.get_all_empty_cells()
            
            for cell_coordinates in cells_to_check:
                cell_possible_values = self.grid.get_possible_values(cell_coordinates)
                if len(cell_possible_values) == 1:
                    self.grid.set_cell_value(cell_coordinates, cell_possible_values[0])
                    self.grid.set_cell_color(cell_coordinates, (0, 255, 0))
                    self.game.cell_update(cell_coordinates)
                    is_algorithm_finished = False
            
            if is_algorithm_finished:
                break
    
    def backtracking_solving(self) -> bool:
        """
        Fonction récursive qui résout le Sudoku en testant toutes les possibilités
        Renvoi True si la grille courante est possible à résoudre, et False si elle ne l'est pas
        """
        
        # Si l'utilisateur ferme la fenêtre
        if self.game.do_quit:
            # Arrêter le programme
            return False
        
        if self.grid.is_full():
            # Si la grille est remplie, renvoyer True si elle est résolue, et False si la résolution n'est pas valide
            return self.is_valid()
        
        # récupère les valeurs possibles de toutes les cases (en premier une liste des valeurs possibles
        possible_values = [[self.grid.get_possible_values((x, y)), (x, y)] if self.grid.content[x][y].get_state() != 'superlock' and self.grid.content[x][y].get_value() == 0 else [-1] for y in range(9) for x in range(9)]

        # supprime tous les éléments [-1] = cellules superlocked ou cases avec déjà des valeurs
        possible_values = list(filter(lambda x: x != [-1], possible_values))
        # tri les éléments de la liste en fonction de la longueur de la liste des valeurs possibles (tri du moins de possibilités au plus de possibilités)
        possible_values.sort(key=lambda v: len(v[0]))
        # récupère la première valeur = nombre minimale de solution
        values, cell_coordinates = possible_values[0]
        #balaye dans les solutions
        for value in values:
            # defini la valeur de la cellule
            self.grid.set_cell_value(cell_coordinates, value)
            # affiche la valeur
            self.game.cell_update(cell_coordinates, pygame.event.get())
            if self.backtracking_solving():  # méthode récursive pour trouver les bonnes valeurs
                return True
            
            else:
                # defini la valeur de la cellule
                self.grid.set_cell_value(cell_coordinates, 0)
                # affiche la valeur
                self.game.cell_update(cell_coordinates, pygame.event.get())

        
        # Si aucune des valeurs possibles de la case ne marche, renvoyer False
        return False