
def get_neighbors(size:tuple[int, int], row:int, column:int):
    """
    нахождение соседних позиций в матрице. только сверху, снизу, справа, слева
    size: tuple[int, int] - (rows, rolumns)
    """
    height, width = size
    top = (row - 1, column) if row > 0 else None
    right = (row, column + 1) if column < width-1 else None
    bottom = (row + 1, column) if row < height-1 else None
    left = (row, column-1) if column > 0 else None
    neighbors = tuple(filter(lambda x: x is not None, [top, right, bottom, left]))
    return neighbors

def get_identical_elements(matrix:list[list[any]], comparison_func:object=lambda x, y: x == y):
    """
    поиск трех и более подряд одинаковых значений
    возвращает кортеж с индексами одинаковых значений
    по горизонтали и вертикали
    сравнение значений осуществляетса comparison_func если она передана в параметр
    если нет, то __eq__
    """
    elements = set()
    for i, row in enumerate(matrix):
        for j,col in enumerate(row[:-2]):
            if any(map(lambda x: x is None, row[j:j+3])):
                continue
            if all(map(lambda x: comparison_func(x, col), row[j+1:j+3])):
                elements.add((i, j))
                elements.add((i, j+1))
                elements.add((i, j+2))
            
    for i in range(len(matrix[0])):
        coords = [*map(lambda x: (x, i), range(len(matrix)))]
        for j in range(len(coords)-2):
            r,c = coords[j]
            val = matrix[r][c]
            current_elements = list(map(lambda x: matrix[x[0]][x[1]], coords[j:j+3]))
            if any(map(lambda x: x is None, current_elements)): continue
            if all(map(lambda x: comparison_func(val, x), current_elements[1:])):
                elements.add(coords[j])
                elements.add(coords[j+1])
                elements.add(coords[j+2])
    
    return tuple(elements)







if __name__ == "__main__":
    ...
    a = [
        [1,2,3,4,3,3,3,],
        [1,1,2,3,4,5,6,],
        [1,1,1,2,3,4,4,],
        [1,2,1,1,1,3,3,],
    ]
    test_res = [
        (0,4), (0,5), (0,6), (2,0), (2,1), (2,2),
        (3,2), (3,3), (3,4), 
        (0,0), (1,0), (3,0),
    ]

    neighbors1 = get_neighbors((4, 7), 1, 1)
    neighbors2 = get_neighbors((4, 7), 0, 0)
    neighbors3 = get_neighbors((4, 7), 3, 2)

    assert (3, 3) not in neighbors1, "Error 1"
    assert (1, 1) not in neighbors1, "Error 1"
    assert (0, 1) in neighbors1, "Error 1"

    test_res.sort()
    i = get_identical_elements(a)
    assert len(test_res) == len(i), "Списки не равны по длинне"
    assert test_res == sorted(i), "Значения в списках разные"
    print("Тесты пройдены")

