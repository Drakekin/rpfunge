def is_hex(char):
    for x in char.lower():
        if not x in "0123456789abcdef":
            return False
    return True


def DEFAULT_INSTRUCTION(pointer):
    char = pointer.program.__getitem__(pointer.position)
    if is_hex(char):
        pointer.stack.append(int(char, 16))
        return False, True
    return True, True
