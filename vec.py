def add(a, b):
    x1, y1 = a
    x2, y2 = b
    return x1 + x2, y1 + y2


def subtract(a, b):
    x1, y1 = a
    x2, y2 = b
    return x1 - x2, y1 - y2


def in_bounds(vector, bounds):
    (min_x, min_y), (max_x, max_y) = bounds
    x, y = vector
    return max_x >= x >= min_x and max_y >= y >= min_y


def constrain(vector, bounds):
    if in_bounds(vector, bounds):
        return vector

    (min_x, min_y), (max_x, max_y) = bounds
    x, y = vector
    x = ((x - min_x) % (max_x + 1 - min_x)) + min_x
    y = ((y - min_y) % (max_y + 1 - min_y)) + min_y
    return x, y


def invert(vector):
    x, y = vector
    return x * -1, y * -1
