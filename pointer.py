import vec
from funge import DEFAULT_INSTRUCTION
# So that you can still run this module under standard CPython, I add this
# import guard that creates a dummy class instead.
try:
    from rpython.rlib.jit import JitDriver
except ImportError:
    class JitDriver(object):
        def __init__(self, **kw):
            pass

        def jit_merge_point(self, **kw):
            pass

        def can_enter_jit(self, **kw):
            pass


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
        # self.jitdriver = JitDriver(
        #     greens=[
        #         "velocity", "location", "storage_offset"
        #     ], reds=[
        #         "stack", "stack_of_stacks"
        #     ]
        # )
        self.program.pointer = self

    def stack_pop(self):
        try:
            return self.stack.pop()
        except IndexError:
            return 0

    def tick(self):
        self.position = self.lahey_constrain(self.program)
        instruction = self.program.get(self.position)
        cont, alive = False, True
        # self.jitdriver.jit_merge_point(
        #     velocity=self.velocity,
        #     location=self.position,
        #     storage_offset=self.storage_offset,
        #     stack=self.stack,
        #     stack_of_stacks=self.stack_of_stacks
        # )
        if self.push_mode:
            if instruction == '"':
                self.push_mode = False
            else:
                self.stack.append(ord(instruction))
        else:
            if instruction in self.instructions:
                operation = self.instructions[instruction]
                cont, alive = operation(self)
            else:
                cont, alive = DEFAULT_INSTRUCTION(self)
        self.move()
        return cont, alive

    def lahey_constrain(self, grid):
        # TODO: Fix the bug whereby if the pointer is outside the program space but pointing towards it, the pointer
        #       is locked in place
        if vec.in_bounds(self.position, grid.extents()):
            return self.position

        position = self.position
        position = vec.subtract(position, self.velocity)
        while vec.in_bounds(position, grid.extents()):
            position = vec.subtract(position, self.velocity)
        return position

    def move(self):
        self.position = vec.add(self.position, self.velocity)

