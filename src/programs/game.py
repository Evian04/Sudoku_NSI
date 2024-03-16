# import des librairies
import os
import pygame
import json
# nos modules
from src.programs.sudoku import Sudoku
from src.programs.graphism import Graphism
from src.programs.test_errors import test_errors


class Game:
    """
    La classe Game permet de mettre en relation les entrées de l'utilisateurs avec la grille du sudoku et la gestion de l'affichage
    """
    
    def __init__(self, screen: pygame.Surface):
        self.do_quit = False
        # enregistre l'écran
        self.screen: pygame.Surface = screen
        
        # chemin du fichier à ouvrir pour le bouton aide (Notice)
        self.help_filepath = "Notice Sudokool.pdf"
        
        # menu actuel, par défaut, menu de démarrage (bouton jouer)
        self.current_menu = "start"
        # inidque si le menu options est ouvert
        self.is_options_open = False
        # indique si unue résolution est en cours
        self.is_solving = False
        
        # indique si la fenetre a le focus
        self.is_window_focused = False
        
        # charge le fichier de configuration et met à jour l'attribut self.config_file
        self.load_config_file()
        # indique si l'affichage doit être fait pendant la résoltion // récupèrre ce paramètre dans config file
        self.do_display_during_solving = self.get_config_value("do_display_during_solving")
        
        # Valeurs possibles pour les symboles (chiffre puis lettre)
        self.possible_values = "123456789ABCDEFG"
        
        # créé l'instance sudoku
        self.sudoku = Sudoku(self, 9)
        # créé l'instance graphism
        self.graphism = Graphism(
            self,  # passe game
            self.sudoku.grid.size,  # passe la taille de la grille
            self.get_config_value("texture_pack"),  # le texture pack actuel
            self.get_config_value("do_display_conflicts"),
            self.get_config_value("do_play_music")
            # la valeur qui indique si il faut afficher les cases en conflit
        )
        
        self.name = "Sudokool"
        # mettre à jour le titre de la fenêtre
        self.update_title()
        
        # mapping des touches du clavier pour ajouter/modifier la valeur d'une case // remplace une touche par une valeur
        self.key_mapping: dict[str] = {
            pygame.K_1:         '1',
            pygame.K_KP_1:      '1',
            pygame.K_2:         '2',
            pygame.K_KP_2:      '2',
            pygame.K_3:         '3',
            pygame.K_KP_3:      '3',
            pygame.K_4:         '4',
            pygame.K_KP_4:      '4',
            pygame.K_5:         '5',
            pygame.K_KP_5:      '5',
            pygame.K_6:         '6',
            pygame.K_KP_6:      '6',
            pygame.K_7:         '7',
            pygame.K_KP_7:      '7',
            pygame.K_8:         '8',
            pygame.K_KP_8:      '8',
            pygame.K_9:         '9',
            pygame.K_KP_9:      '9',
            pygame.K_a:         "A",
            pygame.K_b:         "B",
            pygame.K_c:         "C",
            pygame.K_d:         "D",
            pygame.K_e:         "E",
            pygame.K_f:         "F",
            pygame.K_g:         "G",
            
            # 0 correspond à une case vide (supprime la valeur de la case)
            pygame.K_BACKSPACE: "0",
            pygame.K_DELETE:    "0",
            pygame.K_0:         "0",
            pygame.K_KP_0:      "0"
        }
        
        # met à jour la taille des images // pas d'affichage
        self.graphism.update_rect()
    
    def update_title(self, title: str = ""):
        """
        defini le titre de la fenetre
        :param title: nouveau titre de la fenetre, si non spécifié utilise self.title
        """
        
        if title == "":
            # redefini le titre à partir du nom du jeu, de la taille et du mode de jeu
            pygame.display.set_caption(
                self.name + f" {self.sudoku.grid.size}x{self.sudoku.grid.size} - " + (
                    "joueur" if self.sudoku.game_mode == "playing" else "éditeur")
            )
        
        else:
            # défini le nom à partir de l'argument
            pygame.display.set_caption(title)
    
    def update(self, do_display = True):
        """
        Met à jour l'affichage du jeu
        """
        
        # Si la souris est immobile ou que  ne met pas à jour l'affichage du jeu
        if not do_display or pygame.mouse.get_rel() == (0, 0):
            do_display = False
            
        else:
            do_display = True
        
        # met en pause la lecture de la musique ou la reprend en fonction du focus
        if self.is_window_focused != pygame.key.get_focused():
            self.is_window_focused = pygame.key.get_focused()
            print("focus", "in" if self.is_window_focused else "out")
            # joue ou arrete la lecture du son
            self.graphism.set_music_state(do_play = self.is_window_focused)
        
        # si la fenetre n'a pas le focus, n'affiche pas les élements (économie ressources)
        if not self.is_window_focused:
            do_display = False
        
        # si le menu options est ouvert
        if self.is_options_open:
            self.update_options(do_display)
        
        # si le mmenu démarrer est ouvert
        elif self.current_menu == "start":
            self.update_start(do_display)
        
        # sii le menu normal (grille) est ouvert
        elif self.current_menu == "game":
            self.update_game(do_display)
    
    def update_start(self, do_display: bool):
        """
        Met à jour l'état du jeu lorsque le menu de démarrage est ouvert
        """
        
        # récupère les evenements en cours
        all_events = pygame.event.get()
        
        # balaye dans les évenements
        for event in all_events:
            if event.type == pygame.QUIT:
                self.do_quit = True
                return
            
            # Si la fenètre est redimensionnée
            if event.type == pygame.WINDOWRESIZED:
                do_display = True
                # Mettre à jour la position / dimensions des éléments de la fenêtre
                self.graphism.update_rect()
                pygame.display.flip()
            
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_LEFT:
                do_display = True
                # si l'evenement est de type appui de bouton souris
                mouse_pos = pygame.mouse.get_pos()
                
                # si le bouton play est selectionnée
                if self.graphism.play_button_rect.collidepoint(mouse_pos):
                    self.current_menu = "game"
                
                # si le bouton options est selectionnée
                elif self.graphism.options_start_button_rect.collidepoint(mouse_pos):
                    self.is_options_open = True
                
                elif self.graphism.help_button_rect.collidepoint(mouse_pos):
                    self.open_file(self.help_filepath)
                
                # si le bouton quitter est selectionnée
                elif self.graphism.quit_button_rect.collidepoint(mouse_pos):
                    self.do_quit = True
                    return
        
        # si on souahite afficher
        if do_display:
            self.graphism.display_start_elements()
    
    def update_game(self, do_display: bool):
        """
        Met à jour l'état du jeu lorsque le menu de jeu est affiché
        """
        
        all_events = pygame.event.get()
        # boolean qui indique si une touche controle est pressé
        is_ctrl_pressed = pygame.key.get_pressed()[pygame.K_LCTRL] or pygame.key.get_pressed()[pygame.K_RCTRL]
        
        # Pour tous les évènements qui ont eu lieu depuis la dernière mise à jour de la fenêtre
        for event in all_events:
            
            if event.type == pygame.QUIT:
                self.do_quit = True
                return
            
            # Si la fenètre est redimensionnée
            elif event.type == pygame.WINDOWRESIZED:
                do_display = True
                # Mettre à jour la position / dimensions des éléments de la fenêtre
                self.graphism.update_rect()
                pygame.display.flip()
            
            # Ne pas vérifier les autres event si la résolution est en cours (économie performance)
            if self.is_solving:
                continue
            
            # Si l'utilisateur clique sur l'écran
            elif event.type == pygame.MOUSEBUTTONDOWN:
                do_display = True
                mouse_pos = pygame.mouse.get_pos()
                
                # S'il s'agit d'un clique gauche
                if event.button == pygame.BUTTON_LEFT:
                    # Si le curseur de la souris est sur une case de la grille
                    for x in range(self.sudoku.grid.size):
                        for y in range(self.sudoku.grid.size):
                            if self.graphism.all_cell_rect[x][y].collidepoint(mouse_pos):
                                # Sélectionner la case qui a été cliquée
                                self.sudoku.select_cell((x, y))
                    
                    # vérifie si la touche 'croix' a été pressé
                    if self.graphism.cross_button_rect.collidepoint(mouse_pos):
                        # si la touche controle est pressé
                        if is_ctrl_pressed:
                            # supprimer toutes les valeurs de la grilles
                            self.sudoku.clear_inputs(do_save_in_history=True)
                        
                        else:
                            # supprimer les cases déverrouillées
                            self.sudoku.clear()
                        
                        # vérifier la validiété de la grille
                        self.sudoku.verify_grid()
                    
                    # bouton annuler dernière action
                    elif self.graphism.arrow_left_button_rect.collidepoint(
                            mouse_pos) and self.sudoku.is_history_move_possible("backward"):
                        self.sudoku.move_index_history("backward")
                        print("Action canceled")
                    
                    # bouton retablir la dernière action
                    elif self.graphism.arrow_right_button_rect.collidepoint(
                            mouse_pos) and self.sudoku.is_history_move_possible("forward"):
                        self.sudoku.move_index_history("forward")
                        print('Action restored')
                    
                    # bouton ouvrir
                    elif self.graphism.open_button_rect.collidepoint(mouse_pos):
                        self.sudoku.open_grid()
                        self.graphism.update_grid_attributes(self.sudoku.grid.size)
                    
                    # bouton enregistrer
                    elif self.graphism.save_button_rect.collidepoint(mouse_pos):
                        self.sudoku.save_grid()
                    
                    # bouton résoudre le sudoku
                    elif self.graphism.solve_button_rect.collidepoint(mouse_pos):
                        self.sudoku.solve_grid(self.do_display_during_solving)
                        self.sudoku.verify_grid()
                    
                    # bouton options
                    elif self.graphism.options_button_rect.collidepoint(mouse_pos):
                        self.is_options_open = True
                    
                    # bouton retour (au menu démarrer)
                    elif self.graphism.return_button_rect.collidepoint(mouse_pos):
                        self.current_menu = "start"
                
                # Si l'utilisateur effectue un clique droit
                elif event.button == pygame.BUTTON_RIGHT:
                    # boucle sur toutes les cases
                    for x in range(self.sudoku.grid.size):
                        for y in range(self.sudoku.grid.size):
                            
                            # Si la souris est sur l'une des cases de la grille
                            if self.graphism.all_cell_rect[x][y].collidepoint(mouse_pos):
                                # Inverser l'état de verrouillage de la case en question
                                self.sudoku.reverse_cell_lock((x, y))
            
            # si une touche est pressée
            if event.type == pygame.KEYDOWN:
                do_display = True
                # touche Echap
                if event.key == pygame.K_ESCAPE:
                    if self.is_options_open:
                        self.is_options_open = False
                    else:
                        self.sudoku.deselect_cell()
                
                # fleche gauche
                if event.key == pygame.K_LEFT:
                    self.sudoku.move_selected_cell("left")
                
                # flèche droite
                if event.key == pygame.K_RIGHT:
                    self.sudoku.move_selected_cell("right")
                
                # flèche haut
                if event.key == pygame.K_UP:
                    self.sudoku.move_selected_cell("up")
                
                # flèche bas
                if event.key == pygame.K_DOWN:
                    self.sudoku.move_selected_cell("down")
                
                # Ctrl + C - supprime toutes les valeurs des cases déverrouillées
                if event.key == pygame.K_c and is_ctrl_pressed:
                    self.sudoku.clear()
                    self.sudoku.verify_grid()
                # Ctrl + z : annuler la dernière action
                
                if event.key == pygame.K_z and is_ctrl_pressed:
                    self.sudoku.move_index_history("backward")
                
                # Ctrl + y : restaurer l'action annulée
                if event.key == pygame.K_y and is_ctrl_pressed:
                    self.sudoku.move_index_history("forward")
                
                # une valeur présente dans key_mapping a été pressé
                if event.key in self.key_mapping and not is_ctrl_pressed:
                    # Si aucune case n'est sélectionnée, ne rien faire
                    if self.sudoku.selected_cell == (-1, -1):
                        continue
                    
                    # Si la valeur n'est pas compatible avec la taille de la grille actuelle, ne rien faire
                    if not self.key_mapping[event.key] in "0" + self.possible_values[:self.sudoku.grid.size]:
                        continue
                    
                    # récupère la valeur à affecter à partir du dictionnaire self.key_mapping
                    value = self.key_mapping[event.key]
                    
                    # modifie la valeur de la case selectionnée
                    self.sudoku.set_selected_cell_value(value)
                    
                    # vérifie si cette valeur entre en conflit avec d'autres valeurs de la grille
                    self.sudoku.verify_grid()
        
        if do_display:
            self.graphism.display_game_elements()
    
    def update_options(self, do_display: bool):
        """
        Met à jour l'état du jeu lorsque le menu d'options est ouvert
        """
        
        mouse_pos = pygame.mouse.get_pos()
        all_events = pygame.event.get()
        
        # balayer dans les evenements
        for event in all_events:
            if event.type == pygame.QUIT:
                self.do_quit = True
                return
            
            # Si la fenètre est redimensionnée
            if event.type == pygame.WINDOWRESIZED:
                do_display = True
                # Mettre à jour la position / dimensions des éléments de la fenêtre
                self.graphism.update_rect()
                pygame.display.flip()
            
            # clic gauche
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_LEFT:
                do_display = True
                
                # croix pour quitter le menu options
                if self.graphism.cross_options_button_rect.collidepoint(mouse_pos):
                    self.is_options_open = False
                
                # bouton dimensions
                if self.graphism.dimensions_button_rect.collidepoint(mouse_pos):
                    
                    # afficher image taille 9x9
                    if self.sudoku.grid.size == 4:
                        is_action_successful = self.sudoku.new_empty_grid(9)
                    
                    # afficher image taille 16x16
                    elif self.sudoku.grid.size == 9:
                        is_action_successful = self.sudoku.new_empty_grid(16)
                    
                    # afficher taille 4x4
                    else:
                        is_action_successful = self.sudoku.new_empty_grid(4)
                    
                    if is_action_successful:
                        self.graphism.update_grid_attributes(self.sudoku.grid.size)
                        self.graphism.update_dimensions_button()
                
                # bouton générer
                elif self.graphism.generate_button_rect.collidepoint(mouse_pos):
                    
                    # quitter le menu options
                    self.is_options_open = False
                    self.current_menu = "game"
                    self.graphism.display_game_elements()
                    
                    self.sudoku.generate_grid(0.5)
                    self.sudoku.verify_grid()
                
                # bouton mode de jeu (joueur / éditeur)
                elif self.graphism.game_mode_button_rect.collidepoint(mouse_pos):
                    self.sudoku.reverse_game_mode()
                    self.update_title()
                    self.graphism.update_game_mode_button()
                
                # bouotn changer de textures
                elif self.graphism.change_textures_button_rect.collidepoint(mouse_pos):
                    self.graphism.ask_texture_pack()
                    self.set_config_value("texture_pack", self.graphism.texture_pack)
                
                # bouton activer / desactiver la musique
                elif self.graphism.play_music_button_rect.collidepoint(mouse_pos):
                    # lance la musique
                    self.graphism.reverse_play_music()
                    self.graphism.set_music_state(self.graphism.do_play_music)
                    
                    # met à jour le boutton "play music"
                    self.graphism.update_play_music_buton()
                    
                    # enregistre le paramètre dans le fichier "config.json"
                    self.set_config_value("do_play_music", self.graphism.do_play_music)
                
                # bouton afficher / cacher les erreurs
                elif self.graphism.display_errors_button_rect.collidepoint(mouse_pos):
                    self.graphism.reverse_display_conflicts()
                    self.graphism.update_display_errors_button()
                    self.set_config_value("do_display_conflicts", self.graphism.do_display_conflicts)
                
                # bouton afficher / cacher les cases durant la résolution
                elif self.graphism.display_solving_button_rect.collidepoint(mouse_pos):
                    self.do_display_during_solving = not self.do_display_during_solving
                    self.graphism.update_display_solving_button()
                    self.set_config_value("do_display_during_solving", self.do_display_during_solving)
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    do_display = True
                    self.is_options_open = False
        
        if pygame.mouse.get_pressed()[0] and self.graphism.cursor_background_button_rect.collidepoint(mouse_pos):
            cursor_new_x = mouse_pos[0] - self.graphism.cursor_button.get_width() / 2
            
            self.graphism.cursor_button_rect.x = cursor_new_x
            
            lower_bound = self.graphism.cursor_background_button_rect.x
            upper_bound = self.graphism.cursor_background_button_rect.x + self.graphism.cursor_background_button.get_width() - self.graphism.cursor_button.get_width()
            
            if cursor_new_x < lower_bound:
                self.graphism.cursor_button_rect.x = lower_bound
            
            elif cursor_new_x > upper_bound:
                self.graphism.cursor_button_rect.x = upper_bound
        
        if do_display:
            self.graphism.display_options_elements()
    
    def cell_update(self, coordinates: tuple[int, int], do_display: bool = True):
        """
        Met à jour une case uniquement (gain de performance), utilisée lors de la résolution
        """
        
        test_errors(self.sudoku.grid.size, coordinates=coordinates)
        
        all_events = pygame.event.get()
        
        for event in all_events:
            if event.type == pygame.QUIT:
                self.do_quit = True
                return False
            
            if event.type == pygame.WINDOWRESIZED:
                do_display = True
                self.graphism.update_rect()
                self.graphism.display_game_elements()
        
        if do_display:
            self.graphism.display_cell_elements(coordinates)
    
    def open_file(self, filepath: str) -> bool:
        """
        Ouvre le fichier spécifié grâce à une application externe (non python)
        :param filepath: chemin d'accès absolu ou relatif
        :return: boolean indiquant la réusiste ou non de l'ouverture du fichier
        """
        # ouvre le fichier spécifié grâce à une commande cmd
        result = os.system(f'start "" "{filepath}"')
        # opération réussi - fichier ouvert
        if result == 0:
            return True
        # échec opération - fichier non ouvert
        else:
            return False
    
    def load_config_file(self):
        """
        Charge le fichier de configuration spécifié à self.config_filepath
        attribut self.config_file mis à jour
        """
        
        with open("src/config.json") as file:
            self.config_file = json.load(fp=file)
    
    def get_config_value(self, key: str):
        """
        recupère une valeur de configuration
        :param key: configuration à récupérer (clé)
        :return: valeur obtenue (différents types int, bool, etc)
        """
        
        test_errors(config_file=self.config_file, config_key=key)
        
        return self.config_file[key]
    
    def set_config_value(self, key: str, value):
        """
        met à jour le fichier de configuration
        :param key: clé de l'élément à mettre à jour
        :param value: nouvelle valeur
        """
        
        test_errors(config_file=self.config_file, config_key=key, config_value=value)
        
        self.config_file[key] = value
        
        with open("src/config.json", "w") as file:
            file.write(json.dumps(self.config_file))
