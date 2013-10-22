from pointer import Pointer
from befunge98.instructions import INSTRUCTIONS as befunge
from grid import TwoDimensionalLaheySpace as Grid


def mainloop(grid):
    while len(grid.pointers):
        grid.tick()


def parse(input_program):
    grid = Grid()
    for y, line in enumerate(input_program.split("\n")):
        for x, char in enumerate(line):
            if char == " ":
                continue
            grid.set((x, y), char)
    Pointer(befunge, grid)
    return grid


def run(input_file):
    program = parse(input_file.read())
    mainloop(program)
