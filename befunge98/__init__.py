from funge import load_string
from grid import TwoDimensionalLaheySpace as Grid
from befunge98.instructions import INSTRUCTIONS, move, stack_pop, DEFAULT_INSTRUCTION
import vec


def lahey_constrain(position, velocity, program):
    # TODO: Fix the bug whereby if the pointer is outside the program space but pointing towards it, the pointer
    #       is locked in place
    if vec.in_bounds(position, program.extents()):
        return position

    corrected_position = position
    corrected_position = vec.subtract(corrected_position, velocity)
    while vec.in_bounds(corrected_position, program.extents()):
        corrected_position = vec.subtract(corrected_position, velocity)
    return corrected_position


def mainloop(program):
    position = (0, 0)
    velocity = (1, 0)
    storage_offset = (0, 0)
    stack = []
    stack_of_stacks = []
    push_mode = False

    while True:
        position = lahey_constrain(position, velocity, program)
        instruction = program.get(position)
        alive = True
        # self.jitdriver.jit_merge_point(
        #     velocity=self.velocity,
        #     location=self.position,
        #     storage_offset=self.storage_offset,
        #     stack=self.stack,
        #     stack_of_stacks=self.stack_of_stacks
        # )
        if push_mode:
            if instruction == '"':
                push_mode = False
            else:
                stack.append(ord(instruction))
        else:
            if instruction in INSTRUCTIONS:
                operation = INSTRUCTIONS[instruction]
                position, velocity, storage_offset, stack, stack_of_stacks, push_mode, program, alive = \
                    operation(position, velocity, storage_offset, stack, stack_of_stacks, push_mode, program)
            else:
                position, velocity, storage_offset, stack, stack_of_stacks, push_mode, program, alive = \
                    DEFAULT_INSTRUCTION(position, velocity, storage_offset, stack, stack_of_stacks, push_mode, program)
        position = move(position, velocity)
        if not alive:
            break


def run(input_file):
    program = Grid()
    load_string(program, input_file, (0, 0))
    mainloop(program)
