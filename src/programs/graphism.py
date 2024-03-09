# import des librairies
import pygame
import os
from tkinter.filedialog import askdirectory
from typing import Union
# nos modules
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
            # chemin du texture pack
            path = askdirectory(initialdir="src/graphics", title="Sélectionnez un Pack de Textures")
            
            if not path:
                return
            
            path = path.split("/")[-1]
            
            if not path in os.listdir("src/graphics"):
                print("\nThis isn't a texture pack")
                continue
                
            break
        
        self.texture_pack = path
        # met à jour l'affichage
        self.update_rect()
        #
    
    def display_start_elements(self):
        """
        Affiche les éléments du menu de démarrage
        """
        
        # Affichage du fond d'écran
        self.screen.blit(self.background, self.background_rect)
        
        mouse_pos = pygame.mouse.get_pos()
        
        # bouton jouer
        if self.play_button_rect.collidepoint(mouse_pos):
            self.screen.blit(self.play_selected_button, self.play_button_rect)
        else:
            self.screen.blit(self.play_button, self.play_button_rect)
            
        # bouton options
        if self.options_start_button_rect.collidepoint(mouse_pos):
            self.screen.blit(self.options_start_selected_button, self.options_start_button_rect)
        else:
            self.screen.blit(self.options_start_button, self.options_start_button_rect)
        
        if self.help_button_rect.collidepoint(mouse_pos):
            self.screen.blit(self.help_button, self.help_button_rect)
        else:
            self.screen.blit(self.help_button, self.help_button_rect)
            
        # boutons quitter
        if self.quit_button_rect.collidepoint(mouse_pos):
            self.screen.blit(self.quit_selected_button, self.quit_button_rect)
        else:
            self.screen.blit(self.quit_button, self.quit_button_rect)
        
        pygame.display.flip()
    
    def display_game_elements(self):
        """
        Permet d'afficher les élément du menu principal
        """
        
        # Affichage du fond d'écran
        self.screen.blit(self.background, self.background_rect)
        
        # Affichage des boutons
        mouse_pos = pygame.mouse.get_pos()
        
        # bouton annuler
        if not self.game.sudoku.is_history_move_possible("backward"):
            self.screen.blit(self.arrow_left_disabled_button, self.arrow_left_button_rect)
        elif self.arrow_left_button_rect.collidepoint(mouse_pos):
            self.screen.blit(self.arrow_left_selected_button, self.arrow_left_button_rect)
        else:
            self.screen.blit(self.arrow_left_button, self.arrow_left_button_rect)
        
        # bouton vider la grille
        if self.cross_button_rect.collidepoint(mouse_pos):
            self.screen.blit(self.cross_selected_button, self.cross_button_rect)
        else:
            self.screen.blit(self.cross_button, self.cross_button_rect)
        
        # bouton rétablir
        if not self.game.sudoku.is_history_move_possible("forward"):
            self.screen.blit(self.arrow_right_disabled_button, self.arrow_right_button_rect)
        elif self.arrow_right_button_rect.collidepoint(mouse_pos):
            self.screen.blit(self.arrow_right_selected_button, self.arrow_right_button_rect)
        else:
            self.screen.blit(self.arrow_right_button, self.arrow_right_button_rect)
        
        # bouton ouvrir
        if self.open_button_rect.collidepoint(mouse_pos):
            self.screen.blit(self.open_selected_button, self.open_button_rect)
        else:
            self.screen.blit(self.open_button, self.open_button_rect)

        # bouton enregistrer
        if self.save_button_rect.collidepoint(mouse_pos):
            self.screen.blit(self.save_selected_button, self.save_button_rect)
        else:
            self.screen.blit(self.save_button, self.save_button_rect)
        
        # bouton résoudre
        if self.solve_button_rect.collidepoint(mouse_pos):
            self.screen.blit(self.solve_selected_button, self.solve_button_rect)
        else:
            self.screen.blit(self.solve_button, self.solve_button_rect)
      
        # bouton options
        if self.options_button_rect.collidepoint(mouse_pos):
            self.screen.blit(self.options_selected_button, self.options_button_rect)
        else:
            self.screen.blit(self.options_button, self.options_button_rect)

        if self.return_button_rect.collidepoint(mouse_pos):
            self.screen.blit(self.return_selected_button, self.return_button_rect)
        else:
            self.screen.blit(self.return_button, self.return_button_rect)
        
        # Affiche l'image de fond de la grille
        self.screen.blit(self.grid_background, self.grid_background_rect)
        
        # Pour toutes les coordonnées de cases
        for x in range(self.grid_size):
            for y in range(self.grid_size):
                rect = self.all_cell_rect[x][y]

                # affichage d'une case déverrouillée
                if self.game.sudoku.grid.get_cell_state((x, y)) != "superlocked" and (x, y) != self.game.sudoku.selected_cell:
                    self.screen.blit(self.cell_image, rect)

                # Affichage d'une case sélectionnée
                elif self.game.sudoku.grid.get_cell_state((x, y)) != "superlocked" and (x, y) == self.game.sudoku.selected_cell:
                    self.screen.blit(self.selected_cell_image, rect)

                # Affichage d'une case superlocked
                elif self.game.sudoku.grid.get_cell_state((x, y)) == "superlocked" and (x, y) != self.game.sudoku.selected_cell:
                    self.screen.blit(self.superlocked_cell_image, rect)

                # Affichage d'une case superlocked et sélectionnée
                else:
                    self.screen.blit(self.superlocked_selected_cell_image, rect)

        # affichage du chiffre de chaque case
        for x in range(self.grid_size):
            for y in range(self.grid_size):
                self.display_cell_digit((x, y))
                
                # affichage du cadenas si la case est verrouillée
                if self.game.sudoku.grid.get_cell((x, y)).state == "locked":
                    self.screen.blit(self.padlock_image, self.all_cell_rect[x][y])
        
        # mettre à jour la fenêtre (mise à jour effective des modifications)
        pygame.display.flip()
    
    def display_options_elements(self):
        """
        Permet d'afficher les élément du menu d'options à l'écran
        """
        
        # Affichage du fond d'écran
        self.screen.blit(self.background, self.background_rect)
        
        # Affichage des boutons
        
        mouse_pos = pygame.mouse.get_pos()

        # bouton quitter le menu options
        if self.cross_options_button_rect.collidepoint(mouse_pos):
            self.screen.blit(self.cross_selected_options_button, self.cross_options_button_rect)
        else:
            self.screen.blit(self.cross_options_button, self.cross_options_button_rect)

        # boutons dimension
        if self.dimensions_button_rect.collidepoint(mouse_pos):
            self.screen.blit(self.dimensions_selected_button, self.dimensions_button_rect)
        else:
            self.screen.blit(self.dimensions_button, self.dimensions_button_rect)
            
        # bouton générer
        if self.generate_button_rect.collidepoint(mouse_pos):
            self.screen.blit(self.generate_selected_button, self.generate_button_rect)
        else:
            self.screen.blit(self.generate_button, self.generate_button_rect)
            
        # bouton mode de jeu (joueur ou éditeur)
        if self.game_mode_button_rect.collidepoint(mouse_pos):
            self.screen.blit(self.game_mode_selected_button, self.game_mode_button_rect)
        else:
            self.screen.blit(self.game_mode_button, self.game_mode_button_rect)
            
        # bouton changer de textures
        if self.change_textures_button_rect.collidepoint(mouse_pos):
            self.screen.blit(self.change_textures_selected_button, self.change_textures_button_rect)
        else:
            self.screen.blit(self.change_textures_button, self.change_textures_button_rect)
            
        # bouton afficher / cacher les erreurs
        if self.display_errors_button_rect.collidepoint(mouse_pos):
            self.screen.blit(self.display_errors_selected_button, self.display_errors_button_rect)
        else:
            self.screen.blit(self.display_errors_button, self.display_errors_button_rect)
            
        # bouton afficher / cacher l'affichage des cases durant la résolution
        if self.display_solving_button_rect.collidepoint(mouse_pos):
            self.screen.blit(self.display_solving_selected_button, self.display_solving_button_rect)
        else:
            self.screen.blit(self.display_solving_button, self.display_solving_button_rect)
 
        # mise à jour effective des modifications
        pygame.display.flip()
    
    def display_cell_elements(self, coordinates: tuple[int, int]):
        """
        mise à jour rapide d'une case uniquement, utilisée lors de la résolution
        :param coordinates: coordonnées de la case à mettre à jour
        """
        # Test de préconditions
        test_errors(self.grid_size, coordinates = coordinates)
        
        x, y = coordinates
        
        # mettre à jour une portion de l'écran
        self.screen.blit(self.cell_image, self.all_cell_rect[x][y])
        
        # Affichage du cadenas si la case est "locked"
        if self.game.sudoku.grid.get_cell_state(coordinates) == "locked":
            self.screen.blit(self.padlock_image, self.all_cell_rect[x][y])
        
        # affichage du chiffre de la case
        self.display_cell_digit(coordinates)
        
        # mise à jour effective des modifications
        pygame.display.flip()
    
    def display_cell_digit(self, coordinates):
        """
        Permet d'afficher une valeur particulière dans une case
        """
        
        test_errors(self.grid_size, coordinates = coordinates)
        
        # valeur à mettre
        digit = self.game.sudoku.grid.get_cell_value(coordinates)

        # case vide, rien à afficher
        if digit == '0':
            return
        
        # si la case n'est pas dans un conflit, affiche rla première ilage, sinon l'image avec la valeur en rouge
        if not self.game.sudoku.grid.is_cell_in_conflict(coordinates) or not self.do_display_conflicts:
            digit_image = self.all_digits_image[self.game.possible_values.index(digit)]
        else:
            digit_image = self.all_digits_image[self.game.possible_values.index(digit) + len(self.game.possible_values)]
        x, y = coordinates
        
        # modifier la portion concernée
        self.screen.blit(
            digit_image,
            self.all_cell_rect[x][y]
        )
    
    def load_image(self, path: str, dimensions: Union[list[int, int], list[float]]) -> pygame.Surface:
        """
        Charge une image redimensionnnée à la bonne taille de puis un chemin d'accès
        :param path: chemin de l'image depuis le chemin relatif `src/graphics/{texture_pack}/`
        :param dimensions: dimensions de sortie de l'image (redimensionnement)
        :return l'image redimensionnée spécifée dans `path`
        """
        # image
        image = pygame.image.load(f"src/graphics/{self.texture_pack + '/' + path}")
        resized_image = pygame.transform.smoothscale(image, dimensions)
        return resized_image

    def update_rect(self):
        """
        Calcule des dimensions et des coordonnées des éléments de la fenêtre
        """
        # défini l'icone du jeu
        self.icon = pygame.image.load(f"src/graphics/{self.texture_pack}/icon.png")
        pygame.display.set_icon(self.icon)
        
        # Test si la longueur de référence doit être la longueur ou la largeur de l'écran
        if self.screen.get_width() * (2 / 3) > self.screen.get_height():
            self.rect_ref_distance = self.screen.get_height()
        
        else:
            self.rect_ref_distance = self.screen.get_width() * (2 / 3)
        
        # calcul les dimensions de l'image de fond
        if self.screen.get_width() > self.screen.get_height():
            background_dimensions = [self.screen.get_width()] * 2
        
        else:
            background_dimensions = [self.screen.get_height()] * 2
        
        #
        self.rect_ref_distance *= 0.9
        # Ratio entre la longueur du grand carré et de la marge
        self.outline_thickness = self.rect_ref_distance / 30
        
        # calcul la taille de chaque cellule
        self.cell_dimensions = [(self.rect_ref_distance - (self.square_size + 1) * self.outline_thickness) * (1 / self.grid_size)] * 2
        
        # Calcule les dimensions et les coordonnées des boutons du menu de démarrage
        self.update_start_buttons_rect()
        # Calcule les dimensions et les coordonnées des boutons du menu principal
        self.update_game_buttons_rect()
        # Calcule les dimensions et les coordonnées des boutons du menu options
        self.update_options_buttons_rect()
        # Charge toutes les images possibles pour chaque cellule
        self.update_digits_rect()
        
        # image fond d'écran
        self.background = self.load_image("background.png", background_dimensions)
        
        # rectangle du fond d'écran
        self.background_rect = self.background.get_rect()
        self.background_rect.x = self.screen.get_width() / 2 - background_dimensions[0] / 2
        self.background_rect.y = self.screen.get_height() / 2 - background_dimensions[1] / 2
        
        # image fond de la grille
        self.grid_background = self.load_image("grid_background.png", [self.rect_ref_distance] * 2)
        
        # rectangle de l'image du fond de la grille
        self.grid_background_rect = self.grid_background.get_rect()
        self.grid_background_rect.x = self.screen.get_width() * (1 / 2) - self.rect_ref_distance * (1 / 4)
        self.grid_background_rect.y = self.screen.get_height() * (1 / 2) - self.rect_ref_distance * (1 / 2)
        
        # image d'une cellule déverrouillée
        self.cell_image = self.load_image("cells/cell.png", self.cell_dimensions)
        
        # image d'une cellule superverrouillée
        self.superlocked_cell_image = self.load_image("cells/superlocked_cell.png", self.cell_dimensions)
        
        # image d'une cellule sélectionnée
        self.selected_cell_image = self.load_image("cells/selected_cell.png", self.cell_dimensions)
        self.selected_cell_image = pygame.transform.smoothscale(self.selected_cell_image, self.cell_dimensions)
        
        # image d'une cellule superverrouillée et sélectionnée
        self.superlocked_selected_cell_image = self.load_image("cells/superlocked_selected_cell.png", self.cell_dimensions)
        
        # image du cadenas
        self.padlock_image = self.load_image("/cells/padlock.png", [self.cell_image.get_width() / 2.3] * 2)
        
        # calcul des coordonnées pour chaque case
        self.all_cell_rect = [[
            pygame.Rect([
                self.grid_background_rect.x + self.outline_thickness * (1 + x // self.square_size) + x * self.cell_image.get_width(),
                self.grid_background_rect.y + self.outline_thickness * (1 + y // self.square_size) + y * self.cell_image.get_height(),
                self.cell_image.get_width(),
                self.cell_image.get_height()
            ])
        for y in range(self.grid_size)] for x in range(self.grid_size)]
    
    def update_digits_rect(self):
        """
        Charge toutes les images possibles pour chaque cellule
        """
        self.all_digits_image: list[pygame.Surface] = []
        
        # balaye parmi les valeurs possibles pour ce sudoku `i`, et parmi les deux types d'imaage, les `regular`et les `wrong`
        for color in ["regular", "wrong"]:
            for i in self.game.possible_values:
                digit_image = pygame.image.load(f"src/graphics/{self.texture_pack}/digits/{i}_{color}.png")
                digit_image = pygame.transform.smoothscale(digit_image, self.cell_dimensions)
                self.all_digits_image.append(digit_image)
    
    def update_dimensions_button_rect(self):
        """
        Mettre à jour le bouton dimensions uniquement
        """
        self.dimensions_button = self.load_image("/buttons/options/dimensions_{self.grid_size}.png", self.options_buttons_dimensions)
        
        self.dimensions_selected_button = self.load_image("buttons/options/dimensions_{self.grid_size}_selected.png", self.options_buttons_dimensions)
    
    def update_game_mode_button_rect(self):
        """
        Mettre à jour le bouton mode de jeu uniquement
        """
        self.game_mode_button = self.load_image(f"/buttons/options/game_mode_{self.game.sudoku.game_mode}.png", self.options_buttons_dimensions)
        
        self.game_mode_selected_button = self.load_image(f"buttons/options/game_mode_{self.game.sudoku.game_mode}_selected.png", self.options_buttons_dimensions)
    
    def update_display_errors_button_rect(self):
        """
        Mettre à jour le bouton afficher / cacher les erreurs uniquement
        """
        self.display_errors_button = self.load_image(f"buttons/options/display_errors_{'on' if self.do_display_conflicts else 'off'}.png", self.options_buttons_dimensions)
        
        self.display_errors_selected_button = self.load_image(f"buttons/options/display_errors_{'on' if self.do_display_conflicts else 'off'}_selected.png", self.options_buttons_dimensions)
    
    def update_display_solving_button_rect(self):
        """
        Mettre à jour le bouton afficher / cacher l'affichage durant la résolution uniquement
        """
        self.display_solving_button = self.load_image(f"buttons/options/display_solving_{1}.png".format(self.texture_pack, "on" if self.game.do_display_during_solving else "off"))
        
        self.display_solving_selected_button = pygame.image.load(f"buttons/options/display_solving_{'on' if self.do_display_conflicts else 'off'}_selected.png", self.options_buttons_dimensions)
    
    def update_start_buttons_rect(self):
        """
        Calcule les dimensions et les coordonnées des boutons du menu de démarrage
        """
        
        # image bouton jouer - reference pour la taille pour le calcul
        self.play_button = pygame.image.load(f"src/graphics/{self.texture_pack}/buttons/start/play.png")
        
        # dimensions des boutons du menu démarrer
        self.start_buttons_dimensions = [
            self.rect_ref_distance - self.outline_thickness,
            (self.rect_ref_distance - self.outline_thickness) * (self.play_button.get_height() / self.play_button.get_width())
        ]
        
        # ccordonnées des boutons du menu démarrer
        ref_coordinates = [
            self.screen.get_width() / 2 - self.start_buttons_dimensions[0] / 2,
            self.screen.get_height() / 2 - self.rect_ref_distance / 2
        ]
        
        # espace vertical entre les boutons
        buttons_gap = (self.rect_ref_distance - self.start_buttons_dimensions[1]) / 5
        
        # redimensionnement du bouton
        self.play_button = pygame.transform.smoothscale(self.play_button, self.start_buttons_dimensions)
        
        # bouton jouer sélectionné
        self.play_selected_button = self.load_image("buttons/start/play_selected.png", self.start_buttons_dimensions)
        
        # rectangle du bouton jouer
        self.play_button_rect = self.play_button.get_rect()
        self.play_button_rect.x = ref_coordinates[0]
        self.play_button_rect.y = ref_coordinates[1] + buttons_gap
        
        # image bouton options
        self.options_start_button = self.load_image("buttons/start/options.png", self.start_buttons_dimensions)
        
        # image bouton options sélectionnée
        self.options_start_selected_button = self.load_image("buttons/start/options_selected.png", self.start_buttons_dimensions)
        
        # rectangle du bouton options
        self.options_start_button_rect = self.options_start_button.get_rect()
        self.options_start_button_rect.x = ref_coordinates[0]
        self.options_start_button_rect.y = ref_coordinates[1] + buttons_gap * 2
        
        #image bouton aide
        self.help_button = self.load_image("buttons/start/help.png", self.start_buttons_dimensions)
        
        # image bouotn aide séléctionnée
        self.help_button_selected = self.load_image("buttons/start/help_selected.png", self.start_buttons_dimensions)
        
        # rectangle bouton aide
        self.help_button_rect = self.help_button.get_rect()
        self.help_button_rect.x = ref_coordinates[0]
        self.help_button_rect.y = ref_coordinates[1] + buttons_gap * 3
        
        # image bouton quitter
        self.quit_button = self.load_image("buttons/start/quit.png", self.start_buttons_dimensions)
        
        # image bouton quitter sélectionnée
        self.quit_selected_button = self.load_image("buttons/start/quit_selected.png", self.start_buttons_dimensions)
        
        # rectangle bouton quitter
        self.quit_button_rect = self.quit_button.get_rect()
        self.quit_button_rect.x = ref_coordinates[0]
        self.quit_button_rect.y = ref_coordinates[1] + buttons_gap * 4
    
    def update_game_buttons_rect(self):
        """
        Calcule les dimensions et les coordonnées des bouttons du menu principal
        """
        
        # image bouton ouvrir - sert taille reference pour calcul taille
        self.open_button = pygame.image.load(f"src/graphics/{self.texture_pack}/buttons/game/open.png")

        # calcul la taille des boutons
        self.game_buttons_dimensions = [
            self.rect_ref_distance / 2 - self.outline_thickness,
            (self.rect_ref_distance / 2 - self.outline_thickness) * (self.open_button.get_height() / self.open_button.get_width())
        ]
        
        # calcul les coordonnées des boutons
        ref_coordinates = [
            self.screen.get_width() / 2 - self.rect_ref_distance * (3 / 4),
            self.screen.get_height() / 2 - self.rect_ref_distance / 2
        ]
        
        # espace vertical entre les boutons
        buttons_gap = (self.rect_ref_distance - self.game_buttons_dimensions[1]) / 5

        # redimensionnement bouton ouvrir
        self.open_button = pygame.transform.smoothscale(self.open_button, self.game_buttons_dimensions)

        # image bouton
        self.open_selected_button = self.load_image("buttons/game/open_selected.png", self.game_buttons_dimensions)
        
        # rectangle du bouton ouvrir
        self.open_button_rect = self.open_button.get_rect()
        self.open_button_rect.x = ref_coordinates[0]
        self.open_button_rect.y = ref_coordinates[1] + buttons_gap * 3

        # image bouton sauvegarder
        self.save_button = self.load_image("buttons/game/save.png", self.game_buttons_dimensions)

        # image bouton sauvegarder sélectionnée
        self.save_selected_button = self.load_image("buttons/game/save_selected.png", self.game_buttons_dimensions)

        # rectangle bouton sauvegarder
        self.save_button_rect = self.save_button.get_rect()
        self.save_button_rect.x = ref_coordinates[0]
        self.save_button_rect.y = ref_coordinates[1] + buttons_gap * 2


        # image bouton résoudre
        self.solve_button = self.load_image("buttons/game/solve.png", self.game_buttons_dimensions)
        
        # image bouton résoudre sélectionnée
        self.solve_selected_button = self.load_image("buttons/game/solve_selected.png", self.game_buttons_dimensions)
        
        # rectangle bouton résoudre
        self.solve_button_rect = self.solve_button.get_rect()
        self.solve_button_rect.x = ref_coordinates[0]
        self.solve_button_rect.y = ref_coordinates[1] + buttons_gap
        
        # image bouton options
        self.options_button = self.load_image("buttons/game/options.png", self.game_buttons_dimensions)
        
        # image bouton options sélectionnée
        self.options_selected_button = self.load_image("buttons/game/options_selected.png", self.game_buttons_dimensions)
        
        # rectangle bouton options
        self.options_button_rect = self.options_button.get_rect()
        self.options_button_rect.x = ref_coordinates[0]
        self.options_button_rect.y = ref_coordinates[1] + buttons_gap * 4
        
        # image bouton retour
        self.return_button = self.load_image("buttons/game/return.png", self.game_buttons_dimensions)
        
        # image bouton retour sélectionnée
        self.return_selected_button = self.load_image("buttons/game/return_selected.png", self.game_buttons_dimensions)
        
        # rectangle bouton retour
        self.return_button_rect = self.return_button.get_rect()
        self.return_button_rect.x = ref_coordinates[0]
        self.return_button_rect.y = ref_coordinates[1] + buttons_gap * 5
        
        # image bouton annuler
        self.arrow_left_button = self.load_image("buttons/game/arrow_left.png", [self.game_buttons_dimensions[1]] * 2)
        
        # image bouton annuler sélectionné
        self.arrow_left_selected_button = self.load_image("buttons/game/arrow_left_selected.png", [self.game_buttons_dimensions[1]] * 2)
        
        # image bouton annuler désactivée
        self.arrow_left_disabled_button =self.load_image("buttons/game/arrow_left_disabled.png", [self.game_buttons_dimensions[1]] * 2)
        
        # rectangle bouton annuler
        self.arrow_left_button_rect = self.arrow_left_button.get_rect()
        self.arrow_left_button_rect.x = ref_coordinates[0]
        self.arrow_left_button_rect.y = ref_coordinates[1]
        
        # image bouton vider la grille
        self.cross_button = self.load_image("buttons/game/cross.png", [self.game_buttons_dimensions[1]] * 2)
        
        # image bouton vider la grille sélectionnée
        self.cross_selected_button = self.load_image("buttons/game/cross_selected.png", [self.game_buttons_dimensions[1]] * 2)
        
        # rectangle bouton vider la grille
        self.cross_button_rect = self.cross_button.get_rect()
        self.cross_button_rect.x = ref_coordinates[0] + self.game_buttons_dimensions[0] / 2 - self.game_buttons_dimensions[1] / 2
        self.cross_button_rect.y = ref_coordinates[1]

        # image bouton rétablir
        self.arrow_right_button = self.load_image("buttons/game/arrow_right.png", [self.game_buttons_dimensions[1]] * 2)
        
        # image bouton rétablir sélectionnée
        self.arrow_right_selected_button = self.load_image("buttons/game/arrow_right_selected.png", [self.game_buttons_dimensions[1]] * 2)
        
        # image bouton rétablir désactivée
        self.arrow_right_disabled_button = self.load_image("buttons/game/arrow_right_disabled.png", [self.game_buttons_dimensions[1]] * 2)
        
        # rectangle bouton rétablir
        self.arrow_right_button_rect = self.arrow_right_button.get_rect()
        self.arrow_right_button_rect.x = ref_coordinates[0] + self.game_buttons_dimensions[0] - self.game_buttons_dimensions[1]
        self.arrow_right_button_rect.y = ref_coordinates[1]
    
    def update_options_buttons_rect(self):
        """
        Calcule les dimensions et les coordonnées des boutons du menu d'options
        """
        
        # image bouton dimensions - sert de reference pour la taille
        self.dimensions_button = pygame.image.load(f"src/graphics/{self.texture_pack}/buttons/options/dimensions_{self.grid_size}.png")
        
        # dimensions des boutons
        self.options_buttons_dimensions = [
            self.rect_ref_distance - self.outline_thickness,
            (self.rect_ref_distance - self.outline_thickness) * self.dimensions_button.get_height() / self.dimensions_button.get_width()
        ]
        
        # coordonnées des boutons
        ref_coordinates = [
            self.screen.get_width() / 2 - self.options_buttons_dimensions[0] / 2,
            self.screen.get_height() / 2 - self.rect_ref_distance / 2
        ]
        
        # espace vertical entre les boutons
        buttons_gap = (self.rect_ref_distance - self.options_buttons_dimensions[1]) / 5
        
        # redimensionnement du bouton dimensions
        self.dimensions_button = pygame.transform.smoothscale(self.dimensions_button, self.options_buttons_dimensions)
        
        # image bouton dimensions sélectionnée
        self.dimensions_selected_button = self.load_image(f"buttons/options/dimensions_{self.grid_size}_selected.png", self.options_buttons_dimensions)
        
        # rectangle bouton dimensions
        self.dimensions_button_rect = self.dimensions_button.get_rect()
        self.dimensions_button_rect.x = ref_coordinates[0]
        self.dimensions_button_rect.y = ref_coordinates[1]
        
        # image bouton générer
        self.generate_button = self.load_image("buttons/options/generate.png", self.options_buttons_dimensions)
        
        # image bouton générer sélectionnée
        self.generate_selected_button = self.load_image("buttons/options/generate_selected.png", self.options_buttons_dimensions)
        
        # rectangle  bouton générer
        self.generate_button_rect = self.generate_button.get_rect()
        self.generate_button_rect.x = ref_coordinates[0]
        self.generate_button_rect.y = ref_coordinates[1] + buttons_gap
        
        # image bouton mode de jeu
        self.game_mode_button = self.load_image(f"buttons/options/game_mode_{self.game.sudoku.game_mode}.png", self.options_buttons_dimensions)
        
        # image bouton mode de jeu sélectionnée
        self.game_mode_selected_button = self.load_image(f"buttons/options/game_mode_{self.game.sudoku.game_mode}_selected.png", self.options_buttons_dimensions)
        
        # rectangle mode de jeu
        self.game_mode_button_rect = self.game_mode_button.get_rect()
        self.game_mode_button_rect.x = ref_coordinates[0]
        self.game_mode_button_rect.y = ref_coordinates[1] + buttons_gap * 2
        
        # image textures pack
        self.change_textures_button = self.load_image("buttons/options/change_textures.png", self.options_buttons_dimensions)
        
        #image textures pack sélectionnée
        self.change_textures_selected_button = self.load_image("buttons/options/change_textures_selected.png", self.options_buttons_dimensions)
        
        # rectangle textures pack
        self.change_textures_button_rect = self.change_textures_button.get_rect()
        self.change_textures_button_rect.x = ref_coordinates[0]
        self.change_textures_button_rect.y = ref_coordinates[1] + buttons_gap * 3
        
        # image bouton afficher erreurs
        self.display_errors_button = self.load_image(f"buttons/options/display_errors_{'on' if self.do_display_conflicts else 'off'}.png", self.options_buttons_dimensions)
        
        # image bouton afficher erreurs sélectionnée
        self.display_errors_selected_button = self.load_image(f"buttons/options/display_errors_{'on' if self.do_display_conflicts else 'off'}_selected.png", self.options_buttons_dimensions)
        
        # rectangle bouton afficher erreurs
        self.display_errors_button_rect = self.display_errors_button.get_rect()
        self.display_errors_button_rect.x = ref_coordinates[0]
        self.display_errors_button_rect.y = ref_coordinates[1] + buttons_gap * 4
        
        # image bouton afficher solution pendant résolution
        self.display_solving_button = self.load_image(f"buttons/options/display_solving_{'on' if self.do_display_conflicts else 'off'}.png", self.options_buttons_dimensions)
        
        # image bouton afficher solution pendant résolution sélectionnée
        self.display_solving_selected_button = self.load_image(f"buttons/options/display_solving_{'on' if self.do_display_conflicts else 'off'}_selected.png", self.options_buttons_dimensions)
        
        # rectangle bouton afficher solution pendant résolution
        self.display_solving_button_rect = self.display_solving_button.get_rect()
        self.display_solving_button_rect.x = ref_coordinates[0]
        self.display_solving_button_rect.y = ref_coordinates[1] + buttons_gap * 5
        
        # image bouton quitter
        self.cross_options_button = self.load_image("buttons/options/cross.png", [self.options_buttons_dimensions[1] * (2 / 3)] * 2)
        
        # image bouton quitter sélectionnée
        self.cross_selected_options_button = self.load_image("buttons/options/cross_selected.png", [self.options_buttons_dimensions[1] * (2/3)] * 2)
        
        # rectangle quitter
        self.cross_options_button_rect = self.cross_options_button.get_rect()
        self.cross_options_button_rect.x = self.outline_thickness * 2
        self.cross_options_button_rect.y = ref_coordinates[1] * (4/3)