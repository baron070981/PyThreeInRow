


def get_size(original_size, factor:float):
    """
    новый размер увеличенный или уменьшенный в несколько раз
    большая сторона увеличивается в factor раз
    меньшая сторона изменяется пропорционально
    """
    ...


def get_p_size(size:tuple, width:int=None, height:int=None):
    """
    ровый размер 
    """
    ...
    w, h = size
    if not width and not height:
        raise ValueError()
    if not width and not height:
        raise TypeError()
    if width is not None:
        k = width / w
        return width, round(k * h)
    elif height is not None:
        k = height / h
        return round(w * k), height
    return width, width









