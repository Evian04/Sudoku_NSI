import os.path

import pygame

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
        
        # TEST
        
        self.selected_cell = [x, y]
    
    def deselect_cell(self):
        """
        Déselectionne la case sélectionnée
        """
        
        self.selected_cell = [-1, -1]
    
    def load_grid(self, new_grid):
        """
        /!\ charge une grille à partir d'un fichier ? Pourquoi new_grid ?
        """
    
    def save_grid(self, output_filepath:str):
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
