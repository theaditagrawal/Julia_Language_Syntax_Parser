import ply.lex as lex
import ply.yacc as yacc

trigger = True

reserved = {
    'if': 'IF',
    'elseif': 'ELIF',
    'else': 'ELSE',
    'while': 'WHILE',
    'for': 'FOR',
    'true': 'TRUE',
    'false': 'FALSE',
    'in': 'IN',
    'print': 'PRINT',
    'function': 'FUNCTION',
    'struct': 'STRUCT',
    'end': 'END',
    'until': 'UNTIL',
}

tokens = [
    'NAME', 'INT', 'FLOAT', 'STRING',
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'MODULO', 'EQUALS',
    'LPAREN', 'RPAREN',
    'EQUAL', 'NOTEQ', 'LARGE', 'SMALL', 'LRGEQ', 'SMLEQ', 'COLON', 'COMMA',
    'FUNCTION_CALL', 'STRUCT_DECLARATION',
] + list(reserved.values())

t_PLUS = r'\+'
t_MINUS = r'\-'
t_TIMES = r'\*'
t_DIVIDE = r'\/'
t_MODULO = r'\%'
t_EQUALS = r'\='
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_EQUAL = r'\=\='
t_NOTEQ = r'\!\='
t_LARGE = r'\>'
t_SMALL = r'\<'
t_LRGEQ = r'\>\='
t_SMLEQ = r'\<\='
t_COLON = r'\:'
t_STRING = r'\'[^\']*\'|\"[^\"]*\"'
t_COMMA = r'\,'
t_ignore = " \t"

def t_INT(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_FLOAT(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t

def t_NAME(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'NAME')
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

lexer = lex.lex()

precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE', 'MODULO'),
    ('left', 'EQUAL', 'NOTEQ', 'LARGE', 'SMALL', 'LRGEQ', 'SMLEQ'),
)

env = {}   # stores variables

def p_calc(p):
    '''
    calc : statement
    '''
    if trigger:
        print("Valid construct")
    else:
        print("Invalid construct")

def p_statement(p):
    '''
    statement : expression
              | conditions
              | loops
              | var_assign
              | function_call
              | struct_declaration
    '''

def p_while_np(p):
    '''
    loops : WHILE expression COLON statements END
    '''

def p_while_p(p):
    '''
    loops : WHILE LPAREN expression RPAREN COLON statements END
    '''

def p_for(p):
    '''
    loops : FOR NAME IN expression COLON statements END
    '''

def p_statements(p):
    '''
    statements : statement
               | statement statements
    '''

def p_conditions_until(p):
    '''
    conditions : UNTIL expression COLON statements END
    '''

def p_conditions_if_np(p):
    '''
    conditions : IF expression COLON statements END
    '''

def p_conditions_if_p(p):
    '''
    conditions : IF LPAREN expression RPAREN COLON statements END
    '''

def p_conditions_if_else_np(p):
    '''
    conditions : IF expression COLON statements ELSE COLON statements END
    '''

def p_conditions_if_else_p(p):
    '''
    conditions : IF LPAREN expression RPAREN COLON statements ELSE COLON statements END
    '''

def p_conditions_if_elif_else_np(p):
    '''
    conditions : IF expression COLON statements ELIF expression COLON statements ELSE COLON statements END
    '''

def p_conditions_if_elif_else_p(p):
    '''
    conditions : IF LPAREN expression RPAREN COLON statements ELIF LPAREN expression RPAREN COLON statements ELSE COLON statements END
    '''

def p_var_assign(p):
    '''
    var_assign : NAME EQUALS expression
    '''

def p_print_expression(p):
    '''
    expression : PRINT LPAREN expressions RPAREN
    '''

def p_print_expressions(p):
    '''
    expressions : expression
                | expression COMMA expressions
    '''
def p_loops_until(p):
    '''
    loops : UNTIL expression COLON statements END
          | UNTIL LPAREN expression RPAREN COLON statements END
    '''

def p_function_call(p):
    '''
    function_call : NAME LPAREN argument_list RPAREN
    '''
    p[0] = f"{p[1]}({p[3]})"

def p_argument_list(p):
    '''
    argument_list : expression COMMA argument_list
                  | expression
    '''
    if len(p) == 4:
        p[0] = f"{p[1]}, {p[3]}"
    else:
        p[0] = f"{p[1]}"

def p_struct_declaration(p):
    '''
    struct_declaration : STRUCT NAME COLON struct_fields END
    '''

def p_struct_fields(p):
    '''
    struct_fields : struct_field
                  | struct_field struct_fields
    '''

def p_struct_field(p):
    '''
    struct_field : NAME EQUALS expression
    '''

def p_expression(p):
    '''
    expression : expression PLUS expression
               | expression MINUS expression
               | expression TIMES expression
               | expression DIVIDE expression
               | expression MODULO expression
               | expression EQUAL expression
               | expression NOTEQ expression
               | expression LARGE expression
               | expression SMALL expression
               | expression LRGEQ expression
               | expression SMLEQ expression
    '''

def p_expression_int_float(p):
    '''
    expression : INT
               | FLOAT
               | STRING
               | TRUE
               | FALSE
    '''

def p_expression_var(p):
    '''
    expression : NAME
    '''

def p_error(p):
    global trigger
    trigger = False
    if p is not None:
        print("Syntax error : '%s'" % p.value)
    else:
        print("Syntax error: unexpected end of input")

parser = yacc.yacc()

while True:
    trigger = True
    try:
        lines = []
        user_input = input(">> ")
        if user_input[-1] == ":":
            while True:
                if user_input == '':
                    break
                else:
                    lines.append(user_input + '\n')
                user_input = input(".. ")
            s = "".join(lines)
        else:
            s = user_input
    except EOFError:
        break
    parser.parse(s)