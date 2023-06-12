variables = {}


def execute(data: tuple, template: tuple):
    unpack(data)
    unpacked = unpack(template)
    return unpacked


def unpack(prog: tuple):
    if prog is None:
        return ""
    type_exp = prog[0]
    if type_exp == 'prog':
        return prog_exp(prog)
    elif type_exp == 'txt':
        return prog[1]
    elif type_exp == 'dumbo':
        return unpack(prog[1])
    elif type_exp == 'print':
        return unpack(prog[1])
    elif type_exp == 'for':
        return for_exp(prog[1], variables[prog[2]], prog[3])
    elif type_exp == 'if':
        return if_exp(prog)
    elif type_exp == 'assign':
        return assign_exp(prog[1], unpack(prog[2]))
    elif type_exp == 'str':
        return prog[1][1:-1]
    elif type_exp == 'int':
        return int(prog[1])
    elif type_exp == 'list_string':
        return list_str(prog)
    elif type_exp == 'bool':
        return bool(prog[1])
    elif type_exp == 'comp':
        return comp_exp(unpack(prog[1]), prog[2], unpack(prog[3]))
    elif type_exp == 'or':
        return unpack(prog[1]) or unpack(prog[2])
    elif type_exp == 'and':
        return unpack(prog[1]) and unpack(prog[2])
    elif type_exp == 'var':
        return var_exp(variables[prog[1][1]], prog[1][0])
    elif type_exp == 'list_expressions':
        return list_expressions_exp(prog)
    elif type_exp == 'op':
        return op_exp(unpack(prog[1]), prog[2], unpack(prog[3]))
    elif type_exp == 'concat':
        return unpack(prog[1]) + unpack(prog[2])
    elif type_exp == 'newline':
        return unpack(prog[1]) + "\n"


def prog_exp(prog: tuple):
    if len(prog) > 2:
        prog1 = unpack(prog[1])
        if prog1[0] == 'newline':
            prog1 = prog1[1]
        return str(prog1) + str(unpack(prog[2]))
    return str(unpack(prog[1]))


def list_expressions_exp(prog: tuple):
    if len(prog) > 2:
        prog1 = unpack(prog[1])
        prog2 = unpack(prog[2])
        if prog1 is None:
            return prog2
        if prog2 is None:
            return prog1
        return prog1 + prog2
    return unpack(prog[1])


def for_exp(var, lst, to_do):
    mem = ""
    to_return = ""
    flag = var not in variables
    if flag:
        variables[var] = ''
    else:
        mem = variables[var]
    for i in lst:
        variables[var] = i
        to_return += unpack(to_do)
    if flag:
        del variables[var]
    else:
        variables[var] = mem
    return to_return


def if_exp(prog: tuple):
    if unpack(prog[1]):
        return unpack(prog[2])
    return ""


def assign_exp(var, val):
    variables[var] = val
    return ""


def list_str(prog: tuple):
    if len(prog) > 2:
        return [prog[1][1:-1]] + unpack(prog[2])
    return [prog[1][1:-1]]


def comp_exp(int1, sign, int2):
    if sign == '<':
        return int1 < int2
    elif sign == '>':
        return int1 > int2
    elif sign == '!=':
        return int1 != int2
    elif sign == '=':
        return int1 == int2


def op_exp(int1, sign, int2):
    if sign == '+':
        return int1 + int2
    elif sign == '-':
        return int1 - int2
    elif sign == '*':
        return int1 * int2
    elif sign == '/':
        return int1 // int2


def var_exp(var, type):
    if type == 'str':
        return str(var)
    elif type == 'int':
        return int(var)
    elif type == 'bool':
        return bool(var)
