import pygame
pygame.init()

from src.programs.game import Game

# Mise en place de la fenêtre
screen_size = (1080, 720)
pygame.display.set_caption("Sudoku")
screen = pygame.display.set_mode(screen_size)

game = Game(screen)

running = True
while running:
    
    # Récupérer les évènements de la fenêtre
    all_events = pygame.event.get()
    
    # Mettre à jour le jeu
    game.update(all_events)
    
    for event in all_events:
        
        if event.type == pygame.QUIT:
            # Si l'un des évènements est de fermer la fenêtre, arréter le programme
            pygame.quit()
            running = False