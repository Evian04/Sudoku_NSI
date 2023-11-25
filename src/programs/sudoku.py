import os.path
import pygame
from tkinter.filedialog import askopenfilename
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
    
    def load_grid(self):
        """
        Charge une grille à partir d'un fichier
        """
        
        # Ouvre une fenêtre de dialogue permettant à l'utilisateur de choisir le fichier à charger
        file_path = askopenfilename(initialdir="src/save_folder", initialfile="model.sdk", filetypes=[("Sudoku file", "*.sdk")])
        if not file_path:
            print("No file selected, Empty grid...")
            return False
        
        with open(file_path, "rt") as file:
            file_content = file.read()
        
        file_content = file_content.split("\n\n")
        
        cell_values = [[int(value) for value in line] for line in file_content[0].split("\n")]
        
        """convert_state = {"0": "unlocked", "1": "locked", "2": "superlocked"}
        cell_states = [[convert_state[state] for state in line] for line in file_content[1].split("\n")]
        """
        cell_states = [['superlocked' if int(value) > 0 else 'unlocked'
                        # double boucle imbriquée qui attribue l'état 'unlocked' si la valeur est > à 0 (0 = case vide)
                        for value in line] for line in file_content[0].split("\n")]
        self.grid.set_content(cell_values, cell_states)
    
    def save_grid(self, output_filepath: str):
        """
        /!\ Enregistre la grille actuelle dans un fichier Avec ou sans les valeurs saisies par utilisateur ?
        :param output_filepath:
        :return: new grid
        """
        if not os.path.exists(output_filepath):
            raise ValueError(f"file '{output_filepath}' does not exist")
    
    def lock_cell(self, x: int, y: int):
        """
        Verrouille la case (x, y), la valeur de la case ne pourra plus être modifiée
        """
    
    def unlock_cell(self, x: int, y: int):
        """
        Déverrouille la case (x, y), la valeur de la case pourra de nouveau être modifiée
        """
    
    def verify_grid(self) -> list[tuple[int, int]]:
        """
        Vérifie que les règles du sudoku sont respectées (pas 2 fois le même nombre sur la ligne, sur la colonne, etc...)
        :return: liste des positions (x, y) où les valeurs sont incorrectes
        """
        return list()
    
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
