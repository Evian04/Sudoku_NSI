import pygame

# Initialisation de pygame
pygame.init()

from src.programs.game import Game
from src.programs.options import sudoku_size

# Mise en place de la fenêtre
screen_size = (1080, 720) # Dimensions de la fenêtre
#pygame.display.set_caption("Sudoku") # Nom de la fenêtre
screen = pygame.display.set_mode(screen_size, pygame.RESIZABLE) # Création de la fenêtre


game = Game(screen, sudoku_size)

# Provisoire
game.update()
game.sudoku.load_grid()
#game.sudoku.save_grid()


while True:
    
    # Mettre à jour le jeu
    game.update()
    
    # Si l'utilisateur ferme la fenêtre
    if game.do_quit:
        # Arrêter le programme
        pygame.quit()
        break