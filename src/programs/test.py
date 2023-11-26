result = list()
for square_x in range(0, 9, 3):  # avance de 3 index à la fois (un carré) en x
    for square_y in range(0, 9, 3):  # avance de 3 index à la fois (un carré) en y
        square = list()  # liste de tous les éléments d'un carré
        for y in range(square_y, square_y + 3):  # balaye tous les y dans le carré
            for x in range(square_x, square_x + 3):  # balaye tous les x dans le carré
                #get valeu value
                square.append((x, y))
        result.append(square)
print(result)