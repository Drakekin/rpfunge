import vec


class TwoDimensionalLaheySpace(object):
    def __init__(self):
        self.storage = {}
        self.pointers = []

    def normalise(self, coord):
        return vec.constrain(coord, self.extents())

    def tick(self):
        pointers = self.pointers
        self.pointers = []
        for pointer in pointers:
            cont = True
            alive = True
            while cont:
                cont, alive = pointer.tick()
            if alive:
                self.pointers.append(pointer)

    def lahey_constrain(self, vector, delta):
        if vec.in_bounds(vector, self.extents()):
            return vector

        x, y = vector
        dx, dy = delta
        x -= dx
        y -= dy
        while vec.in_bounds((x, y), self.extents()):
            x -= dx
            y -= dy
        return x, y

    def extents(self):
        if not self.storage:
            return (0, 0), (0, 0)
        minx, miny = self.storage.keys()[0]
        maxx, maxy = self.storage.keys()[0]
        for x, y in self.storage.iterkeys():
            minx = x if minx is None else min(minx, x)
            maxx = x if maxx is None else max(maxx, x)
            miny = y if miny is None else min(miny, y)
            maxy = y if maxy is None else max(maxy, y)
        extents = ((minx, miny), (maxx, maxy))
        return extents

    def get(self, coord):
        return self.storage.get(coord, " ")

    def set(self, coord, value):
        assert len(coord) == 2
        self.storage[coord] = value
