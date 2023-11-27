from src.programs.cell import Cell


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
        
        if type(coordinates[0]) != int:
            raise TypeError(f"The `x` argument must be an intger (type : {type(coordinates[0])})")
        
        if type(coordinates[1]) != int:
            raise TypeError(f"The `y` argument must be an intger (type : {type(coordinates[1])})")
        
        if coordinates[0] < 0 or coordinates[0] >= 9:
            raise ValueError(f"The `x` argument must be between 0 and 9 (value : {coordinates[0]})")
        
        if coordinates[1] < 0 or coordinates[1] >= 9:
            raise ValueError(f"The `y` argument must be between 0 and 9 (value : {coordinates[1]})")
        
        return self.content[coordinates[0]][coordinates[1]].get_value()
    
    def get_cell_state(self, coordinates: tuple[int, int]) -> str:
        """
        Renvoi la valeur de la case de coordonnées (x, y)
        """
        
        if type(coordinates[0]) != int:
            raise TypeError(f"The `x` argument must be an intger (type : {type(coordinates[0])})")
        
        if type(coordinates[1]) != int:
            raise TypeError(f"The `y` argument must be an intger (type : {type(coordinates[1])})")
        
        if coordinates[0] < 0 or coordinates[0] >= 9:
            raise ValueError(f"The `x` argument must be between 0 and 9 (value : {coordinates[0]})")
        
        if coordinates[1] < 0 or coordinates[1] >= 9:
            raise ValueError(f"The `y` argument must be between 0 and 9 (value : {coordinates[1]})")
        
        return self.content[coordinates[0]][coordinates[1]].get_state()
    
    def set_content(self, new_values: list[list[int]], new_states: list[list[str]]):
        """
        Remplace le contenu de la grille par `new content`
        """
        
        if type(new_values) != list:
            raise TypeError(f"The `new_values` argument must be a list (type : {type(new_values)})")
        
        if type(new_states) != list:
            raise TypeError(f"The `new_states` argument must be a list (type : {type(new_states)})")
        
        if len(new_values) != 9:
            raise ValueError(f"The `new_values` argument must have a length of 9 (length : {len(new_values)})")
        
        if len(new_states) != 9:
            raise ValueError(f"The `new_states` argument must have a length of 9 (length : {len(new_states)})")
        
        for x in range(9):
            for y in range(9):
                self.content[x][y] = Cell(new_values[x][y], new_states[x][y])
    
    def set_cell_value(self, coordinates: tuple[int, int], value: int):
        """
        Met la case de coordonnées (x, y) à la valeur `value`
        """
        
        if type(coordinates[0]) != int:
            raise TypeError(f"The `x` argument must be an integer (type : {coordinates[0]})")
        
        if type(coordinates[1]) != int:
            raise TypeError(f"The `y` argument must be an integer (type : {type(coordinates[1])})")
        
        if type(value) != int:
            raise TypeError(f"The `value` argument must be a string (type : {type(value)})")
        
        if coordinates[0] < 0 or coordinates[0] >= 9:
            raise ValueError(f"The `x` argument must be between 0 and 9 (value : {coordinates[0]})")
        
        if coordinates[1] < 0 or coordinates[1] >= 9:
            raise ValueError(f"The `y` argument must be between 0 and 9 (value : {coordinates[1]})")
        
        if int(value) < 0 or int(value) > 9:
            raise ValueError(f"The `value` argument must contains a integer between 0 and 9 (value : {value})")
        
        if self.content[coordinates[0]][coordinates[1]].get_state() == 'unlocked':
            self.content[coordinates[0]][coordinates[1]].put_value(value)
        
        else:
            print(f'Grid.set_cell: cell {coordinates[1]} is locked or superlocked')
            
    def set_cell_color(self, coordinates: tuple[int, int], color: tuple[int, int, int]):
        """
        Met la couleur de la case de coordonnées (x, y) à `color`
        """
        
        if type(coordinates[0]) != int:
            raise TypeError(f"The `x` argument must be an integer (type : {type(coordinates[0])})")
        
        if type(coordinates[1]) != int:
            raise TypeError(f"The `y` argument must be an integer (type : {type(coordinates[1])})")
        
        if type(color) != tuple:
            raise TypeError(f"The `color` argument must be a tuple (type : {type(color)})")
        
        if coordinates[0] < 0 or coordinates[0] >= 9:
            raise ValueError(f"The `x` argument must be between 0 and 9 (value : {coordinates[0]})")
        
        if coordinates[1] < 0 or coordinates[1] >= 9:
            raise ValueError(f"The `y` argument must be between 0 and 9 (value : {coordinates[1]})")
        
        if len(color) != 3:
            raise ValueError(f"The `color` argument must have a length of 3 (length : {color})")
        
        self.content[coordinates[0]][coordinates[1]].set_color(color)
    
    def get_all_values(self) -> list[list[int]]:
        """
        Retourne une double liste de toutes les valeurs (identique à self.content, mais remplace les cellules pas les valeurs des cellules)
        :return:
        """
        
        return [[cell.value for cell in line] for line in self.content]
    
    def get_lines(self) -> list[list[tuple[int, int]]]:
        """
        retourne la liste des lignes avec les coordonnées de chaque cellule
        :return: liste de lignes de coordonnées
        """
        return [[(x,y) for x in range(self.column_number)] for y in range(self.line_number)]
    
    def get_columns(self) -> list[list[tuple[int, int]]]:
        """
        retourne la liste des lignes avec les coordonnées de chaque cellule
        :return: liste de colonnes de coordonnées
        """
        return [[(x, y) for y in range(9)] for x in range(9)]
    
    def get_squares(self):
        """
        retourne la liste des carrés avec les coordonnées de chaque cellule
        :return: liste de carrés de coordonnées
        """
        return [[((x // 3) * 3 + y // 3,(x % 3) * 3 + y % 3) for y in range(9)] for x in range(9)]  # récupère le contneu des sous grilles (carrés)
    
    def get_cell_line(self, coordinates: tuple[int, int]) -> list[tuple[int, int]]:
        """
        retourne la ligne de la cellule spécifié
        :return: liste des coordonnées des cellules de la ligne
        """
        
        if type(coordinates[1]) != int:
            raise TypeError(f"The `y` argument must be an intger (type : {type(coordinates[1])})")
        
        if coordinates[1] < 0 or coordinates[1] >= 9:
            raise ValueError(f"The `y` argument must be between 0 and 9 (value : {coordinates[1]})")
        
        return [(x, coordinates[1]) for x in range(9)]
        
    def get_cell_column(self, coordinates: tuple[int, int]) -> list[tuple[int, int]]:
        """
        retourne la colonne de la cellule spécifié
        :return: liste des coordonnées des cellules de la colonne
        """
        
        if type(coordinates[0]) != int:
            raise TypeError(f"The `x` argument must be an intger (type : {type(coordinates[0])})")
        
        if coordinates[0] < 0 or coordinates[0] >= 9:
            raise ValueError(f"The `x` argument must be between 0 and 9 (value : {coordinates[0]})")
        
        return [(coordinates[0], y) for y in range(9)]
    
    def get_cell_square(self, coordinates: tuple[int, int]) -> list[tuple[int, int]]:
        """
        retourne la ligne de la cellule spécifié
        :return: liste des coordonnées des cellules du carré
        """
        
        if type(coordinates[0]) != int:
            raise TypeError(f"The `x` argument must be an intger (type : {type(coordinates[0])})")
        
        if type(coordinates[1]) != int:
            raise TypeError(f"The `y` argument must be an intger (type : {type(coordinates[1])})")
        
        if coordinates[0] < 0 or coordinates[0] >= 9:
            raise ValueError(f"The `x` argument must be between 0 and 9 (value : {coordinates[0]})")
        
        if coordinates[1] < 0 or coordinates[1] >= 9:
            raise ValueError(f"The `y` argument must be between 0 and 9 (value : {coordinates[1]})")
        
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
        
        if type(coordinates[0]) != int:
            raise TypeError(f"The `x` argument must be an intger (type : {type(coordinates[0])})")
        
        if type(coordinates[1]) != int:
            raise TypeError(f"The `y` argument must be an intger (type : {type(coordinates[1])})")
        
        if coordinates[0] < 0 or coordinates[0] >= 9:
            raise ValueError(f"The `x` argument must be between 0 and 9 (value : {coordinates[0]})")
        
        if coordinates[1] < 0 or coordinates[1] >= 9:
            raise ValueError(f"The `y` argument must be between 0 and 9 (value : {coordinates[1]})")
        
        if self.get_cell_value(coordinates) != 0:
            raise ValueError(f"The cell {coordinates} isn't empty")
        
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