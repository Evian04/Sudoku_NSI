import pygame
pygame.init()

from src.programes.game import Game

screen_size = (1080, 720)
pygame.display.set_caption("Sudoku")
screen = pygame.display.set_mode(screen_size)

running = True

while running:
    
    all_events = pygame.event.get()
    
    for event in all_events:
        
        if event.type == pygame.QUIT:
            pygame.quit()
            running = False