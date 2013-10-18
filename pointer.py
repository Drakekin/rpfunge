import vec
from funge import DEFAULT_INSTRUCTION


class Pointer(object):
    def __init__(self, language, program, location=(0, 0), delta=(1, 0)):
        self.position = location
        self.storage_offset = (0, 0)
        self.velocity = delta
        self.stack_of_stacks = []
        self.stack = []
        self.instructions = language
        self.program = program
        self.push_mode = False

    def stack_pop(self):
        try:
            return self.stack.pop()
        except IndexError:
            return 0

    def tick(self):
        self.position = self.lahey_constrain(self.program)
        self.move()
        instruction = self.program.__getitem__(self.position)
        if self.push_mode:
            if instruction == '"':
                self.push_mode = False
                return False, True
            else:
                self.stack.append(ord(instruction))
                return False, True
        else:
            if instruction in self.instructions:
                operation = self.instructions[instruction]
                cont, alive = operation(self)
                return cont, alive
            else:
                return DEFAULT_INSTRUCTION(self)

    def lahey_constrain(self, grid):
        if vec.in_bounds(self.position, grid.extents()):
            return self.position

        position = self.position
        position = vec.subtract(position, self.velocity)
        while vec.in_bounds(position, grid.extents()):
            position = vec.subtract(position, self.velocity)
        return position

    def move(self):
        self.position = vec.add(self.position, self.velocity)

