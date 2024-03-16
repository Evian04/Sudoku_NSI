# import des libraires
import random
import time
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter.messagebox import askyesnocancel, showinfo
# nos modules
from src.programs.grid import Grid
from src.programs.test_errors import test_errors


class Sudoku:
    """
    La classe "Sudoku" permet d'effectuer des actions complexes sur la grille,
    telles que la résoudre, en charger une depuis un fichier, ou encore en générer une nouvelle
    """
    
    def __init__(self, game, grid_size: int):
        
        # Test préconditions
        test_errors(grid_size)
        
        # indique si la grille a été enregistrée, autrement dit si des modifications ont été appliquée depuis le dernier enregistrement
        self.is_grid_saved = True
        self.game = game  # contient la classe game
        
        # défini le mode entre 'editing' et 'playing'
        self.game_mode = "editing"
        
        # contient la grille avec les cases
        self.grid = Grid(grid_size)
        
        # Coordonnées de la case sélectionnée, (-1, -1) si aucune case
        self.selected_cell = (-1, -1)
        
        # historique de la grille, permet de revenir en arrière, et/ou de rétablir
        self.history: list[tuple[Grid, tuple[int, int]]] = [(self.grid.copy(), self.selected_cell)]
        # indique à quel index on se situe dans l'historique
        self.history_index = 0
        
        # dictionnaire permettant de convertir un état en en chiffre entre 0 et 2 pour l'enregistrement dans un fichier
        self.save_state_conversion = {"unlocked": "0", "locked": "1", "superlocked": "2"}
        # dictionnaire permettant de convertir un chiffre entre 0 et 2 pour l'ouverture d'un fichier
        self.load_state_conversion = {"0": "unlocked", "1": "locked", "2": "superlocked"}
        
        # liste des cases en conflit, c'est à dire dont au moins une ligne, une colonne ou un carré admet deux valeurs identiques
        self.conflicting_cells: list[tuple[int, int]] = list()
    
    def reverse_game_mode(self):
        """
        Met le mode de jeu sur "playing" s'il était sur "editing" et inversement
        """
        
        if self.game_mode == "playing":
            self.game_mode = "editing"
        
        else:
            self.game_mode = "playing"
        
        # Test postconditions
        test_errors(game_mode=self.game_mode)
    
    def set_game_mode(self, game_mode: str):
        """
        Attribue à la variable "game_mode" la valeur indiquée, elle peut être soit `editing` soit `playing`
        """
        
        # Test préconditions
        test_errors(game_mode=game_mode)
        
        self.game_mode = game_mode
        print(f"The game mode was set to {game_mode}")
    
    def select_cell(self, coordinates: tuple[int, int]):
        """
        Selectionne la case de coordonnées (x, y)
        """
        
        # Test préconditions
        test_errors(self.grid.size, coordinates=coordinates)
        
        # Code de la fonction
        self.selected_cell = coordinates
    
    def deselect_cell(self):
        """
        Déselectionne la case sélectionnée
        """
        
        # Code de la fonction
        self.selected_cell = (-1, -1)
    
    def move_selected_cell(self, direction: str):
        """
        Déplace les coordonnées de la case sélctionnées vers la direction indiquée, la valeur peutt être `left`, `right`, `up` ou `down`
        """
        
        # Test des préconditions
        test_errors(direction=direction)
        
        # Si aucune case n'est sélectionnée, retourne None
        if self.selected_cell == (-1, -1):
            return
        
        # fonction match case, correspond à un if direction == ... elif direction == ... mais optimisé par python
        match direction:
            case "left":
                # Si la sélection est au bord de la grille dans la direction indiquée
                if self.selected_cell[0] == 0:
                    return
                
                # Déplacer la sélection d'une case vers la gauche
                self.selected_cell = (self.selected_cell[0] - 1, self.selected_cell[1])
            
            case "right":
                # Si la sélection est au bord de la grille dans la direction indiquée
                if self.selected_cell[0] == self.grid.size - 1:
                    return
                
                # Déplacer la sélection d'une case vers la droite
                self.selected_cell = (self.selected_cell[0] + 1, self.selected_cell[1])
            
            case "up":
                # Si la sélection est au bord de la grille dans la direction indiquée
                if self.selected_cell[1] == 0:
                    return
                
                # Déplacer la sélection d'une case vers le haut
                self.selected_cell = (self.selected_cell[0], self.selected_cell[1] - 1)
            
            case "down":
                # Si la sélection est au bord de la grille dans la direction indiquée
                if self.selected_cell[1] == self.grid.size - 1:
                    return
                
                # Déplacer la sélection d'une case vers le bas
                self.selected_cell = (self.selected_cell[0], self.selected_cell[1] + 1)
        
        # Test des postconditions
        test_errors(self.grid.size, coordinates=self.selected_cell)
    
    def set_selected_cell_value(self, value: str):
        """
        Met la valeur de la case sélectionnée à "value", elle est compris entre 0 et le maximum autorisée par la largeur de la grille
        """
        
        # Test des préconditions
        test_errors(self.grid.size, coordinates=self.selected_cell, value=value)
        
        # si le mode est joueur et que la case est verrouillée ou superverrouillé la case n'es ttpas modifiée, affiche un message dans la console
        if self.game_mode == "playing" and self.grid.get_cell_state(self.selected_cell) in ["locked", "superlocked"]:
            print(
                f"The cell {self.selected_cell} is {self.grid.get_cell_state(self.selected_cell)}, You cannot change its value while playing"
            )
            
            return
        
        if self.grid.get_cell_value(self.selected_cell) != value:
            # defini la valeur de la case
            self.grid.set_cell_value(self.selected_cell, value)
            # affiche un message console
            print(f"The value of the cell {self.selected_cell} was set to {value}")
            
            # enregistre l'action dans l'historique
            self.save_grid_in_history()
            # indique que la grille a été modifiée depuis le dernier enregistrement
            self.is_grid_saved = False
        else:
            print(f"Same value for cell {self.selected_cell}, cell NOT modified")
    
    def reverse_selected_cell_lock(self):
        """
        Inverse l'état de verrouillage de la case sélectionnée
        """
        
        # Test préconditions
        test_errors(coordinates=self.selected_cell)
        
        # inverse l'état
        self.reverse_cell_lock(self.selected_cell)
    
    def reverse_cell_lock(self, coordinates: tuple[int, int]):
        """
        Inverse l'état de verrouillage de la case indiquée
        """
        
        # Test préconditions
        test_errors(self.grid.size, coordinates=coordinates)
        
        # indique si la grille a été modifiée (initialisation)
        is_grid_changed = False
        
        # Si le mode de jeu est sur joueur
        if self.game_mode == "playing":
            # fonction match case
            match self.grid.get_cell_state(coordinates):
                
                # Si la case est déverrouillée
                case "unlocked":
                    # Mettre l'état de la case à verrouillé si la case contient une valeur
                    if self.grid.get_cell_value(coordinates) != '0':
                        self.grid.set_cell_state(coordinates, "locked")
                        print(f"The cell {coordinates} was locked")
                        is_grid_changed = True  # indique un changement de la grille
                    else:
                        print(f'The cell {coordinates} was NOT locked: empty cell')
                
                # Si la case est verrouillée
                case "locked":
                    # Mettre l'état de la case à déverrouillé
                    self.grid.set_cell_state(coordinates, "unlocked")
                    print(f"The cell {coordinates} was unlocked")
                    # indique un changement de la grille
                    is_grid_changed = True
                
                # Si la case est superverrouillée
                case "superlocked":
                    # Afficher un message d'erreur dans la console
                    print(
                        f'The cell {coordinates} is superlocked, you cannot change its value while being in "playing" gam mode')
        
        # Si le mode de jeu est sur edition
        else:
            match self.grid.get_cell_state(coordinates):  # fonction match case
                # Si le mode de jeu est editeur
                case "unlocked":
                    # Mettre l'état de la case à superverrouillé si la case contient une valeur
                    if self.grid.get_cell_value(coordinates) != '0':
                        self.grid.set_cell_state(coordinates, "superlocked")
                        print(f"The cell {coordinates} was superlocked")
                        # indique un changement de la grille
                        is_grid_changed = True
                    else:
                        print(f"The cell {coordinates} was NOT superlocked: empty cell")
                
                # Si la case est verrouillée
                case "locked":
                    # Mettre l'état de la case à deverrouillé
                    self.grid.set_cell_state(coordinates, "unlocked")
                    print(f"The cell {coordinates} was unlocked")
                    # indique un changement de la grille
                    is_grid_changed = True
                
                # Si la case est superverrouille
                case "superlocked":
                    # Mettre l'état de la case à déverrouillé
                    self.grid.set_cell_state(coordinates, "unlocked")
                    print(f"The cell {coordinates} was unlocked")
                    # indique un changement de la grille
                    is_grid_changed = True
        
        # ajoute la ou les action(s) dans l'historique si une modification a eu lieu
        if is_grid_changed:
            self.save_grid_in_history()
        # indique que la grille a été modifiée depuis le dernier enregistrement
        self.is_grid_saved = False
    
    def save_grid_in_history(self):
        """
        Sauvegarde la grille courante dans l'historique
        """
        
        # Si l'utilisateur est remonté dans l'historique, effacer les états de la grille qui ont été annulés
        if self.history_index < len(self.history) - 1:
            self.history = self.history[:self.history_index + 1]
        
        # copie la grille actuelle
        self.history.append((self.grid.copy(), self.selected_cell))
        # redefini l'index
        self.history_index = len(self.history) - 1
    
    def is_history_move_possible(self, move: str) -> bool:
        """
        Permet de savoir si il est possible d'aller en avant ou en arrière dans l'historique
        :param move: valeurs possible `forward` ou `backward`
        """
        
        # Test préconditions
        test_errors(history_move=move)
        
        if move == "backward":
            return self.history_index != 0  # boolean
        
        elif move == "forward":
            return self.history_index != len(self.history) - 1  # boolean
    
    def move_index_history(self, move: str):
        """
        Permet de se déplacer dans l'historique.
        move = "backward"  : Annule la dernière action
        move = "forward"   : Rétablie l'action annulée
        """
        
        # Test préconditions
        test_errors(history_move=move)
        
        if move == "backward":
            self.history_index -= 1
            
            if self.history_index < 0:
                self.history_index = 0
        
        elif move == "forward":
            self.history_index += 1
            
            if self.history_index >= len(self.history):
                self.history_index = len(self.history) - 1
        
        # remplace la grille actuelle par la grille de l'historique
        self.grid = self.history[self.history_index][0].copy()
        self.selected_cell = self.history[self.history_index][1]
        
        # effectue la verification des cases en conflit
        self.verify_grid()
        self.update_cells_conflicting_state()
    
    def clear_history(self):
        """
        Vide l'historique.
        Fonction utilisée lors du chargement / génération d'une nouvelle grille / ouverture d'une nouvelle grille
        """
        
        self.history = [(self.grid.copy(), (-1, -1))]
        self.history_index = 0
    
    def new_empty_grid(self, grid_size: int):
        """
        Génère une nouvelle grille vide avec la taille indiquée
        Renvois True si la grille a bien été créé, et False si l'action a été annulée
        """
        
        # Test préconditions
        test_errors(sudoku_size=grid_size)
        
        # messagebox pour demander à l'utilisateur si il souhaite enregistrer la grille et que la grille n'est ni enregistrée ni vide
        if not self.is_grid_saved and not self.grid.is_empty():
            do_save = askyesnocancel(
                "Sauvegarder la grille",
                f"Une nouvelle grille de taille {grid_size}x{grid_size} va être générer et les données de la grille actuelle seront définitivement perdues.\nVoulez-vous sauvegarder la grille ?"
            )
            
            # si l'utilisateur a cliqué sur cancel, sur la croix ou sur non
            if do_save is None:
                return False
            
            # si l'utilisateur a cliqué sur ok
            if do_save:
                self.save_grid()
        
        # supprimer l'historique
        self.clear_history()
        # créé la nouvelle grille
        self.grid = Grid(grid_size)
        return True
    
    def open_grid(self):
        """
        Charge une grille à partir d'un fichier
        """
        
        # Ouvre une fenêtre de dialogue permettant à l'utilisateur de choisir le fichier à charger
        file_path = askopenfilename(
            initialdir="src/save_folder",
            initialfile="Grille_moyenne.sdk",
            title="Ouvrir",
            filetypes=[("Sudoku file", "*.sdk"), ("All files", "*")]
        )
        
        # Dans le cas où l'utilisateur n'a pas sélectionné de fichier
        if not file_path:
            # Affiche un message en console et ne fait rien d'autre
            print("No file selected")
            return
        
        # Récupère le contenu du fichier sélectionné
        with open(file_path, "r") as file:
            file_content = file.read()
        
        # Formate le contenu du fichier dans les variables grid_size, all_values et all_states
        
        # sépare la partie avec la taille de la grille de la partie avec la valeur de la partie avec les états
        file_content = file_content.split("\n\n")
        # récupère la taille de la grille
        grid_size = int(file_content[0])
        
        # récupère les valeurs
        all_values = [[value for value in line] for line in file_content[1].split("\n")]
        # récupère les états
        all_states = [[self.load_state_conversion[state] for state in line] for line in file_content[2].split("\n")]
        
        # Test postconditions
        test_errors(grid_size, list_values=all_values, list_states=all_states)
        
        # Remplace le contenu de la grille par le contenu lu dans le fichier
        self.grid.reset_attributes(grid_size, all_values, all_states)
        
        print("Grid succesfully opened")
        
        # indique que le contenu a étét enregistré
        self.is_grid_saved = True
        # vérifie la validité de la grille
        self.verify_grid()
        # supprime l'historique
        self.clear_history()
        # défini le mode a `joueur`
        self.set_game_mode("playing")
        # met à jour le titre
        self.game.update_title()
    
    def save_grid(self):
        """
        Enregistre la grille actuelle dans un fichier
        """
        
        # Récupère le chemin du fichier à sauvegarder
        filepath = asksaveasfilename(
            initialdir="src/save_folder/",
            initialfile='saved_sudoku.sdk',
            title=f"Enregistrer",
            filetypes=[("Sudoku file", "*.sdk")]
        )
        
        # Si l'utilisateur n'a rien  saisi, retourne None
        if not filepath:
            return
        
        # Formate les valeurs des cases de la grille en chaine de charactère
        all_values = "\n".join(["".join(line) for line in self.grid.get_all_values()])
        
        # Formate les états des cases de la grille en chaine de charactère
        all_states = "\n".join(
            ["".join([self.save_state_conversion[state] for state in line]) for line in self.grid.get_all_states()])
        
        all_content = str(self.grid.size) + "\n\n" + all_values + "\n\n" + all_states  # formate le fichier
        
        # Ecrit le contenu obtenu dans un fichier
        with open(filepath, "w") as file:
            file.write(all_content)
        
        # indique que la grille a été enregistrée
        self.is_grid_saved = True
        print("Grid saved succesfully")
    
    def is_valid(self) -> bool:
        """
        Renvoie True si la grille ne comporte aucune erreurs, et False si elle en comporte au moins une
        """
        
        # Pour toutes les organisations de grille possibles (en lignes, en colonnes et en carrés)
        for all_values in [self.grid.get_all_values_as(format) for format in ["lines", "columns", "squares"]]:
            
            # Parcourir les sous-listes de cet ensemble de valeurs
            for sub_all_values in all_values:
                
                # Pour toutes les valeurs de case possible
                for value in self.game.possible_values[:self.grid.size]:
                    
                    # Si la valeur apparait plusieur fois dans la sous-liste
                    if sub_all_values.count(value) > 1:
                        return False
        
        # Si aucun doublon n'a été trouvé, renvoyer True
        return True
    
    def verify_grid(self):
        """
        Enregistre dans la variable "self.conflicting_cells" l'ensemble des coordonnées des cases en conflit
        """
        
        tmp_conflicting_cells = list()  # Liste temporaire dans laquelle seront stockées les coordonnées des cases en conflits
        
        # Pour tous les formats possibles
        for format in ["lines", "columns", "squares"]:
            all_values = self.grid.get_all_values_as(format)
            all_coordinates = self.grid.get_all_coordinates_as(format)
            
            # Parcourir les coordonnées en x possibles
            for x in range(self.grid.size):
                
                # Récupérer les groupes de valeurs et de coordonnées correspondant
                group_values = all_values[x]
                groupe_coordinates = all_coordinates[x]
                
                # Pour toutes les valeurs possibles
                for value in self.game.possible_values[:self.grid.size]:
                    
                    # Si cette valeur apparait plusieur fois dans le groupe de valeurs
                    if group_values.count(value) > 1:
                        
                        # Enregistrer dans "tmp_conflicting_cells" les coordonnées des cases ayant la valeur doublon
                        for y in range(self.grid.size):
                            if group_values[y] == value and not groupe_coordinates[y] in tmp_conflicting_cells:
                                tmp_conflicting_cells.append(groupe_coordinates[y])
                    
                    # Si la valeur n'apparait pas plusieur fois dans le groupe de valeurs
                    else:
                        # Supprimer les coordonnées des cases ayant cette valeur de la variable "self.conflicting_cells"
                        for y in range(self.grid.size):
                            if group_values[y] == value and groupe_coordinates[y] in self.conflicting_cells:
                                self.conflicting_cells.remove(groupe_coordinates[y])
        
        # Mise en commun de "tmp_conflicting_cells" et de "self.conflicting_cells"
        for x in range(self.grid.size):
            for y in range(self.grid.size):
                
                if (x, y) in tmp_conflicting_cells and not (x, y) in self.conflicting_cells:
                    self.conflicting_cells.append((x, y))
        
        # met à jour les cases en conflit
        self.update_cells_conflicting_state()
    
    def update_cells_conflicting_state(self):
        """
        Met à jour la variable "is_in_conflict" de toutes les cases de la grille
        """
        
        for x in range(self.grid.size):
            for y in range(self.grid.size):
                # indique si la case est en conflit // "(x, y) in self.conflicting_cells" retourne un boolean
                self.grid.set_cell_conflicting_state((x, y), (x, y) in self.conflicting_cells)
    
    def generate_grid(self, frequency_cell_removed: float, do_show_messagebox: bool = True):
        """
        Génère une grille de sudoku
        :param frequency_cell_removed: fréquence / proportion des cases a retirer à chaque boucle ne donnant pas de résultat
        :param do_show_messagebox: afficher ou non un message à la fin pour indiquer et résumr la génération
        met à jour self.grid
        """
        
        # Test préconditions
        test_errors(frequency = frequency_cell_removed)
        print("generating...")
        
        # met à jour le titre de la fenêtre
        self.game.update_title("Génération ...")
        
        # indique que la génération est en cours
        self.game.is_processing = True
        
        starting_time = time.time()
        cell_frequency = frequency_cell_removed

        # Génère une nouvelle grille vide, ne fait rien si l'action a été annulée
        if not self.new_empty_grid(self.grid.size):
            return False
        
        # génère une grille complète et valide aléatoirement
        self.backtracking_solving(False, do_choice_randomly=True)
        
        if self.game.do_quit:
            return
        
        # Pochoir (test plusieurs configurattion jusqu'a en trouver une correct)
        backup_grid = self.grid.get_all_values()  # copie la grille (sauvegarde)
        # définir les cases à laisser
        number_of_cells_to_remove = round((cell_frequency) * self.grid.cells_count)
        resolved = False
        # boucle qui attend la résolution de la grille
        while not resolved:
            # liste des cases modifiées
            cells_to_remove_list = list()
            cell = (0, 0)
            start = True
            # balaye sur le nombre de cases à balayer
            for _ in range(number_of_cells_to_remove):
                # start est la conditon pour démarrer le while, test si la case est déjà utilisée
                while self.grid.get_cell_value(cell) == "0" or start:
                    start = False
                    # créé une case
                    cell = (random.randint(0, self.grid.size - 1), random.randint(0, self.grid.size - 1))
                
                # place la valeur
                self.grid.set_cell_value(cell, "0")
                # met à jour l'affichage et la mise à jour de la fenêtre // empeche le gel de la fenêtre
                self.game.cell_update(cell, False)
                # ajoute la case à la liste des cases modifiées
                cells_to_remove_list.append(cell)
            
            # verifie l'existance d'une seule solution
            solutions_numbers = self.count_possible_solutions(True)
            if self.game.do_quit:
                return False
            
            # si il y a une seule solution
            if solutions_numbers == 1:
                # balaye sur toutes les solutions
                for cell in self.grid.get_all_coordinates_simple_list():
                    # si la case est dans la liste des cases moddifiées
                    if cell in cells_to_remove_list:
                        # mettre la valeur à 0
                        self.grid.set_cell_value(cell, "0")
                        # mettre à jour la fenetre
                        self.game.cell_update(cell, False)
                    
                    else:
                        # superveroruiller la case
                        self.grid.set_cell_state(cell, "superlocked")
                        # mettre à jour la fenetre
                        self.game.cell_update(cell, False)
                    # indique que la grille est résolu
                    resolved = True
            
            else:
                # restaure la grille
                self.grid.set_content(
                    backup_grid,
                    list_states=[['unlocked' for _ in range(self.grid.size)] for _ in range(self.grid.size)]
                )
                self.game.update(False)
                # définir les cases à laisser
                # augmente de X% le taux de cases laissées (diminue le nombre de boucle nécessaire, accélère la génération)
                cell_frequency -= frequency_cell_removed
                # calcul le nombre de case à supprimer
                number_of_cells_to_remove = round((cell_frequency) * self.grid.cells_count)
        
        # defini le mode de jeu à joueur
        self.set_game_mode("playing")
        # met à jour le boutton "mode de jeu"
        self.game.graphism.update_game_mode_button()
        # met à jour le titre de la fenêtre
        self.game.update_title()
        # met à jour l'affichage
        self.game.graphism.display_game_elements()
        
        # indique que la génération est finie
        self.game.is_processing = False
        
        # calcul temps d'execution - informatif
        executing_time = round(time.time() - starting_time, 2)
        # nombre de cases / cases restantes
        remaining_cells = self.grid.cells_count - number_of_cells_to_remove
        # pourcentaage de cases restantes
        percentage = round(100 - ((number_of_cells_to_remove / self.grid.cells_count) * 100), 2)
        # affichage console
        print(f'Temps de génération: {executing_time}s - {remaining_cells} cases restantes ({percentage}%)')
        # affichage d'un message indiquant la fin de la génération
        if do_show_messagebox:
            showinfo(
                "Génération terminée",
                f"{' ' * 20}Génération effectué avec succès\n"
                f"{' ' * 20}temps d'éxecution: {executing_time}s\n"
                f"{' ' * 20}cases restantes: {remaining_cells} cases ({percentage}%)\n"
                f"{' ' * 100}"
            )
        
        # Sauvegarde de la grille dans l'historique
        self.save_grid_in_history()
    
    def solve_grid(self, do_display: bool = True):
        """
        Résout le Sudoku, tient compte des valeurs entrées pas l'utilisateur, seulement les cases présentes originalement
        """
        
        # Test préconditions
        test_errors(boolean = do_display)
        
        # enregistrmeent du temps de départ
        starting_time = time.time()
        
        # mise à jour du titre
        self.game.update_title("Résolution ...")
        
        # message console indiquand le début de la résolution
        print('solving...')
        
        # défini le mode de jeu sur joueur
        self.set_game_mode("playing")
        # Met à jour le boutton "mode de jeu"
        self.game.graphism.update_game_mode_button()
        # reset la grille
        self.clear_inputs(False)
        
        # indique si le sudoku est resolvable par un message dans la console
        if not self.is_valid():
            print("Invalid input, cannot solve the sudoku")
        
        elif self.backtracking_solving(do_display):
            print("Sudoku solved successfully")
            print(f'Solving executing time: {round(time.time() - starting_time, 2)}s')
        
        else:
            print("Cannot solve the sudoku")
            print(f'Solving executing time: {round(time.time() - starting_time, 2)}s')
        
        # Enregistrer la grille dans l'historique
        self.save_grid_in_history()
        
        # met à jour le titre
        self.game.update_title()
    
    def solve_generated_grid(self):
        """
        Résout le Sudoku, ne tient pas compte des valeurs entrées pas l'utilisateur, seulement les cases présentes originalement
        """
        
        # renvois False si la grille contient des erreurs
        if not self.is_valid():
            return False
        
        # indique que la résolution est en cours
        self.game.is_processing = True
        
        # démarre la résolution (méthode récursive)
        result = self.backtracking_solving(False)
        
        # indique que la résolution est finie
        self.game.is_processing = False
        
        return result
    
    def clear(self):
        """
        supprime toutes les valeurs des cases autres que les superlocked et les locked
        """
        
        # indique si la grille a été modifiée
        is_grid_changed = False
        
        # balaye toutes les cases
        for x in range(self.grid.size):
            for y in range(self.grid.size):
                # verifie que la case soit déverrouillée et que la valeur soit différente de 0 (case vide)
                if self.grid.get_cell_state((x, y)) == "unlocked" and self.grid.get_cell_value((x, y)) != "0":
                    # définie la valeur à zéro
                    self.grid.set_cell_value((x, y), "0")
                    # indique qu'une modification a été faite
                    is_grid_changed = True
        
        # si un changmeent a eu lieu
        if is_grid_changed:
            print("\nThe grid was cleared")
            # enregistrer le cha gement dans l'historique
            self.save_grid_in_history()
            # indiquer qu'une modification a eu lieu depuis le dernier enregistrmeent
            self.is_grid_saved = False
    
    def clear_inputs(self, do_save_in_history: bool):
        """
        Supprime toutes les valeurs entrées par l'utilisateur
        :param do_save_in_history: si l'action doit être entregistrée dans l'historique
        """
        
        # Test préconditions
        test_errors(boolean=do_save_in_history)
        
        # indique si la grille a été modifiée
        is_grid_changed = False
        # balaye toutes les cases
        
        for x in range(self.grid.size):
            for y in range(self.grid.size):
                # vérifie que le mode de jeu soit bien editeur et que la case soit différente de superveroruillée
                if self.game_mode == "editing" or self.grid.get_cell_state((x, y)) != "superlocked":
                    # vérifie si la case est verrouillée ou superverrouillé ett que la valeur est différent de 0 (case vide)
                    if self.grid.get_cell_state((x, y)) != "unlocked" or self.grid.get_cell_value((x, y)) != "0":
                        # bascule l'état à déverrouillé
                        self.grid.set_cell_state((x, y), "unlocked")
                        # met l'état à zéro (case vide)
                        self.grid.set_cell_value((x, y), '0')
                        # indiquer qu'une modification a eu lieu depuis le dernier enregistrmeent
                        is_grid_changed = True
        
        # si un changement a eu lieu et que l'on doit enregistrer l'historique
        if is_grid_changed and do_save_in_history:
            print("\nThe grid was cleared")
            # enregistrer le ou les changement(s) dans l'historique
            self.save_grid_in_history()
            # indiquer qu'une modification a eu lieu depuis le dernier enregistrmeent
            self.is_grid_saved = False
    
    def put_obvious_solutions(self, do_display: bool = True) -> list[tuple[int, int]]:
        """
        Met dans la grille les chiffres évidentes (les case où il n'y a qu'une valeur possible)
        Renvoi la liste des coordonnées des cases modifiées
        """

        # liste des cases modifiées
        modified_cells = list()
        # boucle infinie (arrêt par break)
        while True:
            # indique l'arret de l'algorithme
            is_algorithm_finished = True

            # liste des cases à vérifier
            cells_to_check = self.grid.get_all_empty_cells()
            
            # balaye dans les cases à veéifier
            for cell_coordinates in cells_to_check:
                # récupère les valeurs possibles la case
                cell_possible_values = self.grid.get_possible_values(cell_coordinates)
                # test si lil n'y a qu'une solution
                if len(cell_possible_values) == 1:
                    # defini la valeur
                    self.grid.set_cell_value(cell_coordinates, cell_possible_values[0])
                    # met à jour l'affichage // anti-gel de la fenêtre
                    self.game.cell_update(cell_coordinates, do_display=do_display)
                    # ajoute les coordonnées à la liste des cases modifiées
                    modified_cells.append(cell_coordinates)
                    # inidque que l'algorithme n'est pas fini
                    is_algorithm_finished = False
            
            # si l'algorithme est fini, quitte la boucle
            if is_algorithm_finished:
                break
        
        # retourne la lliste des celllules modifiées
        return modified_cells
    
    def count_possible_solutions(self, do_stop_sup_1: bool = False) -> int:
        """
        Fonction récursive qui compte le nombre de solutions possibles dans le sudoku
        Renvoi -1 si la fenêtre doit être fermée, et le nombre de solutions possibles dans les autres cas
        :param: do_stop_sup_1: indique si le programme doit s'arreter si il dépasse 1 (indique rapidement si il y a plus d'une solution)
        """
        
        # indique que la fenêtre doit être fermée
        if self.game.do_quit:
            return -1
        
        # nombre de solutions trouvées
        encountered_solutions = 0
        
        # récupère les valeurs possibles de toutes les cases [liste des valeurs possibles, coordonnées]
        cells_to_fill = [
            [self.grid.get_possible_values((x, y)), (x, y)]
            if self.grid.get_cell_state((x, y)) != 'superlocked' and self.grid.get_cell_value((x, y)) == '0'
            else []
            for y in range(self.grid.size) for x in range(self.grid.size)
        ]
        
        # supprime tous les éléments [] = cases superlocked ou cases avec déjà des valeurs
        cells_to_fill = list(filter(lambda x: x != [], cells_to_fill))
        
        # si aucune solution n'est trouvée retourne 0, empeche des opération de tri inutiles
        if len(cells_to_fill) == 0:
            return 0
        
        # tri les cases de la liste en fonction du nombre de valeurs possibles
        minimum = min([len(element[0]) for element in cells_to_fill])
        cells_to_fill = list(filter(lambda x: len(x[0]) == minimum, cells_to_fill))
        
        # Récupère les coordonnées et valeurs possibles de la cases ayant le moins de valeurs possibles
        cell_possible_values, cell_coordinates = cells_to_fill[0]
        
        # Pour chaque valeur possible de la case en question
        for value in cell_possible_values:
            # Mettre la valeur dans la case
            self.grid.set_cell_value(cell_coordinates, value)
            # mettre à jour l'affichage // empêche le frezze de la fenêtre
            self.game.cell_update(cell_coordinates, False)
            
            # Si la grille est complète et valide, ajouter 1 au compteur des solutions rencontrées
            if self.grid.is_full():
                encountered_solutions += 1
                # si la limitation à plus d'une réponse est passé en arguments, retourné le nombre de solutions
                if do_stop_sup_1 and encountered_solutions > 1:
                    return encountered_solutions
            
            else:
                if do_stop_sup_1 and encountered_solutions > 1:
                    return encountered_solutions
                # ajouter le nombre de solutions trouvées par la méthode récursive
                encountered_solutions += self.count_possible_solutions(do_stop_sup_1)
                if self.game.do_quit:
                    # Arrêter le programme
                    return -1
                
                if do_stop_sup_1 and encountered_solutions > 1:
                    return encountered_solutions
            
            # si aucun des tests précedent n'est positif, définir la valeur de la case à zéro
            self.grid.set_cell_value(cell_coordinates, "0")
            # mettre à jour l'affichage // anti-gel
            self.game.cell_update(cell_coordinates, False)
        
        # retourner le nombre de solutions
        return encountered_solutions
    
    def backtracking_solving(
        self, do_display: bool,
        do_choice_randomly: bool = False,
        last_cell_coordinates: tuple[int, int] = None,
        grid_possibilities: list[list[list, tuple[int, int]]] = None
    ) -> bool:
        """
        Fonction récursive qui résout le Sudoku en testant toutes les possibilités
        Renvoi True si la grille courante est possible à résoudre, et False si elle ne l'est pas
        :param do_choice_randomly: choisi les valeurs de mannnière aléatoire parmi les cases ayant le moins de possibilité et les valeurs de manière aléatoire, ne ralenti pas la résolutionn
        :param last_cell_coordinates: coordonnées de la dernière case modifiée
        :param grid_possibilities: copie formatée de la grille pour avoir les possibilitées pour chaque case
        """
        
        # Si l'utilisateur ferme la fenêtre
        if self.game.do_quit:
            # Arrêter le programme
            return False
        
        if self.grid.is_full():
            # Si la grille est remplie, renvoyer True si elle est résolue, et False si la résolution n'est pas valide
            return self.is_valid()
        
        # met les valeurs évidentes des cases
        modified_cells_coordinates = self.put_obvious_solutions(do_display)
        
        # test si il s'agit du premier appel de la méthode OU que la grille fait neuf ou moins, si ce n'est pas le cas, utilise une méthode de résolution alternative (trop longue en 9x9
        if not last_cell_coordinates or self.grid.size <= 9:
            # récupère les valeurs possibles de toutes les cases [liste des valeurs possibles, coordonnées] si c'est la première itération
            cells_to_fill = [
                [self.grid.get_possible_values((x, y)), (x, y)]
                if self.grid.get_cell_state((x, y)) != 'superlocked' and self.grid.get_cell_value((x, y)) == '0'
                else []
                for y in range(self.grid.size) for x in range(self.grid.size)
            ]
            # défini grid_possibilities
            grid_possibilities = cells_to_fill
        
        else:
            # récupère les valeurs possibles de toutes les cases qui sont sur la même ligne, colonne ou carré que la dernière case modifiée et/ou sur la même ligne, colonne, carrée que la dernière case modifiée (last_cell_coordinates)
            # défini grid_possibilities
            grid_possibilities = grid_possibilities.copy()
            # liste des cases en cours de modification/ déjà modifiée par cette fonction
            coordinates_list: list[tuple[int, int]] = list()
            # balaye dans la dernière case + les cases modifiées par put_obvious_solutions
            for actual_coordinates in [last_cell_coordinates] + modified_cells_coordinates:
                # balaye dans les diférents formats, les lignes, les colonnes et les carrés
                for format in ["columns", "lines", "squares"]:
                    # ballaye dans les coordonnées des cases de ces formats
                    for coordinates in self.grid.get_group_coordinates(actual_coordinates, format):
                        # test si la coordonnée n'est PAS dans la liste des cases en cours de modification/ déjà modifiée
                        if coordinates not in coordinates_list:
                            # ajouter les coordonnées à cette lliste
                            coordinates_list.append(coordinates)
                            # récupérer les valeurs possible pour cette case
                            possible_values = self.grid.get_possible_values(coordinates)
                            # si la case n'est pas superverrouille et qu'elle est vide
                            if self.grid.get_cell_state(coordinates) != 'superlocked' and self.grid.get_cell_value(
                                    coordinates) == '0':
                                # modifier les valeurs possible pour cette case
                                grid_possibilities[coordinates[1] * self.grid.size + coordinates[0]] = [possible_values,
                                                                                                        coordinates]
                            else:
                                # si la case est superverrouillé ou qu'elle contient déjà une valeur, aucune valeur n'est possible
                                grid_possibilities[coordinates[1] * self.grid.size + coordinates[0]] = []
            
            # indique que les cases à rmeplir sont désormais les valeurs de grid_possibilities
            cells_to_fill = grid_possibilities
        
        # supprime tous les éléments [] = cases superlocked ou cases avec déjà des valeurs
        cells_to_fill = list(filter(lambda x: x != [], cells_to_fill))
        
        # Si il n'y a pas de case vide
        if len(cells_to_fill) == 0:
            # Renvoyer la validité du sudoku obtenu
            return self.is_valid()
        
        # tri les cases de la liste en fonction du nombre de valeurs possibles
        minimum = min([len(element[0]) for element in cells_to_fill])
        cells_to_fill = list(filter(lambda x: len(x[0]) == minimum, cells_to_fill))
        
        # arrangement des cases aléatoires dans le nombre de solution minimales // n'impacte pas la vitesse de  résolution
        if do_choice_randomly:
            random.shuffle(cells_to_fill)
        
        # Récupère les coordonnées et valeurs possibles de la cases ayant le moins de valeurs possibles
        cell_possible_values, cell_coordinates = cells_to_fill[0]
        
        # arrangement des valeurs aléatoires dans les valeurs possibles // n'impact pas la vitesse de résolution
        if do_choice_randomly:
            random.shuffle(cell_possible_values)
        
        # Pour toutes les valeurs possibles de la case
        for value in cell_possible_values:
            # Met la valeur de la case à "value"
            self.grid.set_cell_value(cell_coordinates, value)
            # indique que la case contient une valeur, et donc qu'il n'y a plus la possibilité de mettre une valeur pour cette case
            grid_possibilities[cell_coordinates[1] * self.grid.size + cell_coordinates[0]] = []
            
            # affiche la valeur // anti freeze de lla fenêtre
            self.game.cell_update(cell_coordinates, do_display)
            
            # s'appelle lui-meme (fonction récursive)
            # Si la fonction récursive renvoi une réponse positive, alors faire remonter la réponse, cela signifie qu'un des appel d'une fonction inférieure a trouvé une solution
            if self.backtracking_solving(do_display, last_cell_coordinates=cell_coordinates,
                                         grid_possibilities=grid_possibilities):
                return True
            
            # Sinon retirer les valeurs mise dans les cases
            else:
                if self.game.do_quit:
                    # Arrêter le programme
                    return False
                
                # remettre à zéro la case modifiée
                self.grid.set_cell_value(cell_coordinates, '0')
                # mettre à jour l'affichage // anti-freeze
                self.game.cell_update(cell_coordinates, do_display)
        
        # Enlève toutes les valeurs "évidentes" mises au préalable
        for coordinates in modified_cells_coordinates:
            self.grid.set_cell_value(coordinates, '0')
        
        # Renvoyer False car cela signifie qu'aucune solution n'a été trouvé
        return False
