import pygame
from src.programs.test_errors import test_errors

class Graphism:
    
    def __init__(self, game, background_color: tuple[int, int, int]):
        self.screen = game.screen
        self.game = game
        
        self.background_color = background_color
    
    def display_elements(self):
        """
        Permet de placer les éléments à afficher sur le brouillon de l'écran
        """
        
        # Affichage du fond d'écran
        pygame.draw.rect(self.screen, self.background_color, self.screen.get_rect())
        
        # Affiche les contours de la grille
        self.screen.blit(self.outline_image, self.outline_rect)
        
        # Pour toutes les coordonnées de cases
        for x in range(self.game.sudoku.grid.size):
            for y in range(self.game.sudoku.grid.size):
                rect = self.all_cell_rect[x][y]
                
                if self.game.sudoku.grid.get_cell_state((x, y)) != "superlocked" and (x, y) != self.game.sudoku.selected_cell:
                    # affichage d'une case normale
                    self.screen.blit(self.cell_image, rect)
                
                elif self.game.sudoku.grid.get_cell_state((x, y)) != "superlocked" and (x, y) == self.game.sudoku.selected_cell:
                    # Affichage d'une case sélectionnée
                    self.screen.blit(self.selected_cell_image, rect)
                
                elif self.game.sudoku.grid.get_cell_state((x, y)) == "superlocked" and (x, y) != self.game.sudoku.selected_cell:
                    # Affichage d'une case superlocked
                    self.screen.blit(self.superlocked_cell_image, rect)
                
                else:
                    # Affichage d'une case superlocked et sélectionnée
                    self.screen.blit(self.superlocked_selected_cell_image, rect)
        
        for x in range(self.game.sudoku.grid.size):
            for y in range(self.game.sudoku.grid.size):
                # affichage case locked (affichage du cadenas)
                if self.game.sudoku.grid.get_cell((x, y)).state == "locked":  # affichage des cases verrouillées
                    self.screen.blit(self.padlock_image, self.all_cell_rect[x][y])
                
                # affichage du texte (numéro) pour chaque cellule
                text = self.game.sudoku.grid.get_cell((x, y)).text.get_text()
                self.screen.blit(
                    text,
                    [
                        self.all_cell_rect[x][y].center[0] - text.get_width() / 2,
                        self.all_cell_rect[x][y].center[1] - text.get_height() / 2,
                        self.all_cell_rect[x][y].width,
                        self.all_cell_rect[x][y].height
                    ]
                )
    
    def cell_display_element(self, coordinates: tuple[int, int]):
        """
        mise à jour rapide d'une cellule uniquement, utilisée lors de la résolution
        :param coordinates: coordonnées de la cellule à mettre à jour
        """
        # Test de préconditions
        test_errors(coordinates=coordinates)
        
        x, y = coordinates
        
        self.screen.blit(self.cell_image, self.all_cell_rect[x][y])
        
        # Affichage du cadena si la case est "locked"
        if self.game.sudoku.grid.get_cell_state((x, y)) == "locked":
            self.screen.blit(self.padlock_image, self.all_cell_rect[x][y])
        
        # affichage du texte (numéro) de la cellule
        text = self.game.sudoku.grid.get_cell((x, y)).text.get_text()
        self.screen.blit(
            text,
            [
                self.all_cell_rect[x][y].center[0] - text.get_width() / 2,
                self.all_cell_rect[x][y].center[1] - text.get_height() / 2,
                self.all_cell_rect[x][y].width,
                self.all_cell_rect[x][y].height
            ]
        )
    
    def update_rect(self):
        """
        Calcule de la dimensions et des coordonnées des éléments de la fenêtre
        """
        
        # Test si la longueur de référence doit être la longueur ou la largeur de l'écran
        if self.screen.get_width() * (2 / 3) > self.screen.get_height():
            self.rect_ref_distance = self.screen.get_height()
        
        else:
            self.rect_ref_distance = self.screen.get_width() * (2 / 3)
        
        self.outline_thickness = self.rect_ref_distance / 28 # 28 est le ratio entre la longueur du grand carré et de la marge
        
        self.update_buttons_rect()
        
        self.outline_image = pygame.image.load("src/graphics/outline.png")
        self.outline_image = pygame.transform.scale(self.outline_image, [self.rect_ref_distance] * 2)
        
        self.outline_rect = self.outline_image.get_rect()
        self.outline_rect.x = self.screen.get_width() * (1 / 2) - self.rect_ref_distance * (1 / 4)
        self.outline_rect.y = self.screen.get_height() * (1 / 2) - self.rect_ref_distance * (1 / 2)
        
        cell_dimensions = [(self.rect_ref_distance - 4 * self.outline_thickness) * (1 / self.game.sudoku.grid.size)] * 2
        
        self.cell_image = pygame.image.load("src/graphics/cell.png")
        self.cell_image = pygame.transform.scale(self.cell_image, cell_dimensions)
        
        self.superlocked_cell_image = pygame.image.load("src/graphics/superlocked_cell.png")
        self.superlocked_cell_image = pygame.transform.scale(self.superlocked_cell_image, cell_dimensions)
        
        self.selected_cell_image = pygame.image.load("src/graphics/selected_cell.png")
        self.selected_cell_image = pygame.transform.scale(self.selected_cell_image, cell_dimensions)
        
        self.superlocked_selected_cell_image = pygame.image.load("src/graphics/superlocked_selected_cell.png")
        self.superlocked_selected_cell_image = pygame.transform.scale(self.superlocked_selected_cell_image, cell_dimensions)
        
        self.padlock_image = pygame.image.load("src/graphics/padlock.png")
        self.padlock_image = pygame.transform.scale(self.padlock_image, [self.cell_image.get_width() / 6] * 2)
        
        self.all_cell_rect = [[
            pygame.Rect([
                self.outline_rect.x + self.outline_thickness * (1 + x // 3) + x * self.cell_image.get_width(),
                self.outline_rect.y + self.outline_thickness * (1 + y // 3) + y * self.cell_image.get_height(),
                self.cell_image.get_width(),
                self.cell_image.get_height()
            ])
        for y in range(self.game.sudoku.grid.size)] for x in range(self.game.sudoku.grid.size)]
        
        # recalcule et réattribue les valeurs de la taille des textes
        for x in range(self.game.sudoku.grid.size):
            for y in range(self.game.sudoku.grid.size):
                self.game.sudoku.grid.get_cell((x, y)).text.set_font_size(round(0.375 * self.all_cell_rect[x][y].height))
                # 0.375 est le rapport entre la taille d'un carré et la taille de la police
                # /!\ Méthode provisoire, le text sera remplacé par des images
    
    def update_buttons_rect(self):
        """
        Calcule les dimensions et les coordonnées des éléments de la fenêtre
        """
        
        self.verification_button = pygame.image.load("src/graphics/buttons/verification_{}.png".format("on" if self.game.sudoku.do_display_conflicts else "off"))
        
        buttons_dimensions = [
            self.rect_ref_distance * (1 / 2) - self.outline_thickness,
            (self.rect_ref_distance * (1 / 2) - self.outline_thickness) * (self.verification_button.get_height() / self.verification_button.get_width())
        ]
        
        buttons_ref_coordinates = [
            self.screen.get_width() * (1 / 2) - self.rect_ref_distance * (3 / 4),
            self.screen.get_height() * (1 / 2) - self.rect_ref_distance * (1 / 2)
        ]
        
        buttons_gap = (self.rect_ref_distance - buttons_dimensions[1]) / 4
        
        self.verification_button = pygame.transform.scale(self.verification_button, buttons_dimensions)
        
        self.verification_button_rect = self.verification_button.get_rect()
        self.verification_button_rect.x = buttons_ref_coordinates[0]
        self.verification_button_rect.y = buttons_ref_coordinates[1]
        
        self.solve_button = pygame.image.load("src/graphics/buttons/solve.png")
        self.solve_button = pygame.transform.scale(self.solve_button, buttons_dimensions)
        
        self.solve_button_rect = self.solve_button.get_rect()
        self.solve_button_rect.x = buttons_ref_coordinates[0]
        self.solve_button_rect.y = buttons_ref_coordinates[1] + buttons_gap
        
        self.generate_button = pygame.image.load("src/graphics/buttons/generate.png")
        self.generate_button = pygame.transform.scale(self.generate_button, buttons_dimensions)
        
        self.generate_button_rect = self.generate_button.get_rect()
        self.generate_button_rect.x = buttons_ref_coordinates[0]
        self.generate_button_rect.y = buttons_ref_coordinates[1] + 2 * buttons_gap
        
        self.open_button = pygame.image.load("src/graphics/buttons/open.png")
        self.open_button = pygame.transform.scale(self.open_button, buttons_dimensions)
        
        self.open_button_rect = self.open_button.get_rect()
        self.open_button_rect.x = buttons_ref_coordinates[0]
        self.open_button_rect.y = buttons_ref_coordinates[1] + 3 * buttons_gap
        
        self.save_button = pygame.image.load("src/graphics/buttons/save.png")
        self.save_button = pygame.transform.scale(self.save_button, buttons_dimensions)
        
        self.save_button_rect = self.save_button.get_rect()
        self.save_button_rect.x = buttons_ref_coordinates[0]
        self.save_button_rect.y = buttons_ref_coordinates[1] + 4 * buttons_gap