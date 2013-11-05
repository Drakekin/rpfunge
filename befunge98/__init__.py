from funge import load_string
from pointer import Pointer
from befunge98.instructions import INSTRUCTIONS as befunge
from grid import TwoDimensionalLaheySpace as Grid


def mainloop(grid):
    while grid.pointer:
        grid.tick()


def parse(input_program):
    grid = Grid()
    load_string(grid, input_program, (0, 0))
    Pointer(befunge, grid)
    return grid


def run(input_file):
    program = parse(input_file.read())
    mainloop(program)
