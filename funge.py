def is_hex(char):
    return all((x in "0123456789abcdef") for x in char.lower())


def DEFAULT_INSTRUCTION(pointer):
    char = pointer.program[pointer.position]
    if is_hex(char):
        pointer.stack.append(int(char, 16))
        return False, True
    return True, True
