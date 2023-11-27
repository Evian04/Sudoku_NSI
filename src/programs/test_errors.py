def test_errors(**arguments):
    if "coords" in arguments:
        coordinates = arguments["coordinates"]
        
        if type(coordinates) != tuple:
            raise TypeError(f"The `coordinates` arguments must be a tuple (type : {type(coordinates)})")
        
        if type(coordinates[0]) != int or type(coordinates[1]) != int:
            raise TypeError(f"The `coordinates` argument must contains intgers (value : {coordinates})")
        
        if coordinates[0] < 0 or coordinates[0] > 8 or coordinates[1] < 0 or coordinates[1] > 8:
            raise ValueError(f"The `coordinates` argument must contains integers between 0 and 8 (value : {coordinates})")
        
    if "val" in arguments:
        value = arguments["value"]
        
        if type(value) != int:
            raise TypeError(f"The `value` argument must be an integer (type : {type(value)})")
        
        if value < 0 or value > 9:
            raise ValueError(f"The `value` argument must be between 0 and 9")
    
    if "col" in arguments:
        color = arguments["col"]
        
        if type(color) != tuple:
            raise TypeError(f"The `color` argument must be a tuple (type : {type(color)})")
        
        if len(color) != 3:
            raise ValueError(f"The `color` argument must have a length of 3 (length : {len(color)})")
        
        for value in color:
            if value < 0 or value > 255:
                raise ValueError(f"The `color` argument must contains integers between 0 and 255 (values : {color})")