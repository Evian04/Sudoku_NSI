import os

def test_errors(sudoku_size = 0, **arguments):
    """
    Fonction permettant de gérer les erreures potentielles lors de l'exécution du programme
    """
    
    possible_sudoku_sizes = [4, 9, 16]
    possible_values = "123456789ABCDEFG"
    all_config_keys = ["texture_pack", "do_display_conflicts", "do_display_during_solving"]
    
    assert type(sudoku_size) == int, f'The "sudoku_size" argument must be an integer (type : {type(sudoku_size)})'
    if sudoku_size != 0:
        assert sudoku_size in possible_sudoku_sizes, \
            f'The "sudoku_size" argument must be 4, 9 or 16 (value : {sudoku_size})'
    
    if "boolean" in arguments:
        boolean = arguments["boolean"]
        
        assert type(boolean) == bool, f"This argument must be a boolean (type : {type(boolean)})"
    
    if "coordinates" in arguments:
        assert sudoku_size != 0, 'You must pass a value for "sudoku_size" argument in order to verify "coordinates"'
        
        coordinates = arguments["coordinates"]
        
        assert type(coordinates) == tuple, f'The "coordinates" arguments must be a tuple (type : {type(coordinates)})'
        assert type(coordinates[0]) == int and type(coordinates[1]) == int, \
            f'The "coordinates" argument must contains intgers (value : {coordinates})'
        assert 0 <= coordinates[0] < sudoku_size and 0 <= coordinates[1] < sudoku_size, \
            f'The "coordinates" argument must be contains integers between 0 and grid_size - 1 (value : {coordinates})'
    
    if "value" in arguments:
        assert sudoku_size != 0, 'You must pass a value for the "sudoku_size" argument in order to verify "value"'
        
        value = arguments["value"]
        
        assert type(value) == str, f'The "value" argument must be a string (type : {type(value)})'
        assert value in "0" + possible_values[:sudoku_size], f'The "value" argument must be in "possible_values" (value : {value}, possible values : {possible_values[:sudoku_size]})'
    
    if "state" in arguments:
        state = arguments["state"]
        
        assert type(state) == str, f'The "state" argument must be a string (type : {state})'
        assert state in ["unlocked", "locked", "superlocked"], \
            f'The "state" argument must be "unlocked", "locked" or "superlocked" (value : {state})'
    
    if "color" in arguments:
        color = arguments["color"]
        
        assert type(color) == tuple, f'The "color" argument must be a tuple (type : {type(color)})'
        assert len(color) == 3, f'The "color" argument must have a length of 3 (length : {len(color)})'
        assert 0 <= color[0] <= 255, f'The "color" argument must contains integers between 0 and 255 (values : {color})'
        assert 0 <= color[1] <= 255, f'The "color" argument must contains integers between 0 and 255 (values : {color})'
        assert 0 <= color[2] <= 255, f'The "color" argument must contains integers between 0 and 255 (values : {color})'
    
    if "format" in arguments:
        format = arguments["format"]
        
        assert type(format) == str, f'The "format" argument must be a string (type : {type(format)})'
        assert format in ["lines", "columns", "squares"], \
            f'The "format" argument must be "lines", "columns" or "squares" (value : {format})'
    
    if "frequency" in arguments:
        frequency = arguments["frequency"]
        
        assert type(frequency) == float, f'The "frequency" argument must be a float (type : {type(frequency)})'
        assert 0 <= frequency <= 1, f'The "frequency" argument must be between 0 and 1 (value : {frequency})'

    if "direction" in arguments:
        direction = arguments["direction"]
        
        assert type(direction) == str, f'The "direction" argument must be a string (type : {type(direction)})'
        assert direction in ["left", "right", "up", "down"], f'The "direction" argument must be "left", "right", "up" or "down" (value : {direction})'
    
    if "history_move" in arguments:
        history_move = arguments["history_move"]
        
        assert type(history_move) == str, f'The "history_move" argument must be a string (type : {type(history_move)})'
        assert history_move in ["forward", "backward"], f'The "history_move" argument must be "forward" or "backward" (value : {history_move})'
    
    if "game_mode" in arguments:
        game_mode = arguments["game_mode"]
        
        assert type(game_mode) == str, f'The "game_mode" argument must be a string (type : {type(game_mode)})'
        assert game_mode in ["editing", "playing"], f'The "game_mode" argument must be "editing" or "playing" (value : {game_mode})'
    
    if "list_values" in arguments:
        assert sudoku_size, 'You must pass a value for the "sudoku_size" argument in order to verify "list_values"'
        
        list_values = arguments["list_values"]
        
        assert type(list_values) == list, f'The "list_values" argument must be a list (type : {type(list_values)})'
        assert len(list_values) == sudoku_size, \
            f'The "list_values" argument must have a length of {sudoku_size} (length : {len(list_values)})'
        
        for sub_list_values in list_values:
            assert type(sub_list_values) == list, f'The "list_values" argument must contains lists (value : {list_values})'
            assert len(sub_list_values) == sudoku_size, \
                f'The "list_values" argument must contains lists with lengths of {sudoku_size} (value : {list_values})'
            
            for value in sub_list_values:
                test_errors(sudoku_size, value = value)
    
    if "list_states" in arguments:
        assert sudoku_size != 0, 'You must pass a value for the "sudoku_size" argument in order to verify "list_states"'
        
        list_states = arguments["list_states"]
        
        assert type(list_states) == list, f'The "list_states" argument must be a list (type : {type(list_states)})'
        assert len(list_states) == sudoku_size, \
            f'The "list_states" argument must have a length of {sudoku_size} (length : {len(list_states)})'
        
        for sub_list_values in list_states:
            assert type(sub_list_values) == list, f'The "list_states" argument must contains lists (value : {list_states})'
            assert len(sub_list_values) == sudoku_size, \
                f'The "list_states" argument must contains lists that have lengths of {sudoku_size} (value : {list_states})'
            
            for state in sub_list_values:
                test_errors(state = state)
    
    if "list_coordinates" in arguments:
        assert sudoku_size != 0, 'You must pass a value for the "sudoku_size" argument in order to verify "list_coordinates"'
        
        list_coordinates = arguments["list_coordinates"]
        
        assert type(list_coordinates) == list, f'The "list_coordinates" argument must be a list (type : {type(list_coordinates)})'
        
        for coordinates in list_coordinates:
            test_errors(sudoku_size, coordinates = coordinates)
    
    if "config_file" in arguments:
        config_file = arguments["config_file"]
        
        assert type(config_file) == dict, f'The "config_file" argument must be a dict (type : {type(config_file)})'
        
        for config_key in all_config_keys:
            assert config_key in config_file, f'The "config_file" argument must contains the "{config_key}" key (value : {config_file})'

            test_errors(config_key = config_key, config_value = config_file[config_key])
    
    if "config_key" in arguments:
        config_key = arguments["config_key"]
        
        assert type(config_key) == str, f'The "config_key" argument must be a string (type : {type(config_key)})'
        assert config_key in all_config_keys, \
            f'The "config_key" argument must be "texture_pack", "do_display_conflicts" or "do_display_during_solvings" (value : {config_key})'

    if "config_value" in arguments:
        assert "config_key" in arguments, 'You must pass a value for the "config_key" argument in order to verify "config_value"'
        
        config_key = arguments["config_key"]
        config_value = arguments["config_value"]
        
        match config_key:
            
            case "texture_pack":
                assert type(config_value) == str, \
                    f'The "texture_pack" value of the config_file must be a string (type : {type(config_value)})'
                assert config_value in os.listdir("src/graphics"), \
                    f'The "texture_pack" value of the config_file must be in {os.listdir("src/graphics")} (value : {config_value})'
                    
            case "do_display_conflicts":
                assert type(config_value) == bool, \
                    f'The "do_display_conflicts" value of the config_file must be a boolean (type : {type(config_value)})'
                
            case "do_display_during_solvings":
                assert type(config_value) == bool, \
                    f'The "do_display_during_solvings" value of the config_file must be a boolean (type : {type(config_value)})'