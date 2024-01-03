import pygame
from src.programs.test_errors import test_errors

class Graphism:
    """
    La classe "Graphism" permet de gérer l'affichage des éléments sur la fenêtre
    """
    
    def __init__(self, game, background_color: tuple[int, int, int]):
        self.screen: pygame.Surface = game.screen
        self.game = game
        
        self.do_display_conflicts = True
        
        self.background_color = background_color
    
    def reverse_display_conflicts(self):
        """
        Cette fonction inverse l'état de la variable booléenne "self.do_display_conflicts"
        """
        
        self.do_display_conflicts = not self.do_display_conflicts
    
    def display_elements(self):
        """
        Permet de placer les éléments à afficher sur l'écran
        """
        
        # Affichage du fond d'écran
        pygame.draw.rect(self.screen, self.background_color, self.screen.get_rect())
        
        # Affichage des bouttons
        self.screen.blit(self.verification_button, self.verification_button_rect)
        self.screen.blit(self.solve_button, self.solve_button_rect)
        self.screen.blit(self.generate_button, self.generate_button_rect)
        self.screen.blit(self.open_button, self.open_button_rect)
        self.screen.blit(self.save_button, self.save_button_rect)
        
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
                
                # affichage du chiffre de chaque case
                self.display_cell_digit((x, y))
    
    def cell_display_element(self, coordinates: tuple[int, int]):
        """
        mise à jour rapide d'une case uniquement, utilisée lors de la résolution
        :param coordinates: coordonnées de la case à mettre à jour
        """
        # Test de préconditions
        test_errors(self.game.sudoku.grid.size, coordinates = coordinates)
        
        x, y = coordinates
        
        self.screen.blit(self.cell_image, self.all_cell_rect[x][y])
        
        # Affichage du cadena si la case est "locked"
        if self.game.sudoku.grid.get_cell_state(coordinates) == "locked":
            self.screen.blit(self.padlock_image, self.all_cell_rect[x][y])
        
        # affichage du chiffre de la case
        self.display_cell_digit(coordinates)
    
    def display_cell_digit(self, coordinates):
        """
        Permet d'afficher un chiffre particulier dans une case
        """
        
        test_errors(self.game.sudoku.grid.size, coordinates = coordinates)
        
        digit = self.game.sudoku.grid.get_cell_value(coordinates)
        
        if digit == 0:
            return
        
        if not self.game.sudoku.grid.is_cell_in_conflict(coordinates) or not self.do_display_conflicts:
            digit_image = self.all_digits_image[digit - 1]
            
        else:
            digit_image = self.all_digits_image[digit + 8]
        
        x, y = coordinates
        
        self.screen.blit(
            digit_image,
            self.all_cell_rect[x][y]
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
            
        self.rect_ref_distance *= 0.9
        self.outline_thickness = self.rect_ref_distance / 28 # 28 est le ratio entre la longueur du grand carré et de la marge
        
        self.cell_dimensions = [(self.rect_ref_distance - 4 * self.outline_thickness) * (1 / self.game.sudoku.grid.size)] * 2
        
        self.update_buttons_rect()
        self.update_digits_rect()
        
        self.outline_image = pygame.image.load("src/graphics/outline.png")
        self.outline_image = pygame.transform.scale(self.outline_image, [self.rect_ref_distance] * 2)
        
        self.outline_rect = self.outline_image.get_rect()
        self.outline_rect.x = self.screen.get_width() * (1 / 2) - self.rect_ref_distance * (1 / 4)
        self.outline_rect.y = self.screen.get_height() * (1 / 2) - self.rect_ref_distance * (1 / 2)
        
        self.cell_image = pygame.image.load("src/graphics/cell.png")
        self.cell_image = pygame.transform.scale(self.cell_image, self.cell_dimensions)
        
        self.superlocked_cell_image = pygame.image.load("src/graphics/superlocked_cell.png")
        self.superlocked_cell_image = pygame.transform.scale(self.superlocked_cell_image, self.cell_dimensions)
        
        self.selected_cell_image = pygame.image.load("src/graphics/selected_cell.png")
        self.selected_cell_image = pygame.transform.scale(self.selected_cell_image, self.cell_dimensions)
        
        self.superlocked_selected_cell_image = pygame.image.load("src/graphics/superlocked_selected_cell.png")
        self.superlocked_selected_cell_image = pygame.transform.scale(self.superlocked_selected_cell_image, self.cell_dimensions)
        
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
    
    def update_digits_rect(self):
        self.all_digits_image: list[pygame.Surface] = []
        
        for color in ["black", "red"]:
            for i in range(1, 10):
                digit_image = pygame.image.load(f"src/graphics/digits/{i}_{color}.png")
                digit_image = pygame.transform.scale(digit_image, self.cell_dimensions)
                self.all_digits_image.append(digit_image)
    
    def update_buttons_rect(self):
        """
        Calcule les dimensions et les coordonnées des éléments de la fenêtre
        """
        
        self.verification_button = pygame.image.load("src/graphics/buttons/verification_{}.png".format("on" if self.do_display_conflicts else "off"))
        
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