def test_errors(sudoku_size = 9, **arguments):
    """
    Fonction permettant de gérer les erreures potentielles lors de l'exécution du programme
    """
    
    if "coordinates" in arguments:
        coordinates = arguments["coordinates"]
        
        assert type(coordinates) == tuple, f'The "coordinates" arguments must be a tuple (type : {type(coordinates)})'
        assert type(coordinates[0]) == int and type(coordinates[1]) == int, \
            f'The "coordinates" argument must contains intgers (value : {coordinates})'
        assert 0 <= coordinates[0] < sudoku_size and 0 <= coordinates[1] < sudoku_size, \
            f'The "coordinates" argument must contains integers between 0 and grid_size - 1 (value : {coordinates})'
    
    if "value" in arguments:
        value = arguments["value"]
        
        assert type(value) == int, f'The "value" argument must be an integer (type : {type(value)})'
        assert 0 <= value <= sudoku_size, f'The "value" argument must be between 0 and {sudoku_size} (value : {value})'
    
    if "color" in arguments:
        color = arguments["color"]
        
        assert type(color) == tuple, f'The "color" argument must be a tuple (type : {type(color)})'
        assert len(color) == 3, f'The "color" argument must have a length of 3 (length : {len(color)})'
        assert 0 <= color[0] <= 255, f'The "color" argument must contains integers between 0 and 255 (values : {color})'
        assert 0 <= color[1] <= 255, f'The "color" argument must contains integers between 0 and 255 (values : {color})'
        assert 0 <= color[2] <= 255, f'The "color" argument must contains integers between 0 and 255 (values : {color})'
    
    if "state" in arguments:
        state = arguments["state"]
        
        assert type(state) == str, f'The "state" argument must be a string (type : {state})'
        assert state in ["unlocked", "locked", "superlocked"], \
            f'The "state" argument must be "unlocked", "locked" or "superlocked" (value : {state})'
    
    if "format" in arguments:
        format = arguments["format"]
        
        assert type(format) == str, f'The "format" argument must be a string (type : {type(format)})'
        assert format in ["lines", "columns", "squares"], \
            f'The "format" argument must be "lines", "columns" or "squares" (value : {format})'
    
    if "list_values" in arguments:
        list_values = arguments["list_values"]
        
        assert type(list_values) == list, f'The "list_values" argument must be a list (type : {type(list_values)})'
        assert len(
            list_values) == sudoku_size, f'The "list_values" argument must have a length of {sudoku_size} (length : {len(list_values)})'
        
        for sub_list in list_values:
            assert type(sub_list) == list, f'The "list_values" argument must contains lists (value : {list_values})'
            assert len(sub_list) == sudoku_size, \
                f'The "list_values" argument must contains lists that have lengths of {sudoku_size} (value : {list_values})'
            
            for value in sub_list:
                assert type(value) == int, \
                    f'The "list_values" argument must contains lists that contains integers (value : {list_values})'
                assert 0 <= value <= sudoku_size, \
                    f'The "list_values" argument must contains lists that contains integers between 0 and {sudoku_size} (value : {list_values})'
    
    if "list_states" in arguments:
        list_states = arguments["list_states"]
        
        assert type(list_states) == list, f'The "list_states" argument must be a list (type : {type(list_states)})'
        assert len(list_states) == sudoku_size, \
            f'The "list_states" argument must have a length of {sudoku_size} (length : {len(list_states)})'
        
        for sub_list in list_states:
            assert type(sub_list) == list, f'The "list_states" argument must contains lists (value : {list_states})'
            assert len(sub_list) == sudoku_size, \
                f'The "list_states" argument must contains lists that have lengths of {sudoku_size} (value : {list_states})'
            
            for state in sub_list:
                assert type(state) == str, \
                    f'The "list_values" argument must contains lists that contains strings (value : {list_states})'
                assert state in ["unlocked", "locked", "superlocked"], \
                    f'The "list_values" argument must contains lists that contains "unlocked", "locked" or "superlocked" (value : {list_states})'
    
    if "grid_size" in arguments:
        sudoku_size = arguments["grid_size"]
        
        assert type(sudoku_size) == int, f'The "grid_size" argument must be a int (type : {type(sudoku_size)})'
        assert sudoku_size in [4, 9, 16, 25], \
            f'The "grid_size" argument must be 4, 9, 16, or 25 (value : {sudoku_size})'
