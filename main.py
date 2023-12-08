import pygame

# Initialisation de pygame
pygame.init()

from src.programs.game import Game

# Mise en place de la fenêtre
screen_size = (1080, 720) # Dimensions de la fenêtre
#pygame.display.set_caption("Sudoku") # Nom de la fenêtre
screen = pygame.display.set_mode(screen_size, pygame.RESIZABLE) # Création de la fenêtre

game = Game(screen)

# Provisoire
game.update()
game.sudoku.load_grid()
#game.sudoku.save_grid()
all_events = pygame.event.get()


while True:
    
    # Mettre à jour le jeu
    game.update()
    
    # Si l'utilisateur ferme la fenêtre
    if game.do_quit:
        # Arrêter le programme
        pygame.quit()
        break