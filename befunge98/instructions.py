from math import floor
from random import choice
from subprocess import call
import sys
from funge import DEFAULT_INSTRUCTION
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
    pointer.stack.append(a + b)
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
    pointer.stack.append(floor(b / a))
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
    value = pointer.program[pointer.position]
    while not value == ";":
        pointer.move()
        value = pointer.program[pointer.position]
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
    directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    pointer.velocity = directions[directions.index(pointer.velocity)-1]
    return False, True


@register_instruction("]")
def turn_right(pointer):
    directions = [(1, 0), (0, -1), (-1, 0), (0, 1)]
    pointer.velocity = directions[directions.index(pointer.velocity)-1]
    return False, True


@register_instruction("<")
def left(pointer):
    pointer.velocity = (-1, 0)
    return False, True


@register_instruction(">")
def right(pointer):
    pointer.velocity = (1, 0)
    return False, True


# @register_instruction("?")
# def random_direction(pointer):
#     # directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
#     # pointer.velocity = choice(directions)
#     # return False, True
#     raise NotImplementedError("RPython cannot use the random library")


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
    # Rpython doesn't know how to represent sys
    # sys.stdout.write(str(pointer.stack_pop()))
    print pointer.stack_pop()
    return False, True


@register_instruction(",")
def output_ascii(pointer):
    # Rpython doesn't know how to represent sys
    # sys.stdout.write(unichr(pointer.stack_pop()))
    print unichr(pointer.stack_pop())
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
    pointer.program[location] = unichr(v)
    return False, True


@register_instruction("g")
def get(pointer):
    y = pointer.stack_pop()
    x = pointer.stack_pop()
    location = vec.add((x, y), pointer.storage_offset)
    pointer.stack.append(ord(pointer.program[location]))
    return False, True


# @register_instruction("&")
# def push_number(pointer):
#     # user_input = raw_input("> ")
#     # if user_input.isdigit():
#     #     pointer.stack.append(ord(user_input))
#     # return False, True
#     raise NotImplementedError("RPython doesn't support raw_input")


# @register_instruction("~")
# def push_ascii(pointer):
#     # user_input = raw_input("> ")
#     # if len(user_input) > 1:
#     #     user_input = user_input[-1]
#     # elif len(user_input) == 0:
#     #     user_input = " "
#     # pointer.stack.append(ord(user_input))
#     # return False, True
#     raise NotImplementedError("RPython doesn't support raw_input")


# @register_instruction("i")
# def load_file(pointer):
#     raise NotImplementedError("File Loading Not Implemented")


@register_instruction("j")
def jump(pointer):
    n = pointer.stack_pop()
    for _ in xrange(n):
        pointer.move()
    return False, True


@register_instruction("k")
def jump(pointer):
    instruction = pointer.program[vec.add(pointer.position, pointer.velocity)]
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


# @register_instruction("o")
# def output_file(pointer):
#     raise NotImplementedError("File output not implemented")


# @register_instruction("y")
# def system_info(pointer):
#     raise NotImplementedError("System information not implemented")


@register_instruction("q")
def end_program(pointer):
    # RPython threw a fit
    # sys.exit(pointer.stack_pop())
    return die(pointer)  # Kill the pointer instead


@register_instruction("'")
def fetch_char(pointer):
    char = pointer.program[vec.add(pointer.position, pointer.velocity)]
    pointer.stack.append(ord(char))
    pointer.move()
    return False, True


@register_instruction("s")
def store_char(pointer):
    pointer.program[vec.add(pointer.position, pointer.velocity)] = unichr(pointer.stack_pop())
    pointer.move()
    return False, True


# @register_instruction("t")
# def split(pointer):
#     raise NotImplementedError("Single threaded only")
#     # pos = pointer.position
#     # vx, vy = pointer.velocity
#     # vel = (vx * -1, vy * -1)
#     # new_pointer = Pointer(2, pointer.program, pointer.execute, pointer.pointers)
#     # new_pointer.position = pos
#     # new_pointer.velocity = vel


@register_instruction("z")
def no_op(pointer):
    return True, True


@register_instruction("{")
def start_block(pointer):
    n = pointer.stack_pop()
    soss = []
    if n > 0:
        z = 0
        if n > len(pointer.stack):
            z = len(pointer.stack) - n
            n = len(pointer.stack)
        soss += ([0] * z) + pointer.stack[-n:]
        pointer.stack = pointer.stack[:-n]
    else:
        soss += abs(n) * [0]

    x, y = pointer.storage_offset
    soss += [x, y]
    pointer.stack_of_stacks.append(soss)
    pointer.storage_offset = vec.add(pointer.position, pointer.velocity)
    return False, True


@register_instruction("}")
def end_block(pointer):
    if not pointer.stack_of_stacks:
        return

    n = pointer.stack_pop()
    soss = pointer.stack_of_stacks.pop()
    pointer.storage_offset = soss[-2:]
    soss = soss[:-2]
    if n > 0:
        z = 0
        if n > len(soss):
            z = len(soss) - n
            n = len(soss)
        pointer.stack += ([0] * z) + soss[-n:]
        soss = soss[:-n]
    else:
        soss = soss[:n]

    x, y = pointer.storage_offset
    soss += [x, y]
    pointer.stack_of_stacks.append(soss)
    pointer.storage_offset = vec.add(pointer.position, pointer.velocity)
    return False, True


@register_instruction("u")
def transfer(pointer):
    if not pointer.stack_of_stacks:
        return

    n = pointer.stack_pop()
    soss = pointer.stack_of_stacks[-1]
    if n > 0:
        dest, source = pointer.stack, soss
    elif n == 0:
        return
    else:
        dest, source = soss, pointer.stack

    for _ in range(abs(n)):
        dest.append(source.pop())
    return False, True


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
        string += unichr(value)
        value = pointer.stack_pop()
    pointer.stack.push(call(string))
    return False, True


@register_instruction(" ")
def space(pointer):
    return True, True
