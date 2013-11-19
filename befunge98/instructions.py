from funge import is_hex, random_integer, load_string, read_file
import os
from time import time
import vec


def stack_pop(stack):
    try:
        return stack.pop()
    except IndexError:
        return 0


def move(position, velocity):
    return vec.add(position, velocity)


def DEFAULT_INSTRUCTION(position, velocity, storage_offset, stack, stack_of_stacks, push_mode, program):
    char = program.get(position)
    if is_hex(char):
        stack.append(int(char, 16))
        return position, velocity, storage_offset, stack, stack_of_stacks, push_mode, program, True
    return position, velocity, storage_offset, stack, stack_of_stacks, push_mode, program, True


INSTRUCTIONS = {}


def register_instruction(instruction):
    def register(function):
        INSTRUCTIONS[instruction] = function
        return function

    return register


@register_instruction("+")
def plus(position, velocity, storage_offset, stack, stack_of_stacks, push_mode, program):
    a = stack_pop(stack)
    b = stack_pop(stack)
    stack.append(a + b)
    return position, velocity, storage_offset, stack, stack_of_stacks, push_mode, program, True


@register_instruction("-")
def minus(position, velocity, storage_offset, stack, stack_of_stacks, push_mode, program):
    a = stack_pop(stack)
    b = stack_pop(stack)
    stack.append(b - a)
    return position, velocity, storage_offset, stack, stack_of_stacks, push_mode, program, True


@register_instruction("*")
def multiply(position, velocity, storage_offset, stack, stack_of_stacks, push_mode, program):
    a = stack_pop(stack)
    b = stack_pop(stack)
    stack.append(a * b)
    return position, velocity, storage_offset, stack, stack_of_stacks, push_mode, program, True


@register_instruction("/")
def divide(position, velocity, storage_offset, stack, stack_of_stacks, push_mode, program):
    a = stack_pop(stack)
    b = stack_pop(stack)
    stack.append(b // a)
    return position, velocity, storage_offset, stack, stack_of_stacks, push_mode, program, True


@register_instruction("%")
def mod(position, velocity, storage_offset, stack, stack_of_stacks, push_mode, program):
    a = stack_pop(stack)
    b = stack_pop(stack)
    stack.append(b % a)
    return position, velocity, storage_offset, stack, stack_of_stacks, push_mode, program, True


@register_instruction(";")
def skip(position, velocity, storage_offset, stack, stack_of_stacks, push_mode, program):
    position = move(position, velocity)
    value = program.get(position)
    while not value == ";":
        position = move(position, velocity)
        value = program.get(position)
    return position, velocity, storage_offset, stack, stack_of_stacks, push_mode, program, True


@register_instruction("!")
def _not(position, velocity, storage_offset, stack, stack_of_stacks, push_mode, program):
    value = stack_pop(stack)
    stack.append(1 if value == 0 else 0)
    return position, velocity, storage_offset, stack, stack_of_stacks, push_mode, program, True


@register_instruction("`")
def greater_than(position, velocity, storage_offset, stack, stack_of_stacks, push_mode, program):
    a = stack_pop(stack)
    b = stack_pop(stack)
    stack.append(1 if b > a else 0)
    return position, velocity, storage_offset, stack, stack_of_stacks, push_mode, program, True


@register_instruction("^")
def up(position, velocity, storage_offset, stack, stack_of_stacks, push_mode, program):
    velocity = (0, -1)
    return position, velocity, storage_offset, stack, stack_of_stacks, push_mode, program, True


@register_instruction("v")
def down(position, velocity, storage_offset, stack, stack_of_stacks, push_mode, program):
    velocity = (0, 1)
    return position, velocity, storage_offset, stack, stack_of_stacks, push_mode, program, True


@register_instruction("[")
def turn_left(position, velocity, storage_offset, stack, stack_of_stacks, push_mode, program):
    x, y = velocity
    velocity = y, -x
    return position, velocity, storage_offset, stack, stack_of_stacks, push_mode, program, True


@register_instruction("]")
def turn_right(position, velocity, storage_offset, stack, stack_of_stacks, push_mode, program):
    x, y = velocity
    velocity = -y, x
    return position, velocity, storage_offset, stack, stack_of_stacks, push_mode, program, True


@register_instruction("<")
def left(position, velocity, storage_offset, stack, stack_of_stacks, push_mode, program):
    velocity = (-1, 0)
    return position, velocity, storage_offset, stack, stack_of_stacks, push_mode, program, True


@register_instruction(">")
def right(position, velocity, storage_offset, stack, stack_of_stacks, push_mode, program):
    velocity = (1, 0)
    return position, velocity, storage_offset, stack, stack_of_stacks, push_mode, program, True


@register_instruction("?")
def random_direction(position, velocity, storage_offset, stack, stack_of_stacks, push_mode, program):
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    velocity = directions[random_integer(0, 3)]
    return position, velocity, storage_offset, stack, stack_of_stacks, push_mode, program, True


@register_instruction("_")
def left_right_if(position, velocity, storage_offset, stack, stack_of_stacks, push_mode, program):
    velocity = (1, 0) if stack_pop(stack) == 0 else (-1, 0)
    return position, velocity, storage_offset, stack, stack_of_stacks, push_mode, program, True


@register_instruction("|")
def up_down_if(position, velocity, storage_offset, stack, stack_of_stacks, push_mode, program):
    velocity = (0, 1) if stack_pop(stack) == 0 else (0, -1)
    return position, velocity, storage_offset, stack, stack_of_stacks, push_mode, program, True


@register_instruction('"')
def toggle_push_mode(position, velocity, storage_offset, stack, stack_of_stacks, push_mode, program):
    push_mode = True
    return position, velocity, storage_offset, stack, stack_of_stacks, push_mode, program, True


@register_instruction(':')
def duplicate_stack(position, velocity, storage_offset, stack, stack_of_stacks, push_mode, program):
    a = stack_pop(stack)
    stack.append(a)
    stack.append(a)
    return position, velocity, storage_offset, stack, stack_of_stacks, push_mode, program, True


@register_instruction("\\")
def swap_stack(position, velocity, storage_offset, stack, stack_of_stacks, push_mode, program):
    a = stack_pop(stack)
    b = stack_pop(stack)
    stack.append(b)
    stack.append(a)
    return position, velocity, storage_offset, stack, stack_of_stacks, push_mode, program, True


@register_instruction("$")
def pop_stack(position, velocity, storage_offset, stack, stack_of_stacks, push_mode, program):
    stack_pop(stack)
    return position, velocity, storage_offset, stack, stack_of_stacks, push_mode, program, True


@register_instruction(".")
def output_integer(position, velocity, storage_offset, stack, stack_of_stacks, push_mode, program):
    os.write(1, str(stack_pop(stack)))
    return position, velocity, storage_offset, stack, stack_of_stacks, push_mode, program, True


@register_instruction(",")
def output_ascii(position, velocity, storage_offset, stack, stack_of_stacks, push_mode, program):
    os.write(1, chr(stack_pop(stack)))
    return position, velocity, storage_offset, stack, stack_of_stacks, push_mode, program, True


@register_instruction("#")
def trampoline(position, velocity, storage_offset, stack, stack_of_stacks, push_mode, program):
    position = move(position, velocity)
    return position, velocity, storage_offset, stack, stack_of_stacks, push_mode, program, True


@register_instruction("p")
def put(position, velocity, storage_offset, stack, stack_of_stacks, push_mode, program):
    y = stack_pop(stack)
    x = stack_pop(stack)
    v = stack_pop(stack)
    location = vec.add((x, y), storage_offset)
    program.set(location, chr(v))
    return position, velocity, storage_offset, stack, stack_of_stacks, push_mode, program, True


@register_instruction("g")
def get(position, velocity, storage_offset, stack, stack_of_stacks, push_mode, program):
    y = stack_pop(stack)
    x = stack_pop(stack)
    location = vec.add((x, y), storage_offset)
    stack.append(ord(program.get(location)))
    return position, velocity, storage_offset, stack, stack_of_stacks, push_mode, program, True


@register_instruction("&")
def push_number(position, velocity, storage_offset, stack, stack_of_stacks, push_mode, program):
    num = os.read(0, 1)[0]
    if is_hex(num):
        stack.append(int(num, 16))
    return position, velocity, storage_offset, stack, stack_of_stacks, push_mode, program, True


@register_instruction("~")
def push_ascii(position, velocity, storage_offset, stack, stack_of_stacks, push_mode, program):
    stack.append(ord(os.read(0, 1)[0]))
    return position, velocity, storage_offset, stack, stack_of_stacks, push_mode, program, True


@register_instruction("i")
def load_file(position, velocity, storage_offset, stack, stack_of_stacks, push_mode, program):
    filename = ""
    char = stack_pop(stack)
    while char:
        filename += chr(char)
        char = stack_pop(stack)
    sx, sy = storage_offset
    flags = stack_pop(stack)
    y = stack_pop(stack) + sy
    x = stack_pop(stack) + sx
    #y2 = stack_pop(stack) + sy
    #x2 = stack_pop(stack) + sx
    file_content = read_file(filename)
    if flags % 2:
        # If the LSB of flags is high (i.e. flags is odd) treat file as a single line
        file_content = file_content.replace("\n", "a")
    (xa, ya), (xb, yb) = load_string(program, file_content, (x, y))
    stack += [xb, yb, xa, ya]
    return position, velocity, storage_offset, stack, stack_of_stacks, push_mode, program, True


@register_instruction("j")
def jump(position, velocity, storage_offset, stack, stack_of_stacks, push_mode, program):
    n = stack_pop(stack)
    for _ in xrange(n):
        position = move(position, velocity)
    return position, velocity, storage_offset, stack, stack_of_stacks, push_mode, program, True


@register_instruction("k")
def repeat(position, velocity, storage_offset, stack, stack_of_stacks, push_mode, program):
    instruction = program.get(vec.add(position, velocity))
    if instruction in INSTRUCTIONS:
        operation = INSTRUCTIONS[instruction]
    else:
        operation = DEFAULT_INSTRUCTION
    result = position, velocity, storage_offset, stack, stack_of_stacks, push_mode, program, True
    for _ in xrange(stack_pop(stack)):
        result = operation(position, velocity, storage_offset, stack, stack_of_stacks, push_mode, program)
    return result


@register_instruction("n")
def clear_stack(position, velocity, storage_offset, stack, stack_of_stacks, push_mode, program):
    stack = []
    return position, velocity, storage_offset, stack, stack_of_stacks, push_mode, program, True


@register_instruction("o")
def output_file(position, velocity, storage_offset, stack, stack_of_stacks, push_mode, program):
    raise NotImplementedError("File output not implemented")  # TODO: Implement file saving


@register_instruction("y")
def system_info(position, velocity, storage_offset, stack, stack_of_stacks, push_mode, program):
    t = int(time())
    clock = t % 24 * 60 * 60
    day = t - clock
    x, y = position
    dx, dy = velocity
    sx, sy = storage_offset
    (lx, ly), (hx, hy) = program.extents()
    info_stack = [
                     0b11000, # Unbuffered IO, = implemented, no i or o commands and no concurrency
                     8, # Bytes per cell
                     0, # Handprint
                     1, # Version number
                     1, # = behaves like the C function system()
                     ord("/"), # Path sep
                     2, # Number of dimensions
                     0, # Pointer ID
                     0, # Unused
                     y,
                     x,
                     dy,
                     dx,
                     sy,
                     sx,
                     ly,
                     lx,
                     hy,
                     hx,
                     day,
                     clock,
                     len(stack_of_stacks) + 1,
                     len(stack)
                 ] + [len(s) for s in stack_of_stacks]

    i = stack_pop(stack)
    if 0 < i <= len(info_stack):
        stack.append(info_stack[i - 1])
    else:
        while info_stack:
            stack.append(info_stack.pop())

    return position, velocity, storage_offset, stack, stack_of_stacks, push_mode, program, True


@register_instruction("q")
def end_program(position, velocity, storage_offset, stack, stack_of_stacks, push_mode, program):
    os._exit(stack_pop(stack))
    return position, velocity, storage_offset, stack, stack_of_stacks, push_mode, program, False  # Just in case.


@register_instruction("'")
def fetch_char(position, velocity, storage_offset, stack, stack_of_stacks, push_mode, program):
    char = program.get(vec.add(position, velocity))
    stack.append(ord(char))
    position = move(position, velocity)
    return position, velocity, storage_offset, stack, stack_of_stacks, push_mode, program, True


@register_instruction("s")
def store_char(position, velocity, storage_offset, stack, stack_of_stacks, push_mode, program):
    program.set(vec.add(position, velocity), chr(stack_pop(stack)))
    position = move(position, velocity)
    return position, velocity, storage_offset, stack, stack_of_stacks, push_mode, program, True


# Multifunge is not compatible with JIT
@register_instruction("t")
def split(position, velocity, storage_offset, stack, stack_of_stacks, push_mode, program):
    return reflect(position, velocity, storage_offset, stack, stack_of_stacks, push_mode, program)


@register_instruction("z")
def no_op(position, velocity, storage_offset, stack, stack_of_stacks, push_mode, program):
    return position, velocity, storage_offset, stack, stack_of_stacks, push_mode, program, True


# TODO: Figure out why these functions do not work.
@register_instruction("{")
def start_block(position, velocity, storage_offset, stack, stack_of_stacks, push_mode, program):
    n = stack_pop(stack)
    soss = stack
    if n < 0:
        toss = [0] * (n * -1)
    elif n > len(soss):
        i = n - len(soss)
        toss = [0] * i + soss
        soss = []
    else:
        s = len(soss) - n
        assert s >= 0
        toss = soss[s:]
        soss = soss[:s]
    sx, sy = storage_offset
    soss += [sx, sy]
    storage_offset = vec.add(position, velocity)
    stack_of_stacks.append(soss)
    stack = toss
    return position, velocity, storage_offset, stack, stack_of_stacks, push_mode, program, True


@register_instruction("}")
def end_block(position, velocity, storage_offset, stack, stack_of_stacks, push_mode, program):
    if not stack_of_stacks:
        return reflect(position, velocity, storage_offset, stack, stack_of_stacks, push_mode, program)

    toss = stack
    soss = stack_of_stacks.pop()
    n = stack_pop(stack)
    try:
        sy = soss.pop()
    except IndexError:
        sy = 0
    try:
        sx = soss.pop()
    except IndexError:
        sx = 0

    if n < 0:
        for _ in range(abs(n)):
            try:
                soss.pop()
            except IndexError:
                pass
    elif n > len(toss):
        i = n - len(soss)
        soss += [0] * i + toss
    else:
        s = len(toss) - n
        assert s >= 0
        soss += toss[s:]

    stack = soss
    stack_of_stacks.pop()
    storage_offset = (sx, sy)

    return position, velocity, storage_offset, stack, stack_of_stacks, push_mode, program, True


@register_instruction("u")
def transfer(position, velocity, storage_offset, stack, stack_of_stacks, push_mode, program):
    if not stack_of_stacks:
        return reflect(position, velocity, storage_offset, stack, stack_of_stacks, push_mode, program)

    n = stack_pop(stack)
    soss = stack_of_stacks[-1]
    if n > 0:
        dest, source = stack, soss
    elif n == 0:
        return position, velocity, storage_offset, stack, stack_of_stacks, push_mode, program, True
    else:
        dest, source = soss, stack

    for _ in range(abs(n)):
        dest.append(source.pop())
    return position, velocity, storage_offset, stack, stack_of_stacks, push_mode, program, True


@register_instruction("@")
def die(position, velocity, storage_offset, stack, stack_of_stacks, push_mode, program):
    return position, velocity, storage_offset, stack, stack_of_stacks, push_mode, program, False


@register_instruction("r")
def reflect(position, velocity, storage_offset, stack, stack_of_stacks, push_mode, program):
    velocity = vec.invert(velocity)
    return position, velocity, storage_offset, stack, stack_of_stacks, push_mode, program, True


@register_instruction("=")
def system_call(position, velocity, storage_offset, stack, stack_of_stacks, push_mode, program):
    string = ""
    value = stack_pop(stack)
    while value:
        string += chr(value)
        value = stack_pop(stack)
    process = os.system(string)
    stack.append(process)
    return position, velocity, storage_offset, stack, stack_of_stacks, push_mode, program, True


@register_instruction(" ")
def space(position, velocity, storage_offset, stack, stack_of_stacks, push_mode, program):
    return position, velocity, storage_offset, stack, stack_of_stacks, push_mode, program, True
