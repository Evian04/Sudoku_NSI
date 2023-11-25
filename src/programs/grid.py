from src.programs.cell import Cell


class Grid:
    """
    La class `Grid` permet de stocker et de gérer le contenu de la grille du sudoku
    """
    
    def __init__(self, content: list[list[Cell]] = list()):
        if content:
            # Si le contenu du sudoku est précisé, sauvegarder ce contenu
            self.content = content.copy()
        
        else:
            # Sinon créer une grille vierge
            self.content = [[Cell(0, "unlocked") for y in range(9)] for x in range(9)]
    
    def get_cell_value(self, x: int, y: int) -> int:
        """
        Renvoi la valeur de la case de coordonnées (x, y)
        """
        
        if type(x) != int:
            raise TypeError(f"The `x` argument must be an intger (type : {type(x)})")
        
        if type(y) != int:
            raise TypeError(f"The `y` argument must be an intger (type : {type(y)})")
        
        if x < 0 or x >= 9:
            raise ValueError(f"The `x` argument must be between 0 and 8 (value : {x})")
        
        if y < 0 or y >= 9:
            raise ValueError(f"The `y` argument must be between 0 and 8 (value : {y})")
        
        return self.content[x][y].get_value()
    
    def get_cell_state(self, x: int, y: int) -> str:
        """
        Renvoi la valeur de la case de coordonnées (x, y)
        """
        
        if type(x) != int:
            raise TypeError(f"The `x` argument must be an intger (type : {type(x)})")
        
        if type(y) != int:
            raise TypeError(f"The `y` argument must be an intger (type : {type(y)})")
        
        if x < 0 or x >= 9:
            raise ValueError(f"The `x` argument must be between 0 and 8 (value : {x})")
        
        if y < 0 or y >= 9:
            raise ValueError(f"The `y` argument must be between 0 and 8 (value : {y})")
        
        return self.content[x][y].get_state()
    
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
    
    def set_cell_value(self, x: int, y: int, value: int):
        """
        Met la case de coordonnées (x, y) à la valeur `value`
        """
        
        if type(x) != int:
            raise TypeError(f"The `x` argument must be an integer (type : {type(x)})")
        
        if type(y) != int:
            raise TypeError(f"The `y` argument must be an integer (type : {type(y)})")
        
        if type(value) != int:
            raise TypeError(f"The `value` argument must be a string (type : {type(value)})")
        
        if x < 0 or x >= 9:
            raise ValueError(f"The `x` argument must be between 0 and 9 (value : {x})")
        
        if y < 0 or y >= 9:
            raise ValueError(f"The `y` argument must be between 0 and 9 (value : {y})")
        
        if int(value) < 0 or int(value) > 9:
            raise ValueError(f"The `value` argument must contains a integer between 0 and 9 (value : {value})")
        
        if self.content[x][y].get_state() == 'unlocked':
            self.content[x][y].put_value(value)
        
        else:
            print(f'Grid.set_cell: cell ({x},{y}) is locked or superlocked')
            
    def set_cell_color(self, x: int, y: int, color: tuple[int, int, int]):
        """
        Met la couleur de la case de coordonnées (x, y) à `color`
        """
        
        if type(x) != int:
            raise TypeError(f"The `x` argument must be an integer (type : {type(x)})")
        
        if type(y) != int:
            raise TypeError(f"The `y` argument must be an integer (type : {type(y)})")
        
        if type(color) != tuple:
            raise TypeError(f"The `color` argument must be a tuple (type : {type(color)})")
        
        if x < 0 or x >= 9:
            raise ValueError(f"The `x` argument must be between 0 and 9 (value : {x})")
        
        if y < 0 or y >= 9:
            raise ValueError(f"The `y` argument must be between 0 and 9 (value : {y})")
        
        if len(color) != 3:
            raise ValueError(f"The `color` argument must have a length of 3 (length : {color})")
        
        self.content[x][y].set_color(color)
    
    def get_all_values(self) -> list[list[int]]:
        """
        Retourne une double liste de toutes les valeurs (identique à self.content, mais remplace les cellules pas les valeurs des cellules)
        :return:
        """
        
        return [[cell.value for cell in line] for line in self.content]
