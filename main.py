import pygame

pygame.init()

from src.programs.game import Game

# Mise en place de la fenêtre
screen_size = (1080, 720)
pygame.display.set_caption("Sudoku")
screen = pygame.display.set_mode(screen_size, pygame.RESIZABLE)

game = Game(screen)

# Provisoire
game.update()
game.sudoku.load_grid()
#game.sudoku.save_grid()
all_events = pygame.event.get()


while True:
    
    # Récupérer les évènements de la fenêtre
    all_events = pygame.event.get()
    
    # Mettre à jour le jeu
    game.update(all_events)
    
    # Si l'utilisateur ferme la fenêtre
    if game.do_close_window:
        # Arrêter le programme
        pygame.quit()
        break
