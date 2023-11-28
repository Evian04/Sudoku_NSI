import pygame.font

from src.programs.test_errors import test_errors

class Text:
    
    """
    /!\ PROVISOIR (le temps qu'on ait les textures pour les chiffres)
    """
    
    def __init__(self, text: str = str(), font_name: str = 'Arial', font_size: int = 30, color: tuple[int, int, int] = (0, 0, 0)):
        
        if type(text) != str:
            raise TypeError(f"The `text` argument must be a string (type : {type(text)})")
        
        if type(font_name) != str:
            raise TypeError(f"The `font_name` argument must be a string (type : {type(font_name)})")
        
        if type(font_size) != int:
            raise TypeError(f"The `font_size` argument must be an integer (type : {type(font_size)})")
        
        test_errors(col = color)
        
        self.font = None  # défini par self.set_font()
        self.text_label = None  # défini par self.set_text()
        self.text: str = str()
        self.font_name = font_name
        self.font_size: int = font_size
        self.color = color
        self.update_font()  # créé la police (self.font)
        self.set_text(text)  # créé l'image du texte
    
    def set_font_size(self, font_size: int):
        """
        défini la taille de la police
        :param font_size: taille de la police (pixel de hauteur)
        """
        
        if type(font_size) != int:
            raise TypeError(f"The `font_size` argument must be an integer (type : {type(font_size)})")
        
        self.font_size = font_size
        self.update_font()  # redefini la police apres modification de la taille
        
    def set_font_name(self, font_name: str):
        """
        créé l'objet font de pygame
        :param font_name: nom de la police (police du système: 'Calibri', 'Arial', ect)
        """
        
        if type(font_name) != str:
            raise TypeError(f"The `font_type` argument must be a string (type : {type(font_name)})")
        
        self.font_name = font_name
        self.update_font()
    
    def update_font(self):
        self.font = pygame.font.SysFont(self.font_name, self.font_size)  # création d'une police pour afficher du texte
        self.update_label()
        
    def set_color(self, color: tuple[int, int, int]):
        """
        défini la couleur du texte
        :param color: couleur (valeurs RGB)
        """
        
        if type(color) != tuple:
            raise TypeError(f"The `color` argument must be a tuple (type : {type(color)})")
        
        if len(color) != 3:
            raise ValueError(f"The `color` argument must have a length of 3 (length : {len(color)})")
        
        self.color = color
        self.update_label()
        
    def set_text(self, text: str):
        """
        Permet de créer un texte pour afficher la valeur de la cellule
        :param text: texte à afficher
        """
        
        if type(self.text) != str:
            raise TypeError(f"The `text` argument must be a string (type : {type(self.text)})")
        
        self.text = text
        self.update_label()
    
    def update_label(self):
        self.text_label = self.font.render(self.text, True, self.color)  # création du texte (self.text est une Surface)
    
    def get_text(self):
        """
        donne l'objet Text
        :return: Objet pygame.Surface
        """
        return self.text_label
