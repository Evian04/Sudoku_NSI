from src.programs.cell import Cell
from src.programs.test_errors import test_errors


class Grid:
    """
    La class "Grid" permet de stocker et de gérer le contenu de la grille du sudoku
    """
    
    def __init__(self, size: int = 9, content: list[list[Cell]] = None):
        test_errors(size)
        self.size = size
        self.square_size = int(size ** 0.5)
        if content:
            # Si le contenu du sudoku est précisé, sauvegarder ce contenu
            self.content = content.copy()
        
        else:
            # Sinon créer une grille vierge
            self.content = [[Cell(0, "unlocked", self.size) for y in range(self.size)] for x in range(self.size)]
        
    def get_cell(self, coordinates: tuple[int, int]) -> Cell:
        """
        Renvoi la case de coordonnées (x, y)
        """
        
        test_errors(self.size, coordinates = coordinates)

        return self.content[coordinates[0]][coordinates[1]]
    
    def set_content(self, list_values: list[list[int]], list_states: list[list[str]]):
        """
        Remplace le contenu de la grille par "new content"
        """
        
        test_errors(self.size, list_values = list_values, list_states = list_states)
        
        for x in range(self.size):
            for y in range(self.size):
                self.content[x][y] = Cell(list_values[x][y], list_states[x][y], self.size)
    
    def get_all_values(self) -> list[list[int]]:
        """
        Retourne une double liste de toutes les valeurs
        (identique à self.content, mais remplace les cases pas les valeurs des cases)
        """
        
        return [[cell.value for cell in line] for line in self.content]
    
    def set_cell_value(self, coordinates: tuple[int, int], value: int):
        """
        Met la case de coordonnées (x, y) à la valeur "value"
        """
        
        test_errors(self.size, coordinates = coordinates, value = value)
        
        if self.content[coordinates[0]][coordinates[1]].state == "unlocked":
            self.content[coordinates[0]][coordinates[1]].set_value(value)
        
        else:
            print(f"Grid.set_cell: cell {coordinates} is locked or superlocked")
        
    def get_cell_value(self, coordinates: tuple[int, int]) -> int:
        """
        Renvoi la valeur de la case de coordonnées (x, y)
        """
        
        test_errors(self.size, coordinates = coordinates)
        
        return self.content[coordinates[0]][coordinates[1]].value
    
    def set_cell_state(self, coordinates: tuple[int, int], state: str):
        """
        Met l'état de la case de coordonnées "coordinates" à "state"
        """
        
        test_errors(self.size, coordinates = coordinates, state = state)
        
        self.content[coordinates[0]][coordinates[1]].set_state(state)
    
    def get_cell_state(self, coordinates: tuple[int, int]) -> str:
        """
        Renvoi la valeur de la case de coordonnées (x, y)
        """
        
        test_errors(self.size, coordinates = coordinates)
        
        return self.content[coordinates[0]][coordinates[1]].state
    
    def set_cell_conflicting_state(self, coordinates: tuple[int, int], conflicting_state: bool):
        """
        Met la variable indiquant si la case est en conflit ou non à l'état indiqué
        """

        assert type(conflicting_state) == bool, 'The "conflicting_state" argument must be a boolean'
        
        self.content[coordinates[0]][coordinates[1]].set_conflicting_state(conflicting_state)
    
    def is_cell_in_conflict(self, coordinates: tuple[int, int]) -> bool:
        """
        Renvois si la case est en conflit avec d'autres ou non
        """
        
        test_errors(self.size, coordinates = coordinates)
        
        x, y = coordinates
        conflicting_state = self.content[x][y].is_in_conflict
        
        assert type(conflicting_state) == bool, \
            f'The "is_in_conflict" variable of the cell {coordinates} must be a boolean (type : {type(conflicting_state)})'
            
        return conflicting_state
    
    def get_coordinates_as(self, coordinates: tuple[int, int], input_format: str, output_format: str) -> tuple[int, int]:
        """
        Convertis les coordonnées passées en argument à un autre format
        """
        
        test_errors(self.size, coordinates = coordinates, format = input_format)
        test_errors(format = output_format)
        
        match input_format:
            
            case "columns":
                coordinates = (coordinates[1], coordinates[0])
            
            case "squares":
                coordinates = (
                    (coordinates[0] // self.square_size) * self.square_size + coordinates[1] // self.square_size,
                    (coordinates[0] % self.square_size) * self.square_size + coordinates[1] % self.square_size
                )
        
        match output_format:
            
            case "lines":
                return coordinates
            
            case "columns":
                return (coordinates[1], coordinates[0])
            
            case "squares":
                return (
                    (coordinates[0] // self.square_size) * self.square_size + coordinates[1] // self.square_size,
                    (coordinates[0] % self.square_size) * self.square_size + coordinates[1] % self.square_size
                )
    
    def get_all_values_as(self, format: str) -> list[list[int]]:
        """
        Renvoi les valeurs des cases de la grille en lignes, colonnes ou carrés (argument "format")
        """
        
        test_errors(format = format)
        
        return [
            [
                self.get_cell_value(self.get_coordinates_as((x, y), format, "lines")) for y in range(self.size)
            ] for x in range(self.size)
        ]
        
    def get_all_coordinates_as(self, format: str) -> list[list[tuple[int, int]]]:
        """
        Renvois les coordonnées des cases de la grilles ordonnées en lignes, colonnes ou carrés (argument "format")
        """
        
        test_errors(format = format)
        
        return [
            [
                self.get_coordinates_as((x, y), format, "lines") for y in range(self.size)
            ] for x in range(self.size)
        ]
    
    def get_group_coordinates(self, coordinates: tuple[int, int], format: str) -> list[tuple[int, int]]:
        """
        Renvoi la liste des coordonnées des cases appartenant au même groupe que la case "coordinates"
        l'argument "format" indique le type de groupe à prendre en compte (ligne, colonne ou carré)
        """
        
        test_errors(self.size, coordinates = coordinates, format = format)
        
        formated_coordinates = self.get_coordinates_as(coordinates, "lines", format)
        
        return [self.get_coordinates_as((formated_coordinates[0], y), format, "lines") for y in range(self.size)]
    
    def get_group_values(self, coordinates: tuple[int, int], format: str) -> list[int]:
        """
        Renvoi la liste des valeurs des cases appartenant au même groupe que la case "coordinates"
        L'argument "format" indique le type de groupe à prendre en compte (ligne, colonne ou carré)
        """
        
        test_errors(self.size, coordinates = coordinates, format = format)
        
        formated_coordinates = self.get_coordinates_as(coordinates, "lines", format)
        
        return [
            self.get_cell_value(self.get_coordinates_as((formated_coordinates[0], y), format, "lines")) for y in range(self.size)
        ]
    
    def get_all_empty_cells(self) -> list[tuple[int, int]]:
        """
        Renvoi la liste des coordonnées des cases vides de la grille
        """
        
        all_empty_cells = []
        
        # Pour toutes les cases de la grille
        for y in range(self.size):
            for x in range(self.size):
                coordinates = (x, y)
                
                if self.get_cell_value(coordinates) == 0:  # Si la valeur de la case est zéro
                    test_errors(self.size, coordinates = coordinates)
                    all_empty_cells.append(coordinates)  # Ajouter à la liste des cases vides les coordonnées (x, y)
        
        return all_empty_cells
    
    def get_first_empty_cell(self) -> tuple[int, int]:
        """
        Renvoi les coordonnées de la première case vide
        """
        
        # Pour toutes les cases de la grille
        for y in range(self.size):
            for x in range(self.size):
                coordinates = (x, y)
                
                if self.get_cell_value(coordinates) == 0:  # Dès qu'une case vide est rencontrée
                    test_errors(self.size, coordinates = coordinates)
                    return (x, y)  # Renvoyer les coordonnées (x, y)
    
    def get_possible_values(self, coordinates: tuple[int, int]) -> list[int]:
        """
        Renvoi les valeurs possibles (de 1 à "self.size") de la case en fonctions des autres chiffres de la même ligne, colomne ou carré
        """
        
        test_errors(self.size, coordinates = coordinates)
        
        possible_values = [n + 1 for n in range(self.size)]
        
        # Pour tout les formats existants
        for format in ["lines", "columns", "squares"]:
            group = self.get_group_values(coordinates, format)
            
            for cell_value in group:
                if cell_value in possible_values:
                    possible_values.remove(cell_value)
        
        return possible_values
    
    def is_full(self) -> bool:
        """
        Renvoi True si la grille est remplie, et False si elle ne l'est pas
        """
        
        for x in range(self.size):
            for y in range(self.size):
                if self.get_cell_value((x, y)) == 0:
                    return False
        
        return True
