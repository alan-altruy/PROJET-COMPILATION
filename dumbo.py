import ply.yacc as yacc
from dumbo_lex import tokens
from dumbo_execute import execute

precedence = (
    ('left', 'ADD_OP'),
    ('left', 'MUL_OP'),
    ('left', 'LPAR', 'RPAR'),
    ('left', 'SEMICOLON'),
    ('left', 'COMP'),
    ('left', 'OR'),
    ('left', 'AND'),
    ('left', 'DOT'),
    ('left', 'COMMA'),
    ('left', 'ASSIGNATION'),
)


def p_programme(p):
    '''programme : TXT
                 | TXT programme
                 | dumbo_bloc
                 | dumbo_bloc programme'''
    if not (str(p[1]).startswith("('dumbo',") or str(p[1]).startswith("('newline',")):
        p[1] = ('txt', p[1])
    if len(p) == 2:
        p[0] = ('prog', p[1])
    elif len(p) == 3:
        p[0] = ('prog', p[1], p[2])


def p_dumbo_bloc(p):
    '''dumbo_bloc : LDUMBO expressions_list RDUMBO
                  | LDUMBO RDUMBO'''
    if len(p) == 4:
        p[0] = ('dumbo', p[2])
        if p[3] == '}}\n':
           p[0] = ('newline', ('dumbo', p[2]))
    else:
        p[0] = ('dumbo', ('txt', ''))


def p_expressions_list(p):
    '''expressions_list : expression SEMICOLON expressions_list
                        | expression SEMICOLON'''
    if len(p) == 4:
        p[0] = ('list_expressions', p[1], p[3])
    elif len(p) == 3:
        p[0] = ('list_expressions', p[1])


def p_expression(p):
    '''expression : PRINT string_expression
                  | FOR VARIABLE IN string_list DO expressions_list ENDFOR
                  | FOR VARIABLE IN VARIABLE DO expressions_list ENDFOR
                  | IF boolean_expression DO expressions_list ENDIF
                  | VARIABLE ASSIGNATION string_expression
                  | VARIABLE ASSIGNATION string_list
                  | VARIABLE ASSIGNATION int_expression
                  | VARIABLE ASSIGNATION boolean_expression'''
    if len(p) == 3:
        p[0] = ('print', p[2])
    elif len(p) == 4:
        p[0] = ('assign', p[1], p[3])
    elif len(p) == 6:
        p[0] = ('if', p[2], p[4])
    elif len(p) == 8:
        p[0] = ('for', p[2], p[4], p[6])


def p_string_expression(p):
    '''string_expression : STRING
                  | VARIABLE
                  | string_expression DOT string_expression'''
    if len(p) == 4:
        p[0] = ('concat', p[1], p[3])
    elif len(p) == 2 and p[1][0] == "'":
        p[0] = ('str', p[1])
    else:
        p[0] = ('var', ('str', p[1]))


def p_int_expression(p):
    '''int_expression : INT
                      | int_term ADD_OP int_term
                      | int_term MUL_OP int_term'''
    if len(p) == 2:
        p[0] = ('int', p[1])
    else:
        p[0] = ('op', p[1], p[2], p[3])


def p_int_term(p):
    '''int_term : VARIABLE
                | int_expression
                | LPAR int_expression RPAR'''
    if len(p) == 4:
        p[0] = p[2]
    elif isinstance(p[1], tuple):
        p[0] = p[1]
    else:
        p[0] = ('var', ('int', (p[1])))


def p_boolean_expression(p):
    '''boolean_expression : BOOL
                          | int_term COMP int_term
                          | boolean_term OR boolean_term
                          | boolean_term AND boolean_term'''
    if len(p) == 2:
        if p[1] == 'true':
            p[0] = ('bool', True)
        elif p[1] == 'false':
            p[0] = ('bool', False)
        else:
            p[0] = ('var', ('bool', p[1]))
    elif p[2] == 'or':
        p[0] = ('or', p[1], p[3])
    elif p[2] == 'and':
        p[0] = ('and', p[1], p[3])
    else:
        p[0] = ('comp', p[1], p[2], p[3])


def p_boolean_term(p):
    '''boolean_term : VARIABLE
                    | boolean_expression'''
    if isinstance(p[1], tuple):
        p[0] = p[1]
    else:
        p[0] = ('var', ('bool', (p[1])))


def p_string_list(p):
    'string_list : LPAR string_list_interior RPAR'
    p[0] = p[2]


def p_string_list_interior(p):
    '''string_list_interior : STRING
                            | STRING COMMA string_list_interior'''
    if len(p) == 2:
        p[0] = ('list_string', p[1])
    elif len(p) == 4:
        p[0] = ('list_string', p[1], p[3])


def p_error(p):
    print("Syntax error in input! " + str(p))


if __name__ == "__main__":
    import sys

    length = len(sys.argv)
    if length != 3:
        print("Wrong number of arguments passed : ", length)
    else:
        dataFileName = sys.argv[1]
        templateFileName = sys.argv[2]

        parser = yacc.yacc(debug=True)
        try:
            dataFile = open(dataFileName, "r").read()
            data = parser.parse(dataFile)
            templateFile = open(templateFileName, "r").read()
            template = parser.parse(templateFile)
            print(execute(data, template))
        except EOFError:
            pass
