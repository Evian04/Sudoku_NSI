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
    
    def get_cell(self, coordinates: tuple[int, int]) -> Cell:
        """
        Renvoi la cellule de coordonnées (x, y)
        """
        test_errors(coordinates=coordinates)

        return self.content[coordinates[0]][coordinates[1]]
        
    def get_cell_value(self, coordinates: tuple[int, int]) -> int:
        """
        Renvoi la valeur de la case de coordonnées (x, y)
        """
        
        test_errors(coordinates=coordinates)
        
        return self.content[coordinates[0]][coordinates[1]].get_value()
    
    def get_cell_state(self, coordinates: tuple[int, int]) -> str:
        """
        Renvoi la valeur de la case de coordonnées (x, y)
        """
        
        test_errors(coordinates=coordinates)
        
        return self.content[coordinates[0]][coordinates[1]].get_state()
    
    def set_content(self, list_values: list[list[int]], list_states: list[list[str]]):
        """
        Remplace le contenu de la grille par `new content`
        """
        
        test_errors(list_values=list_values, list_states=list_states)
        
        for x in range(9):
            for y in range(9):
                self.content[x][y] = Cell(list_values[x][y], list_states[x][y])
    
    def set_cell_value(self, coordinates: tuple[int, int], value: int):
        """
        Met la case de coordonnées (x, y) à la valeur `value`
        """
        
        test_errors(coordinates=coordinates, value=value)
        
        if self.content[coordinates[0]][coordinates[1]].get_state() == 'unlocked':
            self.content[coordinates[0]][coordinates[1]].set_value(value)
        
        else:
            print(f'Grid.set_cell: cell {coordinates} is locked or superlocked')
    
    def set_cell_state(self, coordinates: tuple[int, int], state: str):
        """
        Met l'état de la case de coordonnées `coordinates` à `state`
        """
        
        test_errors(coordinates=coordinates, state=state)
        
        self.content[coordinates[0]][coordinates[1]].set_state(state)
    
    def set_cell_color(self, coordinates: tuple[int, int], color: tuple[int, int, int]):
        """
        Met la couleur de la case de coordonnées (x, y) à `color`
        """
        
        test_errors(coordinates=coordinates, color=color)
        
        self.content[coordinates[0]][coordinates[1]].set_color(color)
    
    def get_all_values(self) -> list[list[int]]:
        """
        Retourne une double liste de toutes les valeurs (identique à self.content, mais remplace les cellules pas les valeurs des cellules)
        :return:
        """
        
        return [[cell.value for cell in line] for line in self.content]
    
    def get_coordinates_as(self, coordinates: tuple[int, int], input_format: str, output_format: str) -> tuple[
        int, int]:
        """
        Convertis les coordonnées passées en argument à un autre format
        """
        
        test_errors(coordinates=coordinates, format=input_format)
        test_errors(format=output_format)
        
        match input_format:
            
            case "columns":
                coordinates = (coordinates[1], coordinates[0])
            
            case "squares":
                coordinates = (
                (coordinates[0] // 3) * 3 + coordinates[1] // 3, (coordinates[0] % 3) * 3 + coordinates[1] % 3)
        
        match output_format:
            
            case "lines":
                return coordinates
            
            case "columns":
                return (coordinates[1], coordinates[0])
            
            case "squares":
                return ((coordinates[0] // 3) * 3 + coordinates[1] // 3, (coordinates[0] % 3) * 3 + coordinates[1] % 3)
    
    def get_content_as(self, format: str) -> list[list[int]]:
        """
        Renvoi le contenu de la grille ligne par ligne, colonne par colonne ou carré par carré (argument `format`)
        """
        
        return [[self.get_cell_value(self.get_coordinates_as((x, y), format, "lines")) for y in range(9)] for x in
                range(9)]
    
    def get_coordinates_group(self, coordinates: tuple[int, int], format: str) -> list[tuple[int, int]]:
        """
        Renvoi la liste des coordonnées des cases appartenant au même groupe que la case `coordinates`
        l'argument `format` indique le type de groupe à prendre en compte (ligne, colonne ou carré)
        """
        
        test_errors(coordinates=coordinates, format=format)
        
        formated_coordinates = self.get_coordinates_as(coordinates, "lines", format)
        
        return [self.get_coordinates_as((formated_coordinates[0], y), format, "lines") for y in range(9)]
    
    def get_cell_group(self, coordinates: tuple[int, int], format: str) -> list[int]:
        """
        Renvoi la liste des valeurs des cases appartenant au même groupe que la case `coordinates`
        l'argument `format` indique le type de groupe à prendre en compte (ligne, colonne ou carré)
        """
        
        test_errors(coordinates=coordinates, format=format)
        
        formated_coordinates = self.get_coordinates_as(coordinates, "lines", format)
        
        return [self.get_cell_value(self.get_coordinates_as((formated_coordinates[0], y), format, "lines")) for y in
                range(9)]
    
    def get_all_empty_cells(self) -> list[tuple[int, int]]:
        """
        Renvoi la liste des coordonnées des cases vides de la grille
        """
        
        all_empty_cells = []
        
        # Pour toutes les cases de la grille
        for y in range(9):
            for x in range(9):
                if self.get_cell_value((x, y)) == 0:  # Si la valeur de la case est zéro
                    all_empty_cells.append((x, y))  # Ajouter à la liste des cases vides les coordonnées (x, y)
        
        return all_empty_cells
    
    def get_first_empty_cell(self) -> tuple[int, int]:
        """
        Renvoi les coordonnées de la première case vide
        """
        
        # Pour toutes les cases de la grille
        for y in range(9):
            for x in range(9):
                if self.get_cell_value((x, y)) == 0:  # Dès qu'une case vide est rencontrée
                    return (x, y)  # Renvoyer les coordonnées (x, y)
    
    def get_possible_values(self, coordinates: tuple[int, int]) -> list[int]:
        """
        Renvoi les valeurs possibles (1 à 9) de la case en fonctions des autres chiffres de la même ligne, colomne ou carré
        """
        
        test_errors(coordinates=coordinates)
        possible_values = [n + 1 for n in range(9)]
        
        # Pour tout les formats existants
        for format in ["lines", "columns", "squares"]:
            group = self.get_cell_group(coordinates, format)
            
            for cell_value in group:
                if cell_value in possible_values:
                    possible_values.remove(cell_value)
        
        return possible_values
    
    def is_full(self) -> bool:
        """
        Renvoi True si la grille est remplie, et False si elle ne l'est pas
        """
        
        for x in range(9):
            for y in range(9):
                if self.get_cell_value((x, y)) == 0:
                    return False
        
        return True
