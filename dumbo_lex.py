import ply.lex as lex

reserved = {
    'for': 'FOR',
    'print': 'PRINT',
    'in': 'IN',
    'do': 'DO',
    'endfor': 'ENDFOR',
    'if': 'IF',
    'true': 'BOOL',
    'false': 'BOOL',
    'or': 'OR',
    'and': 'AND',
    'endif': 'ENDIF',
}

tokens = ['LDUMBO', 'RDUMBO', 'COMMA', 'TXT', 'STRING', 'VARIABLE', 'SEMICOLON', 'ASSIGNATION', 'LPAR', 'RPAR',
          'DOT', 'COMP', 'INT', 'ADD_OP', 'MUL_OP'] + list(set(reserved.values()))

states = (
    ('dumbo', 'inclusive'),
)


def t_dumbo_RESERVED(t):
    r'print|for|in|do|endfor|true|false|or|and|if|endif'
    t.type = reserved.get(t.value, 'VARIABLE')
    return t


def t_LDUMBO(t):
    r'\{\{'  # {{
    t.lexer.begin('dumbo')
    return t


t_dumbo_ignore = ' \t'


def t_dumbo_RDUMBO(t):
    r'\}{2}\n?'  # }}
    t.lexer.begin('INITIAL')
    return t


t_dumbo_IF = r'if'
t_dumbo_FOR = r'for'
t_dumbo_IN = r'in'
t_dumbo_DO = r'do'
t_dumbo_PRINT = r'print'
t_dumbo_ENDFOR = r'endfor'
t_dumbo_ENDIF = r'endif'
t_dumbo_OR = r'or'
t_dumbo_AND = r'and'
t_dumbo_COMP = r'\=|\!\=|\<|\>'
t_dumbo_BOOL = r'true|false'
t_dumbo_ADD_OP = r'\+|\-'
t_dumbo_MUL_OP = r'\*|\/'
t_dumbo_SEMICOLON = r'\;'
t_dumbo_ASSIGNATION = r':='
t_dumbo_LPAR = r'\('
t_dumbo_RPAR = r'\)'
t_dumbo_COMMA = r'\,'
t_dumbo_DOT = r'\.'
t_dumbo_STRING = r"'[^']*'"
t_dumbo_INT = r'-?[0-9]+'
t_dumbo_VARIABLE = r'[a-zA-Z_][a-zA-Z0-9_]*'
t_TXT = r'[^{{2}]+'  # Tout sauf {{


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


def t_dumbo_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


lexer = lex.lex()
