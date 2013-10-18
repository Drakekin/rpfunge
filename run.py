from befunge98 import run
from sys import argv

if __name__ == "__main__":
    if argv[1] == "debug":
        from cStringIO import StringIO
        program = (
            """>0"!dlroW ,olleH":v\n"""
            """               v:,_@   \n"""
            """               >  ^    \n"""
            """                       \n"""
        )
        run(StringIO(program))
    else:
        run(open(argv[1], 'r'))
