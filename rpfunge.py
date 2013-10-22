import sys
from befunge98 import mainloop, parse
import os
from funge import read_file


def run(filename):
    program_contents = read_file(filename)
    program = parse(program_contents)
    mainloop(program)


def entry_point(argv):
    try:
        filename = argv[1]
    except IndexError:
        print "You must supply a filename"
        return 1

    run(filename)
    return 0


def target(*args):
    return entry_point, None


if __name__ == "__main__":
    entry_point(sys.argv)
