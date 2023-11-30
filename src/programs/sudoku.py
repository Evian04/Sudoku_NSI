import os.path

import pygame
from tkinter.filedialog import askopenfilename, asksaveasfilename

from src.programs.grid import Grid
from src.programs.test_errors import test_errors


class Sudoku:
    
    def __init__(self, game):
        self.game = game
        self.grid = Grid()
        self.selected_cell = (-1, -1)  # Coordonnées de la case sélectionnée, (-1, -1) si aucune case
        
    def select_cell(self, coordinates: tuple[int, int]):
        """
        Selectionne la case de coordonnées (x, y)
        """
        
        test_errors(coordinates = coordinates)
        
        self.selected_cell = coordinates
    
    def deselect_cell(self):
        return tuple(self.selected_cell)
    
    def move_selected_cell(self, direction: str):
        """
        Déplace les coordonnées de la case sélctionnées vers la direction indiquée
        """
        
        if type(direction) != str:
            raise ValueError(f"The `direction` argument must be a string (type : {type(direction)})")
        
        match direction:
            
            case "left":
                if self.selected_cell[0] == 0:
                    return
                
                self.selected_cell = (self.selected_cell[0] - 1, self.selected_cell[1])
            
            case "right":
                if self.selected_cell[0] == 8:
                    return
            
                self.selected_cell = (self.selected_cell[0] + 1, self.selected_cell[1])
            
            case "up":
                if self.selected_cell[1] == 0:
                    return
                
                self.selected_cell = (self.selected_cell[0], self.selected_cell[1] - 1)
            
            case "down":
                if self.selected_cell[1] == 8:
                    return
                
                self.selected_cell = (self.selected_cell[0], self.selected_cell[1] + 1)
                
            case other:
                raise ValueError(f'The `direction` argument must be "left", "right", "up" or "down" (value : {direction})')

    
    def set_selected_cell_value(self, value: int):
        """
        Met la valeur de la case sélectionnée à `value`
        """
        
        test_errors(value = value)
        
        if self.selected_cell == (-1, -1):
            raise ValueError("You must select a cell in order to set its value")
        
        self.grid.set_cell_value(self.selected_cell, value)
        
    def set_selected_cell_color(self, color: tuple[int, int, int]):
        """
        Met la couleur de la case sélectionnée à `color`
        """
        
        test_errors(color = color)
        
        self.grid.set_cell_color(self.selected_cell, color)
    
    def load_grid(self):
        """
        Charge une grille à partir d'un fichier
        """
        
        # Ouvre une fenêtre de dialogue permettant à l'utilisateur de choisir le fichier à charger
        file_path = askopenfilename(
            initialdir="src/save_folder",
            initialfile="model.sdk",
            filetypes=[("Sudoku file", "*.sdk")]
        )
        if not file_path:
            print("No file selected for opening, Empty grid...")
            return
        
        with open(file_path, "rt") as file:
            file_content = file.read()
        
        file_content = file_content.split("\n\n")
        
        cell_values = [[int(value) for value in line] for line in file_content[0].split("\n")]
        
        convert_state = {"0": "unlocked", "1": "locked", "2": "superlocked"}
        cell_states = [[convert_state.get(state, 0) for state in line] for line in file_content[1].split("\n")]
        # /!\ ce choix là ? ^^^
        
        """cell_states = [['superlocked' if int(value) > 0 else 'unlocked'
                        # double boucle imbriquée qui attribue l'état 'unlocked' si la valeur est > à 0 (0 = case vide)
                        for value in line] for line in file_content[0].split("\n")]
        """
        self.grid.set_content(cell_values, cell_states)
    
    def save_grid(self):
        """
        /!\ Enregistre la grille actuelle dans un fichier Avec ou sans les valeurs saisies par utilisateur ?
        """
        filepath = asksaveasfilename(initialdir="src/save_folder/", initialfile='saved_sudoku.sdk',
                                     filetypes=[("Sudoku file", "*.sdk")])
        if not filepath:
            print('No file selected for saving')
            return False
        
        # VALEURS CELLULES:
        # convertit toutes les valeurs des cellules en string
        double_list_values = [[str(cell.value) for cell in line]
                               for line in self.grid.content]
        # convertit la double liste en liste simple (une string par linee)
        list_values = ["".join(line) for line in double_list_values]
        #convertit la liste en une string
        str_content = "\n".join(list_values)

        # ETATS CELLULES:
        convert_state = {"unlocked": "0", "locked": "1", "superlocked": "2"}
        
        # convertit toutes les valeurs des celules en string avec le dictionnaire de conversion
        double_list_state = [[convert_state[cell.state] for cell in line]
                               for line in self.grid.content]
        # convertit la double liste en liste simple (une string par ligne)
        list_state = ["".join(line) for line in double_list_state]
        
        # additionne les deux (valuers, états)
        str_content += "\n\n" + "\n".join(list_state)  # "\n\n" pour séparer les valeurs grille de leur correspondance avec les êtats des cases
        with open(filepath,"w") as file:
            file.write(str_content)
    
    def lock_selected_cell(self):
        """
        Verrouille la case sélectionnée, la valeur de la case ne pourra plus être modifiée
        """
        
        if self.selected_cell == (-1, -1):
            raise ValueError("You must select a cell in order to lock it")
        
        if self.grid.get_cell_state(self.selected_cell) == "superlocked":
            return
        
        self.grid.set_cell_state(self.selected_cell, "locked")
    
    def unlock_selected_cell(self):
        """
        Déverrouille la case sélectionnée, la valeur de la case pourra de nouveau être modifiée
        """
        
        if self.selected_cell == (-1, -1):
            raise ValueError("You must select a cell in order to unlock it")
        
        if self.grid.get_cell_state(self.selected_cell) == "superlocked":
            return
        
        self.grid.set_cell_state(self.selected_cell, "unlocked")
    
    def is_valid(self) -> bool:
        """
        Renvois True si la grille ne comporte aucune erreurs, et False si elle en comporte au moins une
        """
        
        for grid_format in [self.grid.get_content_as(format) for format in ["lines", "columns", "squares"]]:
            for x in range(9):
                for y in range(9):
                    
                    if grid_format[x].count(grid_format[x][y]) > 1:
                        return False
        
        return True

    def verify_cell(self, coordinates: tuple[int, int]):
        """
        Vérifie que les règles du sudoku sont respectées sur la colonne, la ligne et le carré de la cellule (x, y) (pas 2 fois le même nombre sur un même ligne, sur un même colonne, etc...)
        Ajoute les couleurs sur le texte
        """
        
        test_errors(coordinates = coordinates)
        
        for n in range(1, 10):
            for format in ["lines", "columns", "squares"]:
                group_coordinates = self.grid.get_coordinates_group(coordinates, format)
                group_values = self.grid.get_cell_group(coordinates, format)
            
                if group_values.count(n) > 1:
                    for cell_coordinates in group_coordinates:
                        if self.grid.get_cell_value(cell_coordinates) == n and not cell_coordinates in self.grid.duplicate_cells:
                            self.grid.duplicate_cells.append(cell_coordinates)
                    
                else:
                    for cell_coordinates in group_coordinates:
                        if self.grid.get_cell_value(cell_coordinates) == n and cell_coordinates in self.grid.duplicate_cells:
                            self.grid.duplicate_cells.remove(cell_coordinates)

        # Affichage des couleurs sur le texte
        for x in range(9):
            for y in range(9):
                if (x, y) in self.grid.duplicate_cells:
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
        
        self.clear_inputs()
        self.put_obvious_solutions()
        
        if self.backtracking_solving():
            print("Sudoku solved successfully")
            
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
                    is_algorithm_finished = False
            
            if is_algorithm_finished:
                break
    
    def backtracking_solving(self) -> bool:
        """
        Fonction récursive qui résout le Sudoku en testant toutes les possibilités
        Renvois True si la grille courante est possible à résoudre, et False si elle ne l'est pas
        """
        
        
        if self.grid.is_full():
            # Si la grille est remplie, renvoyer True si elle est résolue, et False si la résolution n'est pas valide
            return self.is_valid()
        
        # Récupérer les coordonnées de la première case vide
        first_empty_cell = self.grid.get_first_empty_cell()
        
        # Boucler sur l'ensemble des valeurs possible pour cette case
        for value in self.grid.get_possible_values(first_empty_cell):
            # Mettre la valeur à l'emplacement de la case
            self.grid.set_cell_value(first_empty_cell, value)
            
            # Si la grille est résolue, renvoyer True
            if self.backtracking_solving():
                return True
            
            # Sinon, enlever la valeur, qui n'est donc pas la bonne
            self.grid.set_cell_value(first_empty_cell, 0)
        
        # Si aucune des valeurs possibles de la case ne marche, renvoyer False
        return False