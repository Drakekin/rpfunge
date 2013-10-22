import os
from time import time
from funge import DEFAULT_INSTRUCTION, is_hex, random_integer, load_string, read_file
from pointer import Pointer
import vec

INSTRUCTIONS = {}


def register_instruction(instruction):
    def register(function):
        INSTRUCTIONS[instruction] = function
        return function
    return register


@register_instruction("+")
def plus(pointer):
    a = pointer.stack_pop()
    b = pointer.stack_pop()
    pointer.stack.append(a + b)
    return False, True


@register_instruction("-")
def minus(pointer):
    a = pointer.stack_pop()
    b = pointer.stack_pop()
    pointer.stack.append(a - b)
    return False, True


@register_instruction("*")
def multiply(pointer):
    a = pointer.stack_pop()
    b = pointer.stack_pop()
    pointer.stack.append(a * b)
    return False, True


@register_instruction("/")
def divide(pointer):
    a = pointer.stack_pop()
    b = pointer.stack_pop()
    pointer.stack.append(b // a)
    return False, True


@register_instruction("%")
def mod(pointer):
    a = pointer.stack_pop()
    b = pointer.stack_pop()
    pointer.stack.append(b % a)
    return False, True


@register_instruction(";")
def skip(pointer):
    pointer.move()
    value = pointer.program.get(pointer.position)
    while not value == ";":
        pointer.move()
        value = pointer.program.get(pointer.position)
    return False, True


@register_instruction("!")
def _not(pointer):
    value = pointer.stack_pop()
    pointer.stack.append(1 if value == 0 else 0)
    return False, True


@register_instruction("`")
def greater_than(pointer):
    a = pointer.stack_pop()
    b = pointer.stack_pop()
    pointer.stack.append(1 if b > a else 0)
    return False, True


@register_instruction("^")
def up(pointer):
    pointer.velocity = (0, -1)
    return False, True


@register_instruction("v")
def down(pointer):
    pointer.velocity = (0, 1)
    return False, True


@register_instruction("[")
def turn_left(pointer):
    x, y = pointer.velocity
    pointer.velocity = y, -x
    return False, True


@register_instruction("]")
def turn_right(pointer):
    x, y = pointer.velocity
    pointer.velocity = -y, x
    return False, True


@register_instruction("<")
def left(pointer):
    pointer.velocity = (-1, 0)
    return False, True


@register_instruction(">")
def right(pointer):
    pointer.velocity = (1, 0)
    return False, True


@register_instruction("?")
def random_direction(pointer):
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    pointer.velocity = directions[random_integer(0, 3)]
    return False, True


@register_instruction("_")
def left_right_if(pointer):
    pointer.velocity = (1, 0) if pointer.stack_pop() == 0 else (-1, 0)
    return False, True


@register_instruction("|")
def up_down_if(pointer):
    pointer.velocity = (0, 1) if pointer.stack_pop() == 0 else (0, -1)
    return False, True


@register_instruction('"')
def toggle_push_mode(pointer):
    pointer.push_mode = True
    return False, True


@register_instruction(':')
def duplicate_stack(pointer):
    a = pointer.stack_pop()
    pointer.stack.append(a)
    pointer.stack.append(a)
    return False, True


@register_instruction("\\")
def swap_stack(pointer):
    a = pointer.stack_pop()
    b = pointer.stack_pop()
    pointer.stack.append(b)
    pointer.stack.append(a)
    return False, True


@register_instruction("$")
def pop_stack(pointer):
    pointer.stack_pop()
    return False, True


@register_instruction(".")
def output_integer(pointer):
    os.write(1, str(pointer.stack_pop()))
    return False, True


@register_instruction(",")
def output_ascii(pointer):
    os.write(1, chr(pointer.stack_pop()))
    return False, True


@register_instruction("#")
def trampoline(pointer):
    pointer.move()
    return False, True


@register_instruction("p")
def put(pointer):
    y = pointer.stack_pop()
    x = pointer.stack_pop()
    v = pointer.stack_pop()
    location = vec.add((x, y), pointer.storage_offset)
    pointer.program.set(location, chr(v))
    return False, True


@register_instruction("g")
def get(pointer):
    y = pointer.stack_pop()
    x = pointer.stack_pop()
    location = vec.add((x, y), pointer.storage_offset)
    pointer.stack.append(ord(pointer.program.get(location)))
    return False, True


@register_instruction("&")
def push_number(pointer):
    num = os.read(0, 1)[0]
    if is_hex(num):
        pointer.stack.append(int(num, 16))
    return False, True


@register_instruction("~")
def push_ascii(pointer):
    pointer.stack.append(ord(os.read(0, 1)[0]))
    return False, True


@register_instruction("i")
def load_file(pointer):
    filename = ""
    char = pointer.stack_pop()
    while char:
        filename += chr(char)
        char = pointer.stack_pop()
    sx, sy = pointer.storage_offset
    flags = pointer.stack_pop()
    y = pointer.stack_pop() + sy
    x = pointer.stack_pop() + sx
    #y2 = pointer.stack_pop() + sy
    #x2 = pointer.stack_pop() + sx
    (xa, ya), (xb, yb) = load_string(pointer.program, read_file(filename), (x, y))
    pointer.stack += [xb, yb, xa, ya]
    return False, True


@register_instruction("j")
def jump(pointer):
    n = pointer.stack_pop()
    for _ in xrange(n):
        pointer.move()
    return False, True


@register_instruction("k")
def repeat(pointer):
    instruction = pointer.program.get(vec.add(pointer.position, pointer.velocity))
    if instruction in INSTRUCTIONS:
        operation = INSTRUCTIONS[instruction]
    else:
        operation = DEFAULT_INSTRUCTION
    result = False, True
    for _ in xrange(pointer.stack_pop()):
        result = operation(pointer)
    return result


@register_instruction("n")
def clear_stack(pointer):
    pointer.stack = []
    return False, True


@register_instruction("o")
def output_file(pointer):
    raise NotImplementedError("File output not implemented")  # TODO: Implement file saving


@register_instruction("y")
def system_info(pointer):
    t = int(time())
    clock = t % 24*60*60
    day = t - clock
    x, y = pointer.position
    dx, dy = pointer.velocity
    sx, sy = pointer.storage_offset
    (lx, ly), (hx, hy) = pointer.program.extents()
    info_stack = [
        0b11000,  # Unbuffered IO, = implemented, no i or o commands and no concurrency
        8,  # Bytes per cell
        0,  # Handprint
        1,  # Version number
        1,  # = behaves like the C function system()
        ord("/"),  # Path sep
        2,  # Number of dimensions
        0,  # Pointer ID
        0,  # Unused
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
        len(pointer.stack_of_stacks) + 1,
        len(pointer.stack)
    ] + [len(s) for s in pointer.stack_of_stacks]

    i = pointer.stack_pop()
    if 0 < i <= len(info_stack):
        pointer.stack.append(info_stack[i-1])
    else:
        while info_stack:
            pointer.stack.append(info_stack.pop())

    return False, True


@register_instruction("q")
def end_program(pointer):
    os._exit(pointer.stack_pop())
    return False, False  # Just in case.


@register_instruction("'")
def fetch_char(pointer):
    char = pointer.program.get(vec.add(pointer.position, pointer.velocity))
    pointer.stack.append(ord(char))
    pointer.move()
    return False, True


@register_instruction("s")
def store_char(pointer):
    pointer.program.set(vec.add(pointer.position, pointer.velocity), chr(pointer.stack_pop()))
    pointer.move()
    return False, True


@register_instruction("t")
def split(pointer):
    new_pointer = Pointer(pointer.instructions, pointer.program, pointer.position, vec.invert(pointer.velocity))
    new_pointer.move()
    return False, True


@register_instruction("z")
def no_op(pointer):
    return True, True


# TODO: Figure out why these functions do not work.
#
# @register_instruction("{")
# def start_block(pointer):
#     n = pointer.stack_pop()
#     soss = []
#     if n > 0:
#         z = 0
#         if n > len(pointer.stack):
#             z = len(pointer.stack) - n
#             n = len(pointer.stack)
#         soss += ([0] * z) + pointer.stack[-n:]
#         pointer.stack = pointer.stack[:-n]
#     else:
#         soss += abs(n) * [0]
#
#     x, y = pointer.storage_offset
#     soss += [x, y]
#     pointer.stack_of_stacks.append(soss)
#     pointer.storage_offset = vec.add(pointer.position, pointer.velocity)
#     return False, True
#
#
# @register_instruction("}")
# def end_block(pointer):
#     if not pointer.stack_of_stacks:
#         return
#
#     n = pointer.stack_pop()
#     soss = pointer.stack_of_stacks.pop()
#     pointer.storage_offset = soss[-2:]
#     soss = soss[:-2]
#     if n > 0:
#         z = 0
#         if n > len(soss):
#             z = len(soss) - n
#             n = len(soss)
#         pointer.stack += ([0] * z) + soss[-n:]
#         soss = soss[:-n]
#     else:
#         soss = soss[:n]
#
#     x, y = pointer.storage_offset
#     soss += [x, y]
#     pointer.stack_of_stacks.append(soss)
#     pointer.storage_offset = vec.add(pointer.position, pointer.velocity)
#     return False, True
#
#
# @register_instruction("u")
# def transfer(pointer):
#     if not pointer.stack_of_stacks:
#         return
#
#     n = pointer.stack_pop()
#     soss = pointer.stack_of_stacks[-1]
#     if n > 0:
#         dest, source = pointer.stack, soss
#     elif n == 0:
#         return
#     else:
#         dest, source = soss, pointer.stack
#
#     for _ in range(abs(n)):
#         dest.append(source.pop())
#     return False, True


@register_instruction("@")
def die(pointer):
    return False, False


@register_instruction("r")
def reflect(pointer):
    pointer.velocity = vec.invert(pointer.velocity)
    return False, True


@register_instruction("=")
def system_call(pointer):
    string = ""
    value = pointer.stack_pop()
    while value:
        string += chr(value)
        value = pointer.stack_pop()
    process = os.system(string)
    pointer.stack.append(process)
    return False, True


@register_instruction(" ")
def space(pointer):
    return True, True
