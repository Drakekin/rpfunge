Rpfunge - A Befunge98 Implementation in Rpython
-----------------------------------------------

Rpfunge is an implementation of the Befunge98 esoteric programming language
as described in this [spec page][befunge98-spec] in Rpython, a restricted
subset of the Python programming language that compiles down to a single
executable, designed for the implementation of JIT-enabled virtual machines.

To compile the interpreter, first clone pypy:

    hg clone http://bitbucket.org/pypy/pypy

Then ensure you have the required dependencies, on debian based systems run:

    sudo apt-get install gcc make python-dev libffi-dev libsqlite3-dev \
    pkg-config libz-dev libbz2-dev libncurses-dev libexpat1-dev libssl-dev \
    libgc-dev python-sphinx python-greenlet

Finally, cd into the directory where you downloaded the rpfunge source to and
run the following command:

    python [path to pypy]/rpython/bin/rpython rpfunge.py

This will produce a binary called `rpfunge-c` which can then run befunge98 programs

TODO
====

* Implement stack-of-stack functions
* Implement file output
* Implement JIT hinting

[befunge98-spec]: http://quadium.net/funge/spec98.html "Funge 98 Final Specification"
