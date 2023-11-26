import os.path
import pygame
from tkinter.filedialog import askopenfilename, asksaveasfilename
from src.programs.grid import Grid


class Sudoku:
    
    def __init__(self, game):
        self.game = game
        self.grid = Grid()
        self.selected_cell = [-1, -1]  # Coordonnées de la case sélectionnée, [-1, -1] si aucune case
    def select_cell(self, x: int, y: int):
        """
        Selectionne la case de coordonnées (x, y)
        """
        
        if type(x) != int:
            raise TypeError(f"The `x` argument must be an integer (type : {type(x)})")
        
        if type(y) != int:
            raise TypeError(f"The `y` argument must be an integer (type : {type(y)})")
        
        if x < 0 or x > 8:
            raise ValueError(f"The `x` argument must be between 0 and 8")
        
        if y < 0 or y > 8:
            raise ValueError(f"The `y` argument must be between 0 and 8")
        
        self.selected_cell = [x, y]
    
    def deselect_cell(self):
        """
        Déselectionne la case sélectionnée
        """
        
        self.selected_cell = [-1, -1]
        
    def set_selected_cell_value(self, value: int):
        """
        Met la valeur de la case sélectionnée à `value`
        """
        
        if type(value) != int:
            raise TypeError(f"The `value` argument must be an integer (type : {type(value)})")
        
        if value < 0 or value > 9:
            raise ValueError(f"The `value` argument must be between 0 and 9 (value : {value})")
        
        if self.selected_cell == [-1, -1]:
            raise ValueError("You must select a cell in order to set its value")
        
        self.grid.set_cell_value(self.selected_cell[0], self.selected_cell[1], value)
        
    def set_selected_cell_color(self, color: tuple[int, int, int]):
        """
        Met la couleur de la case sélectionnée à `color`
        """
        
        if type(color) != tuple:
            raise TypeError(f"The `color` argument must be a tuple (type : {type(color)})")
        
        if len(color) != 3:
            raise ValueError(f"The `color` argument must have a length of 3 (length : {len(color)})")
        
        self.grid.set_cell_color(self.selected_cell[0], self.selected_cell[1], color)
    
    def load_grid(self):
        """
        Charge une grille à partir d'un fichier
        """
        
        # Ouvre une fenêtre de dialogue permettant à l'utilisateur de choisir le fichier à charger
        file_path = askopenfilename(initialdir="src/save_folder", initialfile="model.sdk",
                                    filetypes=[("Sudoku file", "*.sdk")])
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
        
        if self.selected_cell == [-1, -1]:
            raise ValueError("You must select a cell in order to lock it")
        
        if self.grid.get_cell_state(self.selected_cell[0], self.selected_cell[1]) == "superlocked":
            raise ValueError("You cannot lock a cell that is superlocked")
        
        self.grid.content[self.selected_cell[0]][self.selected_cell[1]].state = "locked"
    
    def unlock_selected_cell(self):
        """
        Déverrouille la case sélectionnée, la valeur de la case pourra de nouveau être modifiée
        """
        
        if self.selected_cell == [-1, -1]:
            raise ValueError("You must select a cell in order to unlock it")
        
        if self.grid.get_cell_state(self.selected_cell[0], self.selected_cell[1]) == "superlocked":
            raise ValueError("You cannot unlock a cell that is superlocked")
        
        self.grid.content[self.selected_cell[0]][self.selected_cell[1]].state = "unlocked"
    
    def verify_grid(self):
        """
        Vérifie que les règles du sudoku sont respectées sur toute la grille (pas 2 fois le même nombre sur un même ligne, sur un même colonne, etc...)
        Ajoute les couleurs sur le texte
        """
        
        content_as_lines = self.grid.get_all_values()  # récupère le contenu des lignes
        content_as_columns = [[content_as_lines[y][x] for y in range(9)] for x in range(9)]  # récupère le contenu des colonnes
        content_as_squares = [[content_as_lines[(x // 3) * 3 + y // 3][(x % 3) * 3 + y % 3] for y in range(9)] for x in range(9)]  # récupère le contneu des sous grilles (carrés)
        
        for x in range(self.grid.column_number):  # balaye x (colonnes)
            for n in range(1, 9 + 1):  # nombres à vérifier
                self.grid.duplicate_cells = list()
                # vérification lignes
                if content_as_lines[x].count(n) > 1:
                    for y in range(self.grid.line_number):
                        if content_as_lines[x][y] == n and not (x, y) in self.grid.duplicate_cells:
                            self.grid.duplicate_cells.append((x, y))
                
                # vérification colonnes
                if content_as_columns[x].count(n) > 1:
                    for y in range(self.grid.line_number):
                        if content_as_columns[x][y] == n and not (y, x) in self.grid.duplicate_cells:  # (y,x) parce que les valuers des colonnes sont inversées par rapport à celle de slignes
                            self.grid.duplicate_cells.append((y, x))
                            
                # vérification sous-grilles (carrés)
                if content_as_squares[x].count(n) > 1:
                    for y in range(len(content_as_squares[x])):
                        if content_as_squares[x][y] == n and not ((x // 3) * 3 + y // 3, (x % 3) * 3 + y % 3) in self.grid.duplicate_cells:
                            self.grid.duplicate_cells.append(((x // 3) * 3 + y // 3, (x % 3) * 3 + y % 3))
        
        # Affichage des couleurs sur le texte
        for x in range(self.grid.column_number):
            for y in range(self.grid.line_number):
                if (x, y) in self.grid.duplicate_cells:
                    self.grid.content[x][y].text.set_color((255, 0, 0))
        
                else:
                    self.grid.content[x][y].text.set_color((0, 0, 0))

    def verify_cell(self, x_cell:int, y_cell:int):
        """
        Vérifie que les règles du sudoku sont respectées sur la colonne, la ligne et le carré de la cellule (x, y) (pas 2 fois le même nombre sur un même ligne, sur un même colonne, etc...)
        Ajoute les couleurs sur le texte
        """
        line = self.grid.get_cell_line(y_cell)
        column = self.grid.get_cell_column(x_cell)
        square = self.grid.get_cell_square(x_cell, y_cell)
        # vérifier ligne
        for nb in range(1, 9 + 1):
            
            if [self.grid.content[x][y].value for x, y in line].count(nb) > 1:
                for x, y in line:
                    if self.grid.content[x][y].value == nb and not (x, y) in self.grid.duplicate_cells:
                        self.grid.duplicate_cells.append((x, y))
            
            if [self.grid.content[x][y].value for x, y in column].count(nb) > 1:
                for x, y in column:
                    if self.grid.content[x][y].value == nb and not (x, y) in self.grid.duplicate_cells:
                        self.grid.duplicate_cells.append((x, y))
            
            if [self.grid.content[x][y].value for x, y in square].count(nb) > 1:
                for x, y in square:
                    if self.grid.content[x][y].value == nb and not (x, y) in self.grid.duplicate_cells:
                        self.grid.duplicate_cells.append((x, y))

        # Affichage des couleurs sur le texte
        for x in range(self.grid.column_number):
            for y in range(self.grid.line_number):
                if (x, y) in self.grid.duplicate_cells:
                    self.grid.content[x][y].text.set_color((255, 0, 0))

                else:
                    self.grid.content[x][y].text.set_color((0, 0, 0))
        
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
