from tkinter.filedialog import askopenfilename

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
        Renvois la valeur de la case de coordonnées (x, y)
        """
        
        if type(x) != int:
            raise TypeError(f"Grid.get_cell() : The `x` argument must be an intger (type : {type(x)})")
        
        if type(y) != int:
            raise TypeError(f"Grid.get_cell() : The `y` argument must be an intger (type : {type(y)})")
        
        if x < 0 or x >= 9:
            raise ValueError(f"Grid.get_cell() : The `x` argument must be between 0 and 8 (value : {x})")
        
        if y < 0 or y >= 9:
            raise ValueError(f"Grid.get_cell() : The `y` argument must be between 0 and 8 (value : {y})")
        
        return self.content[x][y].get_value()
    
    def set_content(self, new_content: list[list[str]]):
        """
        Remplace le contenu de la grille par `new content`
        """
        
        if type(new_content) != list:
            raise TypeError(f"Grid.set_content() : The `new_content` argument must be a list (type : {type(new_content)})")
        
        if len(new_content) != 9:
            raise ValueError(f"Grid.set_content() : The `new_content` argument must have a length of 9 (length : {len(new_content)})")
        
        self.content = new_content
    
    def set_cell(self, x: int, y: int, value: int):
        """
        Met la case de coordonnées (x, y) à la valeur `value`
        """
        
        if type(x) != int:
            raise TypeError(f"Grid.set_cell() : The `x` argument must be an intger (type : {type(x)})")
        
        if type(y) != int:
            raise TypeError(f"Grid.set_cell() : The `y` argument must be an intger (type : {type(y)})")
        
        if type(value) != str:
            raise TypeError(f"Grid.set_cell() : The `value` argument must be a string (type : {type(value)})")
        
        if x < 0 or x >= 9:
            raise ValueError(f"Grid.set_cell() : The `x` argument must be between 0 and 8 (value : {x})")
        
        if y < 0 or y >= 9:
            raise ValueError(f"Grid.set_cell() : The `y` argument must be between 0 and 8 (value : {y})")
        
        if not value.isdigit() or int(value) > 0 or int(value) < 9:
            raise ValueError(f"Grid.set_cell() : The `value` argument must contains a integer between 0 and 9 (value : {value})")
        
        self.content[x][y].put_value(value)
