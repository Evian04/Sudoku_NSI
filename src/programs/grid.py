from src.programs.cell import Cell
from src.programs.test_errors import test_errors


class Grid:
    """
    La class `Grid` permet de stocker et de gérer le contenu de la grille du sudoku
    """
    
    def __init__(self, content: list[list[Cell]] = None):
        if content:
            # Si le contenu du sudoku est précisé, sauvegarder ce contenu
            self.content = content.copy()
        
        else:
            # Sinon créer une grille vierge
            self.content = [[Cell(0, "unlocked") for y in range(9)] for x in range(9)]

        self.line_number = 9
        self.column_number = 9
        self.duplicate_cells: list[tuple[int, int]] = list()

    def get_cell_value(self, coordinates: tuple[int, int]) -> int:
        """
        Renvoi la valeur de la case de coordonnées (x, y)
        """
        
        test_errors(coordinates = coordinates)
        
        return self.content[coordinates[0]][coordinates[1]].get_value()
    
    def get_cell_state(self, coordinates: tuple[int, int]) -> str:
        """
        Renvoi la valeur de la case de coordonnées (x, y)
        """
        
        test_errors(coordinates = coordinates)
        
        return self.content[coordinates[0]][coordinates[1]].get_state()
    
    def set_content(self, list_values: list[list[int]], list_states: list[list[str]]):
        """
        Remplace le contenu de la grille par `new content`
        """
        
        test_errors(list_values = list_values, list_states = list_states)
        
        for x in range(9):
            for y in range(9):
                self.content[x][y] = Cell(list_values[x][y], list_states[x][y])
    
    def set_cell_value(self, coordinates: tuple[int, int], value: int):
        """
        Met la case de coordonnées (x, y) à la valeur `value`
        """
        
        test_errors(coordinates = coordinates, value = value)
        
        if self.content[coordinates[0]][coordinates[1]].get_state() == 'unlocked':
            self.content[coordinates[0]][coordinates[1]].set_value(value)
        
        else:
            print(f'Grid.set_cell: cell {coordinates[1]} is locked or superlocked')
            
    def set_cell_color(self, coordinates: tuple[int, int], color: tuple[int, int, int]):
        """
        Met la couleur de la case de coordonnées (x, y) à `color`
        """
        
        test_errors(coordinates = coordinates, color = color)
        
        self.content[coordinates[0]][coordinates[1]].set_color(color)
    
    def get_all_values(self) -> list[list[int]]:
        """
        Retourne une double liste de toutes les valeurs (identique à self.content, mais remplace les cellules pas les valeurs des cellules)
        :return:
        """
        
        return [[cell.value for cell in line] for line in self.content]
    
    def get_lines(self) -> list[list[int]]:
        """
        retourne la liste des lignes avec la valeur de chaque cellule
        :return: liste de lignes de coordonnées
        """
        return [[self.get_cell_value((x, y)) for y in range(9)] for x in range(9)]
    
    def get_columns(self) -> list[list[int]]:
        """
        retourne la liste des lignes avec la valeur de chaque cellule
        :return: liste de colonnes de coordonnées
        """
        
        return [[self.get_cell_value((x, y)) for y in range(9)] for x in range(9)]
    
    def get_squares(self):
        """
        retourne la liste des carrés avec la valeur de chaque cellule
        :return: liste de carrés de coordonnées
        """
        
        return [[self.get_cell_value(((x // 3) * 3 + y // 3, (x % 3) * 3 + y % 3)) for y in range(9)] for x in range(9)]
    
    def get_cell_line(self, coordinates: tuple[int, int]) -> list[tuple[int, int]]:
        """
        retourne la ligne de la cellule spécifié
        :return: liste des coordonnées des cellules de la ligne
        """
        
        test_errors(coordinates = coordinates)
        
        return [(x, coordinates[1]) for x in range(9)]
        
    def get_cell_column(self, coordinates: tuple[int, int]) -> list[tuple[int, int]]:
        """
        retourne la colonne de la cellule spécifié
        :return: liste des coordonnées des cellules de la colonne
        """
        
        test_errors(coordinates = coordinates)
        
        return [(coordinates[0], y) for y in range(9)]
    
    def get_cell_square(self, coordinates: tuple[int, int]) -> list[tuple[int, int]]:
        """
        retourne la ligne de la cellule spécifié
        :return: liste des coordonnées des cellules du carré
        """
        
        test_errors(coordinates = coordinates)
        
        square = [
            (x_square, y_square) for x_square in range(coordinates[0] // 3, coordinates[0] // 3 + 3) for y_square in range(coordinates[1] // 3, coordinates[1] // 3 + 3)
        ]
        
        return square
    
    def get_all_empty_cells(self) -> list[tuple[int, int]]:
        """
        Renvois la liste des coordonnées des cases vides de la grille
        """
        
        all_empty_cells = []
        
        # Pour toutes les cases de la grille
        for x in range(9):
            for y in range(9):
                if self.get_cell_value((x, y)) == 0: # Si la valeur de la case est zéro
                    all_empty_cells.append((x, y))   # Ajouter à la liste des cases vides les coordonnées (x, y)
                    
        return all_empty_cells

    def get_first_empty_cell(self) -> tuple[int, int]:
        """
        Renvois les coordonnées de la première case vide
        """
        
        # Pour toutes les cases de la grille
        for x in range(9):
            for y in range(9):
                if self.get_cell_value((x, y)) == 0: # Dès qu'un case vide est rencontrée
                    return (x, y)                    # Renvoyer les coordonnées (x, y)
    
    def get_possible_values(self, coordinates: tuple[int, int]) -> list[int]:
        """
        Renvois les valeurs possibles (1 à 9) de la case en fonctions des autres chiffres de la même ligne, colomne ou carré
        """
        
        test_errors(coordinates = coordinates)
        
        possible_values = [n + 1 for n in range(9)]
        
        for cell_position in self.get_cell_line(coordinates):
            cell_value = self.get_cell_value(cell_position)
            if cell_value in possible_values:
                possible_values.remove(cell_value)
        
        for cell_position in self.get_cell_column(coordinates):
            cell_value = self.get_cell_value(cell_position)
            if cell_value in possible_values:
                possible_values.remove(cell_value)
        
        for cell_position in self.get_cell_square(coordinates):
            cell_value = self.get_cell_value(cell_position)
            if cell_value in possible_values:
                possible_values.remove(cell_value)
                
        return possible_values
    
    def is_full(self) -> bool:
        """
        Renvois True si la grille est remplie, et False si elle ne l'est pas
        """
        
        for x in range(9):
            for y in range(9):
                if self.get_cell_value((x, y)) == 0:
                    return False
        
        return True