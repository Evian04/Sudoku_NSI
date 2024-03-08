import pygame
import os
from tkinter.filedialog import askdirectory

from src.programs.test_errors import test_errors

class Graphism:
    """
    La classe "Graphism" permet de gérer l'affichage des éléments sur la fenêtre
    """
    
    def __init__(self, game, grid_size: int, texture_pack: str, do_display_conflicts: bool):
        self.screen: pygame.Surface = game.screen
        self.game = game
        
        self.grid_size = grid_size
        self.square_size = int(self.grid_size ** 0.5)
        
        self.texture_pack = texture_pack
        self.do_display_conflicts = do_display_conflicts

    def update_grid_attributes(self, size: int):
        """
        met à jour les attributs de la grille, utiliser lors d'un changement de taille de la grille
        """
        self.grid_size = size
        self.square_size = int(self.grid_size ** 0.5)
        self.update_rect()

    def reverse_display_conflicts(self):
        """
        Cette fonction inverse l'état de la variable booléenne "self.do_display_conflicts"
        """
        
        self.do_display_conflicts = not self.do_display_conflicts
    
    def ask_texture_pack(self):
        """
        Ouvre une fenêtre de dialogue pour demander l'emplacement du nouveau pack de texture à utiliser
        """
        
        while True:
            path = askdirectory(initialdir = "src/graphics", title = "Sélectionnez un Pack de Textures")
            
            if not path:
                return
            
            path = path.split("/")[-1]
            
            if not path in os.listdir("src/graphics"):
                print("\nThis isn't a texture pack")
                continue
                
            break
        
        self.texture_pack = path
        self.update_rect()
        return
    
    def display_start_elements(self):
        """
        Affiche les éléments du menu de démarrage
        """
        
        # Affichage du fond d'écran
        self.screen.blit(self.background, self.background_rect)
        
        mouse_pos = pygame.mouse.get_pos()
        
        if self.play_button_rect.collidepoint(mouse_pos):
            self.screen.blit(self.play_selected_button, self.play_button_rect)
        else:
            self.screen.blit(self.play_button, self.play_button_rect)
            
        if self.options_start_button_rect.collidepoint(mouse_pos):
            self.screen.blit(self.options_start_selected_button, self.options_start_button_rect)
        else:
            self.screen.blit(self.options_start_button, self.options_start_button_rect)
        
        if self.quit_button_rect.collidepoint(mouse_pos):
            self.screen.blit(self.quit_selected_button, self.quit_button_rect)
        else:
            self.screen.blit(self.quit_button, self.quit_button_rect)
        
        pygame.display.flip()
    
    def display_game_elements(self):
        """
        Permet d'afficher les élément du menu principal à l'écran
        """
        
        # Affichage du fond d'écran
        self.screen.blit(self.background, self.background_rect)
        
        # Affichage des bouttons
        mouse_pos = pygame.mouse.get_pos()
        
        if not self.game.sudoku.is_history_move_possible("backward"):
            self.screen.blit(self.arrow_left_disabled_button, self.arrow_left_button_rect)
        elif self.arrow_left_button_rect.collidepoint(mouse_pos):
            self.screen.blit(self.arrow_left_selected_button, self.arrow_left_button_rect)
        else:
            self.screen.blit(self.arrow_left_button, self.arrow_left_button_rect)
        
        if self.cross_button_rect.collidepoint(mouse_pos):
            self.screen.blit(self.cross_selected_button, self.cross_button_rect)
        else:
            self.screen.blit(self.cross_button, self.cross_button_rect)
        
        if not self.game.sudoku.is_history_move_possible("forward"):
            self.screen.blit(self.arrow_right_disabled_button, self.arrow_right_button_rect)
        elif self.arrow_right_button_rect.collidepoint(mouse_pos):
            self.screen.blit(self.arrow_right_selected_button, self.arrow_right_button_rect)
        else:
            self.screen.blit(self.arrow_right_button, self.arrow_right_button_rect)
        
        if self.solve_button_rect.collidepoint(mouse_pos):
            self.screen.blit(self.solve_selected_button, self.solve_button_rect)
        else:
            self.screen.blit(self.solve_button, self.solve_button_rect)
        
        if self.save_button_rect.collidepoint(mouse_pos):
            self.screen.blit(self.save_selected_button, self.save_button_rect)
        else:
            self.screen.blit(self.save_button, self.save_button_rect)
        
        if self.open_button_rect.collidepoint(mouse_pos):
            self.screen.blit(self.open_selected_button, self.open_button_rect)
        else:
            self.screen.blit(self.open_button, self.open_button_rect)
        
        if self.options_button_rect.collidepoint(mouse_pos):
            self.screen.blit(self.options_selected_button, self.options_button_rect)
        else:
            self.screen.blit(self.options_button, self.options_button_rect)

        if self.options_button_rect.collidepoint(mouse_pos):
            self.screen.blit(self.return_selected_button, self.return_button_rect)
        else:
            self.screen.blit(self.return_button, self.return_button_rect)
        
        # Affiche l'image de fond de la grille
        self.screen.blit(self.grid_background, self.grid_background_rect)
        
        # Pour toutes les coordonnées de cases
        for x in range(self.grid_size):
            for y in range(self.grid_size):
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
        
        for x in range(self.grid_size):
            for y in range(self.grid_size):
                # affichage du chiffre de chaque case
                self.display_cell_digit((x, y))
                
                # affichage du cadenas si la case est vérouillée
                if self.game.sudoku.grid.get_cell((x, y)).state == "locked":
                    self.screen.blit(self.padlock_image, self.all_cell_rect[x][y])
        
        pygame.display.flip()
    
    def display_options_elements(self):
        """
        Permet d'afficher les élément du menu d'options à l'écran
        """
        
        # Affichage du fond d'écran
        self.screen.blit(self.background, self.background_rect)
        
        # Affichage des bouttons
        
        mouse_pos = pygame.mouse.get_pos()
        
        if self.dimensions_button_rect.collidepoint(mouse_pos):
            self.screen.blit(self.dimensions_selected_button, self.dimensions_button_rect)
        else:
            self.screen.blit(self.dimensions_button, self.dimensions_button_rect)
            
        if self.generate_button_rect.collidepoint(mouse_pos):
            self.screen.blit(self.generate_selected_button, self.generate_button_rect)
        else:
            self.screen.blit(self.generate_button, self.generate_button_rect)
            
        if self.game_mode_button_rect.collidepoint(mouse_pos):
            self.screen.blit(self.game_mode_selected_button, self.game_mode_button_rect)
        else:
            self.screen.blit(self.game_mode_button, self.game_mode_button_rect)
            
        if self.change_textures_button_rect.collidepoint(mouse_pos):
            self.screen.blit(self.change_textures_selected_button, self.change_textures_button_rect)
        else:
            self.screen.blit(self.change_textures_button, self.change_textures_button_rect)
            
        if self.display_errors_button_rect.collidepoint(mouse_pos):
            self.screen.blit(self.display_errors_selected_button, self.display_errors_button_rect)
        else:
            self.screen.blit(self.display_errors_button, self.display_errors_button_rect)
            
        if self.display_solving_button_rect.collidepoint(mouse_pos):
            self.screen.blit(self.display_solving_selected_button, self.display_solving_button_rect)
        else:
            self.screen.blit(self.display_solving_button, self.display_solving_button_rect)
            
        if self.cross_options_button_rect.collidepoint(mouse_pos):
            self.screen.blit(self.cross_selected_options_button, self.cross_options_button_rect)
        else:
            self.screen.blit(self.cross_options_button, self.cross_options_button_rect)
        
        pygame.display.flip()
    
    def display_cell_elements(self, coordinates: tuple[int, int]):
        """
        mise à jour rapide d'une case uniquement, utilisée lors de la résolution
        :param coordinates: coordonnées de la case à mettre à jour
        """
        # Test de préconditions
        test_errors(self.grid_size, coordinates = coordinates)
        
        x, y = coordinates
        
        self.screen.blit(self.cell_image, self.all_cell_rect[x][y])
        
        # Affichage du cadena si la case est "locked"
        if self.game.sudoku.grid.get_cell_state(coordinates) == "locked":
            self.screen.blit(self.padlock_image, self.all_cell_rect[x][y])
        
        # affichage du chiffre de la case
        self.display_cell_digit(coordinates)
        
        pygame.display.flip()
    
    def display_cell_digit(self, coordinates):
        """
        Permet d'afficher un chiffre particulier dans une case
        """
        
        test_errors(self.grid_size, coordinates = coordinates)
        
        digit = self.game.sudoku.grid.get_cell_value(coordinates)
        
        if digit == '0':
            return
        
        if not self.game.sudoku.grid.is_cell_in_conflict(coordinates) or not self.do_display_conflicts:
            digit_image = self.all_digits_image[self.game.possible_values.index(digit)]
        else:
            digit_image = self.all_digits_image[self.game.possible_values.index(digit) + len(self.game.possible_values)]
        x, y = coordinates
        
        self.screen.blit(
            digit_image,
            self.all_cell_rect[x][y]
        )
    
    def update_rect(self):
        """
        Calcule des dimensions et des coordonnées des éléments de la fenêtre
        """
        
        # Test si la longueur de référence doit être la longueur ou la largeur de l'écran
        if self.screen.get_width() * (2 / 3) > self.screen.get_height():
            self.rect_ref_distance = self.screen.get_height()
        
        else:
            self.rect_ref_distance = self.screen.get_width() * (2 / 3)
        
        if self.screen.get_width() > self.screen.get_height():
            background_dimensions = [self.screen.get_width()] * 2
        
        else:
            background_dimensions = [self.screen.get_height()] * 2
            
        self.rect_ref_distance *= 0.9
        self.outline_thickness = self.rect_ref_distance / 30 # Ratio entre la longueur du grand carré et de la marge
        
        self.cell_dimensions = [(self.rect_ref_distance - (self.square_size + 1) * self.outline_thickness) * (1 / self.grid_size)] * 2
        
        self.update_start_buttons_rect()
        self.update_game_buttons_rect()
        self.update_options_buttons_rect()
        self.update_digits_rect()
        
        self.background = pygame.image.load(f"src/graphics/{self.texture_pack}/background.png")
        self.background = pygame.transform.smoothscale(self.background, background_dimensions)
        
        self.background_rect = self.background.get_rect()
        self.background_rect.x = self.screen.get_width() / 2 - background_dimensions[0] / 2
        self.background_rect.y = self.screen.get_height() / 2 - background_dimensions[1] / 2
        
        self.grid_background = pygame.image.load(f"src/graphics/{self.texture_pack}/grid_background.png")
        self.grid_background = pygame.transform.smoothscale(self.grid_background, [self.rect_ref_distance] * 2)
        
        self.grid_background_rect = self.grid_background.get_rect()
        self.grid_background_rect.x = self.screen.get_width() * (1 / 2) - self.rect_ref_distance * (1 / 4)
        self.grid_background_rect.y = self.screen.get_height() * (1 / 2) - self.rect_ref_distance * (1 / 2)
        
        self.cell_image = pygame.image.load(f"src/graphics/{self.texture_pack}/cells/cell.png")
        self.cell_image = pygame.transform.smoothscale(self.cell_image, self.cell_dimensions)
        
        self.superlocked_cell_image = pygame.image.load(f"src/graphics/{self.texture_pack}/cells/superlocked_cell.png")
        self.superlocked_cell_image = pygame.transform.smoothscale(self.superlocked_cell_image, self.cell_dimensions)
        
        self.selected_cell_image = pygame.image.load(f"src/graphics/{self.texture_pack}/cells/selected_cell.png")
        self.selected_cell_image = pygame.transform.smoothscale(self.selected_cell_image, self.cell_dimensions)
        
        self.superlocked_selected_cell_image = pygame.image.load(f"src/graphics/{self.texture_pack}/cells/superlocked_selected_cell.png")
        self.superlocked_selected_cell_image = pygame.transform.smoothscale(self.superlocked_selected_cell_image, self.cell_dimensions)
        
        self.padlock_image = pygame.image.load(f"src/graphics/{self.texture_pack}/cells/padlock.png")
        self.padlock_image = pygame.transform.smoothscale(self.padlock_image, [self.cell_image.get_width() / 2.3] * 2)
        
        self.all_cell_rect = [[
            pygame.Rect([
                self.grid_background_rect.x + self.outline_thickness * (1 + x // self.square_size) + x * self.cell_image.get_width(),
                self.grid_background_rect.y + self.outline_thickness * (1 + y // self.square_size) + y * self.cell_image.get_height(),
                self.cell_image.get_width(),
                self.cell_image.get_height()
            ])
        for y in range(self.grid_size)] for x in range(self.grid_size)]
    
    def update_digits_rect(self):
        self.all_digits_image: list[pygame.Surface] = []
        
        for color in ["regular", "wrong"]:
            
            for i in self.game.possible_values:
                digit_image = pygame.image.load(f"src/graphics/{self.texture_pack}/digits/{i}_{color}.png")
                digit_image = pygame.transform.smoothscale(digit_image, self.cell_dimensions)
                self.all_digits_image.append(digit_image)
    
    def update_dimensions_button_rect(self):
        self.dimensions_button = pygame.image.load(f"src/graphics/{self.texture_pack}/buttons/options/dimensions_{self.grid_size}.png")
        self.dimensions_button = pygame.transform.smoothscale(self.dimensions_button, self.options_buttons_dimensions)
        
        self.dimensions_selected_button = pygame.image.load(f"src/graphics/{self.texture_pack}/buttons/options/dimensions_{self.grid_size}_selected.png")
        self.dimensions_selected_button = pygame.transform.smoothscale(self.dimensions_selected_button, self.options_buttons_dimensions)
    
    def update_game_mode_button_rect(self):
        self.game_mode_button = pygame.image.load(f"src/graphics/{self.texture_pack}/buttons/options/game_mode_{self.game.sudoku.game_mode}.png")
        self.game_mode_button = pygame.transform.smoothscale(self.game_mode_button, self.options_buttons_dimensions)
        
        self.game_mode_selected_button = pygame.image.load(f"src/graphics/{self.texture_pack}/buttons/options/game_mode_{self.game.sudoku.game_mode}_selected.png")
        self.game_mode_selected_button = pygame.transform.smoothscale(self.game_mode_selected_button, self.options_buttons_dimensions)
    
    def update_display_errors_button_rect(self):
        self.display_errors_button = pygame.image.load("src/graphics/{0}/buttons/options/display_errors_{1}.png".format(self.texture_pack, "on" if self.do_display_conflicts else "off"))
        self.display_errors_button = pygame.transform.smoothscale(self.display_errors_button, self.options_buttons_dimensions)
        
        self.display_errors_selected_button = pygame.image.load("src/graphics/{0}/buttons/options/display_errors_{1}_selected.png".format(self.texture_pack, "on" if self.do_display_conflicts else "off"))
        self.display_errors_selected_button = pygame.transform.smoothscale(self.display_errors_selected_button, self.options_buttons_dimensions)
    
    def update_display_solving_button_rect(self):
        self.display_solving_button = pygame.image.load("src/graphics/{0}/buttons/options/display_solving_{1}.png".format(self.texture_pack, "on" if self.game.do_display_during_solving else "off"))
        self.display_solving_button = pygame.transform.smoothscale(self.display_solving_button, self.options_buttons_dimensions)
        
        self.display_solving_selected_button = pygame.image.load("src/graphics/{0}/buttons/options/display_solving_{1}_selected.png".format(self.texture_pack, "on" if self.game.do_display_during_solving else "off"))
        self.display_solving_selected_button = pygame.transform.smoothscale(self.display_solving_selected_button, self.options_buttons_dimensions)
    
    def update_start_buttons_rect(self):
        """
        Calcule les dimensions et les coordonnées des bouttons du menu de démarrage
        """
        
        self.play_button = pygame.image.load(f"src/graphics/{self.texture_pack}/buttons/start/play.png")
        
        self.start_buttons_dimensions = [
            self.rect_ref_distance - self.outline_thickness,
            (self.rect_ref_distance - self.outline_thickness) * (self.play_button.get_height() / self.play_button.get_width())
        ]
        
        ref_coordinates = [
            self.screen.get_width() / 2 - self.start_buttons_dimensions[0] / 2,
            self.screen.get_height() / 2 - self.rect_ref_distance / 2
        ]
        
        buttons_gap = (self.rect_ref_distance - self.start_buttons_dimensions[1]) / 4
        
        self.play_button = pygame.transform.smoothscale(self.play_button, self.start_buttons_dimensions)
        
        self.play_selected_button = pygame.image.load(f"src/graphics/{self.texture_pack}/buttons/start/play_selected.png")
        self.play_selected_button = pygame.transform.smoothscale(self.play_selected_button, self.start_buttons_dimensions)
        
        self.play_button_rect = self.play_button.get_rect()
        self.play_button_rect.x = ref_coordinates[0]
        self.play_button_rect.y = ref_coordinates[1] + buttons_gap
        
        
        self.options_start_button = pygame.image.load(f"src/graphics/{self.texture_pack}/buttons/start/options.png")
        self.options_start_button = pygame.transform.smoothscale(self.options_start_button, self.start_buttons_dimensions)
        
        self.options_start_selected_button = pygame.image.load(f"src/graphics/{self.texture_pack}/buttons/start/options_selected.png")
        self.options_start_selected_button = pygame.transform.smoothscale(self.options_start_selected_button, self.start_buttons_dimensions)
        
        self.options_start_button_rect = self.options_start_button.get_rect()
        self.options_start_button_rect.x = ref_coordinates[0]
        self.options_start_button_rect.y = ref_coordinates[1] + buttons_gap * 2
        
        
        self.quit_button = pygame.image.load(f"src/graphics/{self.texture_pack}/buttons/start/quit.png")
        self.quit_button = pygame.transform.smoothscale(self.quit_button, self.start_buttons_dimensions)
        
        self.quit_selected_button = pygame.image.load(f"src/graphics/{self.texture_pack}/buttons/start/quit_selected.png")
        self.quit_selected_button = pygame.transform.smoothscale(self.quit_selected_button, self.start_buttons_dimensions)
        
        self.quit_button_rect = self.quit_button.get_rect()
        self.quit_button_rect.x = ref_coordinates[0]
        self.quit_button_rect.y = ref_coordinates[1] + buttons_gap * 3
    
    def update_game_buttons_rect(self):
        """
        Calcule les dimensions et les coordonnées des bouttons du menu principal
        """
        
        self.solve_button = pygame.image.load(f"src/graphics/{self.texture_pack}/buttons/game/solve.png")

        self.game_buttons_dimensions = [
            self.rect_ref_distance / 2 - self.outline_thickness,
            (self.rect_ref_distance / 2 - self.outline_thickness) * (self.solve_button.get_height() / self.solve_button.get_width())
        ]
        
        ref_coordinates = [
            self.screen.get_width() / 2 - self.rect_ref_distance * (3 / 4),
            self.screen.get_height() / 2 - self.rect_ref_distance / 2
        ]
        
        buttons_gap = (self.rect_ref_distance - self.game_buttons_dimensions[1]) / 5

        #bouton ouvrir
        self.open_button = pygame.image.load(f"src/graphics/{self.texture_pack}/buttons/game/open.png")
        self.open_button = pygame.transform.smoothscale(self.open_button, self.game_buttons_dimensions)

        self.open_selected_button = pygame.image.load(
            f"src/graphics/{self.texture_pack}/buttons/game/open_selected.png")
        self.open_selected_button = pygame.transform.smoothscale(self.open_selected_button,
                                                                 self.game_buttons_dimensions)

        self.open_button_rect = self.open_button.get_rect()
        self.open_button_rect.x = ref_coordinates[0]
        self.open_button_rect.y = ref_coordinates[1] + buttons_gap * 3

        # bouton sauvegarder
        self.save_button = pygame.image.load(f"src/graphics/{self.texture_pack}/buttons/game/save.png")
        self.save_button = pygame.transform.smoothscale(self.save_button, self.game_buttons_dimensions)

        self.save_selected_button = pygame.image.load(
            f"src/graphics/{self.texture_pack}/buttons/game/save_selected.png")
        self.save_selected_button = pygame.transform.smoothscale(self.save_selected_button,
                                                                 self.game_buttons_dimensions)

        self.save_button_rect = self.save_button.get_rect()
        self.save_button_rect.x = ref_coordinates[0]
        self.save_button_rect.y = ref_coordinates[1] + buttons_gap * 2


        # bouton résoudre
        self.solve_button = pygame.transform.smoothscale(self.solve_button, self.game_buttons_dimensions)
        
        self.solve_selected_button = pygame.image.load(f"src/graphics/{self.texture_pack}/buttons/game/solve_selected.png")
        self.solve_selected_button = pygame.transform.smoothscale(self.solve_selected_button, self.game_buttons_dimensions)
        
        self.solve_button_rect = self.solve_button.get_rect()
        self.solve_button_rect.x = ref_coordinates[0]
        self.solve_button_rect.y = ref_coordinates[1] + buttons_gap
        
        # bouton options
        self.options_button = pygame.image.load(f"src/graphics/{self.texture_pack}/buttons/game/options.png")
        self.options_button = pygame.transform.smoothscale(self.options_button, self.game_buttons_dimensions)
        
        self.options_selected_button = pygame.image.load(f"src/graphics/{self.texture_pack}/buttons/game/options_selected.png")
        self.options_selected_button = pygame.transform.smoothscale(self.options_selected_button, self.game_buttons_dimensions)
        
        self.options_button_rect = self.options_button.get_rect()
        self.options_button_rect.x = ref_coordinates[0]
        self.options_button_rect.y = ref_coordinates[1] + buttons_gap * 4
        
        
        self.return_button = pygame.image.load(f"src/graphics/{self.texture_pack}/buttons/game/return.png")
        self.return_button = pygame.transform.smoothscale(self.return_button, self.game_buttons_dimensions)
        
        self.return_selected_button = pygame.image.load(f"src/graphics/{self.texture_pack}/buttons/game/return_selected.png")
        self.return_selected_button = pygame.transform.smoothscale(self.return_selected_button, self.game_buttons_dimensions)
        
        self.return_button_rect = self.return_button.get_rect()
        self.return_button_rect.x = ref_coordinates[0]
        self.return_button_rect.y = ref_coordinates[1] + buttons_gap * 5
        
        # bouton annuler
        self.arrow_left_button = pygame.image.load(f"src/graphics/{self.texture_pack}/buttons/game/arrow_left.png")
        self.arrow_left_button = pygame.transform.smoothscale(self.arrow_left_button, [self.game_buttons_dimensions[1]] * 2)
        
        self.arrow_left_selected_button = pygame.image.load(f"src/graphics/{self.texture_pack}/buttons/game/arrow_left_selected.png")
        self.arrow_left_selected_button = pygame.transform.smoothscale(self.arrow_left_selected_button, [self.game_buttons_dimensions[1]] * 2)
        
        self.arrow_left_disabled_button = pygame.image.load(f"src/graphics/{self.texture_pack}/buttons/game/arrow_left_disabled.png")
        self.arrow_left_disabled_button = pygame.transform.smoothscale(self.arrow_left_disabled_button, [self.game_buttons_dimensions[1]] * 2)
        
        self.arrow_left_button_rect = self.arrow_left_button.get_rect()
        self.arrow_left_button_rect.x = ref_coordinates[0]
        self.arrow_left_button_rect.y = ref_coordinates[1]
        
        # bouton croix, vide la grille
        self.cross_button = pygame.image.load(f"src/graphics/{self.texture_pack}/buttons/game/cross.png")
        self.cross_button = pygame.transform.smoothscale(self.cross_button, [self.game_buttons_dimensions[1]] * 2)
        
        self.cross_selected_button = pygame.image.load(f"src/graphics/{self.texture_pack}/buttons/game/cross_selected.png")
        self.cross_selected_button = pygame.transform.smoothscale(self.cross_selected_button, [self.game_buttons_dimensions[1]] * 2)
        
        self.cross_button_rect = self.cross_button.get_rect()
        self.cross_button_rect.x = ref_coordinates[0] + self.game_buttons_dimensions[0] / 2 - self.game_buttons_dimensions[1] / 2
        self.cross_button_rect.y = ref_coordinates[1]

        # boutn rétablir
        self.arrow_right_button = pygame.image.load(f"src/graphics/{self.texture_pack}/buttons/game/arrow_right.png")
        self.arrow_right_button = pygame.transform.smoothscale(self.arrow_right_button, [self.game_buttons_dimensions[1]] * 2)
        
        self.arrow_right_selected_button = pygame.image.load(f"src/graphics/{self.texture_pack}/buttons/game/arrow_right_selected.png")
        self.arrow_right_selected_button = pygame.transform.smoothscale(self.arrow_right_selected_button, [self.game_buttons_dimensions[1]] * 2)
        
        self.arrow_right_disabled_button = pygame.image.load(f"src/graphics/{self.texture_pack}/buttons/game/arrow_right_disabled.png")
        self.arrow_right_disabled_button = pygame.transform.smoothscale(self.arrow_right_disabled_button, [self.game_buttons_dimensions[1]] * 2)
        
        self.arrow_right_button_rect = self.arrow_right_button.get_rect()
        self.arrow_right_button_rect.x = ref_coordinates[0] + self.game_buttons_dimensions[0] - self.game_buttons_dimensions[1]
        self.arrow_right_button_rect.y = ref_coordinates[1]
    
    def update_options_buttons_rect(self):
        """
        Calcule les dimensions et les coordonnées des bouttons du menu d'options
        """
        
        self.dimensions_button = pygame.image.load(f"src/graphics/{self.texture_pack}/buttons/options/dimensions_{self.grid_size}.png")
        
        self.options_buttons_dimensions = [
            self.rect_ref_distance - self.outline_thickness,
            (self.rect_ref_distance - self.outline_thickness) * self.dimensions_button.get_height() / self.dimensions_button.get_width()
        ]
        
        ref_coordinates = [
            self.screen.get_width() / 2 - self.options_buttons_dimensions[0] / 2,
            self.screen.get_height() / 2 - self.rect_ref_distance / 2
        ]
        
        buttons_gap = (self.rect_ref_distance - self.options_buttons_dimensions[1]) / 5
        
        self.dimensions_button = pygame.transform.smoothscale(self.dimensions_button, self.options_buttons_dimensions)
        
        self.dimensions_selected_button = pygame.image.load(f"src/graphics/{self.texture_pack}/buttons/options/dimensions_{self.grid_size}_selected.png")
        self.dimensions_selected_button = pygame.transform.smoothscale(self.dimensions_selected_button, self.options_buttons_dimensions)
        
        self.dimensions_button_rect = self.dimensions_button.get_rect()
        self.dimensions_button_rect.x = ref_coordinates[0]
        self.dimensions_button_rect.y = ref_coordinates[1]
        
        
        self.generate_button = pygame.image.load(f"src/graphics/{self.texture_pack}/buttons/options/generate.png")
        self.generate_button = pygame.transform.smoothscale(self.generate_button, self.options_buttons_dimensions)
        
        self.generate_selected_button = pygame.image.load(f"src/graphics/{self.texture_pack}/buttons/options/generate_selected.png")
        self.generate_selected_button = pygame.transform.smoothscale(self.generate_selected_button, self.options_buttons_dimensions)
        
        self.generate_button_rect = self.generate_button.get_rect()
        self.generate_button_rect.x = ref_coordinates[0]
        self.generate_button_rect.y = ref_coordinates[1] + buttons_gap
        
        
        self.game_mode_button = pygame.image.load(f"src/graphics/{self.texture_pack}/buttons/options/game_mode_{self.game.sudoku.game_mode}.png")
        self.game_mode_button = pygame.transform.smoothscale(self.game_mode_button, self.options_buttons_dimensions)
        
        self.game_mode_selected_button = pygame.image.load(f"src/graphics/{self.texture_pack}/buttons/options/game_mode_{self.game.sudoku.game_mode}_selected.png")
        self.game_mode_selected_button = pygame.transform.smoothscale(self.game_mode_selected_button, self.options_buttons_dimensions)
        
        self.game_mode_button_rect = self.game_mode_button.get_rect()
        self.game_mode_button_rect.x = ref_coordinates[0]
        self.game_mode_button_rect.y = ref_coordinates[1] + buttons_gap * 2
        
        
        self.change_textures_button = pygame.image.load(f"src/graphics/{self.texture_pack}/buttons/options/change_textures.png")
        self.change_textures_button = pygame.transform.smoothscale(self.change_textures_button, self.options_buttons_dimensions)
        
        self.change_textures_selected_button = pygame.image.load(f"src/graphics/{self.texture_pack}/buttons/options/change_textures_selected.png")
        self.change_textures_selected_button = pygame.transform.smoothscale(self.change_textures_selected_button, self.options_buttons_dimensions)
        
        self.change_textures_button_rect = self.change_textures_button.get_rect()
        self.change_textures_button_rect.x = ref_coordinates[0]
        self.change_textures_button_rect.y = ref_coordinates[1] + buttons_gap * 3
        
        
        self.display_errors_button = pygame.image.load("src/graphics/{0}/buttons/options/display_errors_{1}.png".format(self.texture_pack, "on" if self.do_display_conflicts else "off"))
        self.display_errors_button = pygame.transform.smoothscale(self.display_errors_button, self.options_buttons_dimensions)
        
        self.display_errors_selected_button = pygame.image.load("src/graphics/{0}/buttons/options/display_errors_{1}_selected.png".format(self.texture_pack, "on" if self.do_display_conflicts else "off"))
        self.display_errors_selected_button = pygame.transform.smoothscale(self.display_errors_selected_button, self.options_buttons_dimensions)
        
        self.display_errors_button_rect = self.display_errors_button.get_rect()
        self.display_errors_button_rect.x = ref_coordinates[0]
        self.display_errors_button_rect.y = ref_coordinates[1] + buttons_gap * 4
        
        
        self.display_solving_button = pygame.image.load("src/graphics/{0}/buttons/options/display_solving_{1}.png".format(self.texture_pack, "on" if self.game.do_display_during_solving else "off"))
        self.display_solving_button = pygame.transform.smoothscale(self.display_solving_button, self.options_buttons_dimensions)
        
        self.display_solving_selected_button = pygame.image.load("src/graphics/{0}/buttons/options/display_solving_{1}_selected.png".format(self.texture_pack, "on" if self.game.do_display_during_solving else "off"))
        self.display_solving_selected_button = pygame.transform.smoothscale(self.display_solving_selected_button, self.options_buttons_dimensions)
        
        self.display_solving_button_rect = self.display_solving_button.get_rect()
        self.display_solving_button_rect.x = ref_coordinates[0]
        self.display_solving_button_rect.y = ref_coordinates[1] + buttons_gap * 5
        
        
        self.cross_options_button = pygame.image.load(f"src/graphics/{self.texture_pack}/buttons/options/cross.png")
        self.cross_options_button = pygame.transform.smoothscale(self.cross_options_button, [self.options_buttons_dimensions[1] * (2 / 3)] * 2)
        
        self.cross_selected_options_button = pygame.image.load(f"src/graphics/{self.texture_pack}/buttons/options/cross_selected.png")
        self.cross_selected_options_button = pygame.transform.smoothscale(self.cross_selected_options_button, [self.options_buttons_dimensions[1] * (2/3)] * 2)
        
        self.cross_options_button_rect = self.cross_options_button.get_rect()
        self.cross_options_button_rect.x = self.outline_thickness * 2
        self.cross_options_button_rect.y = ref_coordinates[1] * (4/3)