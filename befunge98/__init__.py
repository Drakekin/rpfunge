from pointer import Pointer
from befunge98.instructions import INSTRUCTIONS as befunge
from grid import TwoDimensionalLaheySpace as Grid


def mainloop(grid):
    while len(grid.pointers):
        grid.tick()


def parse(input_program):
    grid = Grid()
    # newline_characters = ["\r", "\n", "\r\n"]
    # for newline_character in newline_characters:
    #     input_program = input_program.replace(newline_character, "\n")
    for y, line in enumerate(input_program.split("\n")):
        for x, char in enumerate(line):
            if char == " ":
                continue
            grid.__setitem__((x, y), char)
    grid.pointers.append(Pointer(befunge, grid))
    return grid


def run(input_file):
    program = parse(input_file.read())
    mainloop(program)
