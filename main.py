# Import de pygame
import pygame

# Import des autres programmes
from src.programs.game import Game

# Initialisation de pygame
pygame.init()

# Création et initialisation de la fenêtre
screen_size = (1080, 720)  # Dimensions de la fenêtre
screen = pygame.display.set_mode(screen_size, pygame.RESIZABLE)  # Création de la fenêtre

# création de l'instance Game, il s'agit du conteneur du jeu
game = Game(screen)
game.update()

# boucle permettant au jeu de fonctionner, boucle infinie sous condition
while not game.do_quit:
    
    # Limitation à 60 images par seconde
    pygame.time.Clock().tick(60)

    # Si la souris est immobile, ne pas mettre à jour l'affichage du jeu
    do_display = pygame.mouse.get_rel() != (0, 0)

    # Mettre à jour le jeu
    game.update(do_display)

# fermeture de la fenêtre
pygame.quit()
# message console indiquant la fermeture de la fenêtre
print("Program closed")