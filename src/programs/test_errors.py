def test_errors(**arguments):
    
    if "coordinates" in arguments:
        coordinates = arguments["coordinates"]
        
        if type(coordinates) != tuple:
            raise TypeError(f"The `coordinates` arguments must be a tuple (type : {type(coordinates)})")
        
        if type(coordinates[0]) != int or type(coordinates[1]) != int:
            raise TypeError(f"The `coordinates` argument must contains intgers (value : {coordinates})")
        
        if coordinates[0] < 0 or coordinates[0] > 8 or coordinates[1] < 0 or coordinates[1] > 8:
            raise ValueError(f"The `coordinates` argument must contains integers between 0 and 8 (value : {coordinates})")
        
    if "value" in arguments:
        value = arguments["value"]
        
        if type(value) != int:
            raise TypeError(f"The `value` argument must be an integer (type : {type(value)})")
        
        if value < 0 or value > 9:
            raise ValueError(f"The `value` argument must be between 0 and 9")
    
    if "color" in arguments:
        color = arguments["color"]
        
        if type(color) != tuple:
            raise TypeError(f"The `color` argument must be a tuple (type : {type(color)})")
        
        if len(color) != 3:
            raise ValueError(f"The `color` argument must have a length of 3 (length : {len(color)})")
        
        for value in color:
            if value < 0 or value > 255:
                raise ValueError(f"The `color` argument must contains integers between 0 and 255 (values : {color})")

    if "state" in arguments:
        state = arguments["state"]
        
        if type(state) != str:
            raise TypeError(f"The `state` argument must be a string (type : {state})")
        
        if not state in ["unlocked", "locked", "superlocked"]:
            raise ValueError(f'The `state` argument must be  "unlocked", "locked" or "superlocked" (value : {state})')
        
    if "list_values" in arguments:
        list_values = arguments["list_values"]
        
        if type(list_values) != list:
            raise TypeError(f"The `list_values` argument must be a list (type : {type(list_values)})")
        
        if len(list_values) != 9:
            raise ValueError(f"The `list_values` argument must have a length of 9 (length : {len(list_values)})")
        
        for sub_list in list_values:
            if type(sub_list) != list:
                raise TypeError(f"The `list_values` argument must contains lists (value : {list_values})")
            
            if len(sub_list) != 9:
                raise ValueError(f"The `list_values` argument must contains lists that have lengths of 9 (value : {list_values})")
            
            for value in sub_list:
                if type(value) != int:
                    raise TypeError(f"The `list_values` argument must contains lists that contains integers (value : {list_values})")
                
                if value < 0 or value > 9:
                    raise ValueError(f"The `list_values` argument must contains lists that contains integers between 0 and 9 (value : {list_values})")
                
    if "list_states" in arguments:
        list_states = arguments["list_states"]
        
        if type(list_states) != list:
            raise TypeError(f"The `list_states` argument must be a list (type : {type(list_states)})")
        
        if len(list_states) != 9:
            raise ValueError(f"The `list_states` argument must have a length of 9 (length : {len(list_states)})")
        
        for sub_list in list_states:
            if type(sub_list) != list:
                raise TypeError(f"The `list_states` argument must contains lists (value : {list_states})")
            
            if len(sub_list) != 9:
                raise ValueError(f"The `list_states` argument must contains lists that have lengths of 9 (value : {list_states})")
            
            for state in sub_list:
                if type(state) != str:
                    raise TypeError(f"The `list_values` argument must contains lists that contains strings (value : {list_states})")
                
                if not state in ["unlocked", "locked", "superlocked"]:
                    raise ValueError(f'The `list_values` argument must contains lists that contains "unlocked", "locked" or "superlocked" (value : {list_values})')