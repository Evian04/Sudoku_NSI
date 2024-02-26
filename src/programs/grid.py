from src.programs.cell import Cell
from src.programs.test_errors import test_errors


class Grid:
    """
    La class "Grid" permet de stocker et de gérer le contenu de la grille du sudoku
    """
    
    def __init__(self, size: int):
        test_errors(size)
        
        self.size = size
        self.square_size = int(self.size ** 0.5)
        self.cells_count = self.size ** 2 # nombre total de cases
        self.possible_values = "123456789ABCDEFG"
        
        self.content = [[Cell("0", "unlocked", self.size) for y in range(self.size)] for x in range(self.size)]
    
    def copy(self):
        """
        Renvoie une copie de la grille
        Permet de créer un nouvel objet Grid avec les mêmes attributs
        """
        
        copied_grid = Grid(self.size)
        copied_grid.set_content(self.get_all_values(), self.get_all_states())
        
        # Test postconditions
        test_errors(self.size, list_values = copied_grid.get_all_values(), list_states = copied_grid.get_all_states())
        
        return copied_grid
    
    def reset_attributes(self, size: int, list_values: list[list[str]], list_states: list[list[str]]):
        """
        Met à jour les attributs de la grille, utilisé lors d'un changement de taille de la grille
        """
        
        # Test préconditions
        test_errors(size, list_values = list_values, list_states = list_states)
        
        self.size = size
        self.square_size = int(size ** 0.5)
        self.cells_count = size ** 2        
        
        self.set_content(list_values, list_states)
        
    def get_cell(self, coordinates: tuple[int, int]) -> Cell:
        """
        Renvoi la case de coordonnées (x, y)
        """
        
        test_errors(self.size, coordinates = coordinates)

        return self.content[coordinates[0]][coordinates[1]]
    
    def set_content(self, list_values: list[list[str]], list_states: list[list[str]]):
        """
        Remplace le contenu de la grille par "new content"
        """
        
        test_errors(self.size, list_values = list_values, list_states = list_states)
        
        self.content.clear()
        for x in range(self.size):
            self.content.append([])
            for y in range(self.size):
                cell = Cell(list_values[x][y], list_states[x][y], self.size)
                self.content[x].append(cell)
    
    def get_all_values(self) -> list[list[str]]:
        """
        Renvoie une double liste contenant toutes les valeurs de la grille
        """
        
        return [[cell.value for cell in line] for line in self.content]

    def get_all_states(self) -> list[list[str]]:
        """
        Renvois une double liste contenant toutes les états des cases de la grille
        """
        
        return [[cell.state for cell in line] for line in self.content]
    
    def get_all_coordinates_simple_list(self) -> list[tuple[int, int]]:
        """
        Retourne une liste (simple) de toutes les coordonnées de la grille
        """
        return [(x, y) for x in range(0, self.size) for y in range(0, self.size)]

    def set_cell_value(self, coordinates: tuple[int, int], value: str):
        """
        Met la case de coordonnées (x, y) à la valeur "value"
        """
        
        # Test préconditions
        test_errors(self.size, coordinates = coordinates, value = value)
        
        self.content[coordinates[0]][coordinates[1]].set_value(value)
        
    def get_cell_value(self, coordinates: tuple[int, int]) -> str:
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

        # Test préconditions
        test_errors(boolean = conflicting_state)
        
        self.content[coordinates[0]][coordinates[1]].set_conflicting_state(conflicting_state)
    
    def is_cell_in_conflict(self, coordinates: tuple[int, int]) -> bool:
        """
        Renvois si la case est en conflit avec d'autres ou non
        """
        
        test_errors(self.size, coordinates = coordinates)
        
        x, y = coordinates
        return self.content[x][y].is_in_conflict
    
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
    
    def get_all_values_as(self, format: str) -> list[list[str]]:
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
    
    def get_group_values(self, coordinates: tuple[int, int], format: str) -> list[str]:
        """
        Renvoi la liste des valeurs des cases appartenant au même groupe que la case "coordinates"
        L'argument "format" indique le type de groupe à prendre en compte (ligne, colonne ou carré)
        """
        
        test_errors(self.size, coordinates = coordinates, format = format)
        
        formated_coordinates = self.get_coordinates_as(coordinates, "lines", format)
        
        return [
            self.get_cell_value(self.get_coordinates_as((formated_coordinates[0], y), format, "lines")) for y in range(self.size)
        ]
    
    def get_group_coordinates(self, coordinates: tuple[int, int], format: str) -> list[tuple[int, int]]:
        """
        Renvoi la liste des coordonnées des cases appartenant au même groupe que la case "coordinates"
        l'argument "format" indique le type de groupe à prendre en compte (ligne, colonne ou carré)
        """
        
        test_errors(self.size, coordinates = coordinates, format = format)
        
        formated_coordinates = self.get_coordinates_as(coordinates, "lines", format)
        
        return [self.get_coordinates_as((formated_coordinates[0], y), format, "lines") for y in range(self.size)]
    
    def get_all_empty_cells(self) -> list[tuple[int, int]]:
        """
        Renvoi la liste des coordonnées des cases vides de la grille
        """
        
        all_empty_cells = []
        
        # Pour toutes les cases de la grille
        for y in range(self.size):
            for x in range(self.size):
                coordinates = (x, y)
                
                if self.get_cell_value(coordinates) == '0':  # Si la valeur de la case est zéro
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
                
                if self.get_cell_value(coordinates) == '0':  # Dès qu'une case vide est rencontrée
                    test_errors(self.size, coordinates = coordinates)
                    return (x, y)  # Renvoyer les coordonnées (x, y)
    
    def get_possible_values(self, coordinates: tuple[int, int]) -> list[str]:
        """
        Renvoi les valeurs possibles (de 1 à "self.size") de la case en fonctions des autres chiffres de la même ligne, colomne ou carré
        """
        
        # Test préconditions
        test_errors(self.size, coordinates = coordinates)
        
        possible_values = [digit for digit in self.possible_values[:self.size]]
        
        # Pour tout les formats existants
        for format in ["lines", "columns", "squares"]:
            group = self.get_group_values(coordinates, format)
            
            for cell_value in group:
                if cell_value in possible_values:
                    possible_values.remove(cell_value)
        
        return possible_values
    
    def is_full(self) -> bool:
        """
        Renvoie True si la grille est remplie, et False si elle ne l'est pas
        """
        
        for x in range(self.size):
            for y in range(self.size):
                if self.get_cell_value((x, y)) == "0":
                    return False
        
        return True

    def is_empty(self) -> bool:
        """
        Renvoie True si la grille est vide, et False si elle ne l'est pas
        """
        
        for x in range(self.size):
            for y in range(self.size):
                if self.get_cell_value((x, y)) != "0":
                    return False
        
        return True