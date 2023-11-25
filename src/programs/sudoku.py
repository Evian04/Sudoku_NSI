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
    
    def load_grid(self):
        """
        Charge une grille à partir d'un fichier
        """
        
        # Ouvre une fenêtre de dialogue permettant à l'utilisateur de choisir le fichier à charger
        file_path = askopenfilename(initialdir="src/save_folder", initialfile="model.sdk",
                                    filetypes=[("Sudoku file", "*.sdk")])
        if not file_path:
            print("No file selected for opening, Empty grid...")
            return False
        
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
        Vérifie que les règles du sudoku sont respectées (pas 2 fois le même nombre sur la linee, sur la colonne, etc...)
        :return: liste des positions (x, y) où les valeurs sont incorrectes
        """
        print("verify")
        
        numbers_to_verify = list(range(1, self.column_number))

        # VERIFIER LES COLONNES
        #recupérer les colonnes
        columns = [column for column in self.grid.get_all_values()]
        for i, column in enumerate(columns):
            for number_to_verify in numbers_to_verify:
                if column.count(number_to_verify) > 1:
                    print(f"error line {i}, number '{number_to_verify}' {column.count(number_to_verify)} times")

        
        # VERIFIER LES LIGNES
        # opération complexe pour récupérer une liste des lignes
        lines = [[line[i] for line in self.grid.get_all_values()] for i in range(len(self.grid.get_all_values()[0]))]
        for i, line in enumerate(lines):
            for number_to_verify in numbers_to_verify:
                if line.count(number_to_verify) > 1:
                    print(f"error line {i}, number '{number_to_verify}' {line.count(number_to_verify)} times")
        
        
        # VERIFIER SOUS-GRILLE (zone en 3x3 intermédiaire)
        # code à faire
        
        return True
    
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
