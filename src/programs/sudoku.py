import os.path
import pygame
from tkinter.filedialog import askopenfilename, asksaveasfilename
from src.programs.grid import Grid


class Sudoku:
    
    def __init__(self, game):
        self.game = game
        self.grid = Grid()
        self.selected_cell = [-1, -1]  # Coordonnées de la case sélectionnée, [-1, -1] si aucune case
        self.line_number = 9
        self.column_number = 9
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
    
    def verify_grid(self) -> list[tuple[int, int]]:
        """
        Vérifie que les règles du sudoku sont respectées (pas 2 fois le même nombre sur un même ligne, sur un même colonne, etc...)
        :return: liste des positions (x, y) où les valeurs sont incorrectes
        """
        print("verify")
        
        duplicate_cells = []
        
        content_as_lines = self.grid.get_all_values()
        content_as_columns = [[content_as_lines[y][x] for y in range(9)] for x in range(9)]
        content_as_squares = [[content_as_lines[(x // 3) * 3 + y // 3][(x % 3) * 3 + y % 3] for y in range(9)] for x in range(9)]
        
        for x in range(9):
            for n in range(1, 10):
                
                if content_as_lines[x].count(n) > 1:
                    for y in range(9):
                        if content_as_lines[x][y] == n and not (x, y) in duplicate_cells:
                            duplicate_cells.append((x, y))
                            
                if content_as_columns[x].count(n) > 1:
                    for y in range(9):
                        if content_as_columns[x][y] == n and not (y, x) in duplicate_cells:
                            duplicate_cells.append((y, x))
                            
                if content_as_columns[x].count(n) > 1:
                    for y in range(9):
                        if content_as_squares[x][y] == n and not ((x // 3) * 3 + y // 3, (x % 3) * 3 + y % 3) in duplicate_cells:
                            duplicate_cells.append(((x // 3) * 3 + y // 3, (x % 3) * 3 + y % 3))
        
        return duplicate_cells
    
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
