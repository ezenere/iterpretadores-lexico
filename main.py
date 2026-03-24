PARENTHESIS = 1
PARENTHESIS_L = 1
PARENTHESIS_R = 2

MATH = 2
MATH_PLUS = 1
MATH_MINUS = 2
MATH_TIMES = 3
MATH_FLOAT_DIV = 4
MATH_INT_DIV = 5
MATH_MODULLUS = 6
MATH_EXPONENTIAL = 7

KEYWORD = 3
KEYWORD_RES = 1

FLOAT = 4
INT = 5

VARIABLE = 6

OPERATION = 7

class Token:
    def __init__(self, kind, value):
        self.kind = kind
        self.value = value

def state_end(expr, index, tokens):
    if index == len(expr):
        return tokens
    
    if expr[index] == ' ':
        return state_end(expr, index + 1, tokens)

    return False

def state_int_div_operand(expr, index, tokens, parentheses, token):
    if index == len(expr):
        return False

    if expr[index] in " )":
        tokens.append(Token(MATH, MATH_INT_DIV))
        return state_parentheses(expr, index, tokens, parentheses)

    return False

def state_single_operand(expr, index, tokens, parentheses, token):
    if index == len(expr):
        return False

    if expr[index] == '/':
        return state_int_div_operand(expr, index + 1, tokens, parentheses, token+'/')

    if expr[index] in " )" and token == '+':
        tokens.append(Token(MATH, MATH_PLUS))
        return state_parentheses(expr, index, tokens, parentheses)

    if expr[index] in " )" and token == '-':
        tokens.append(Token(MATH, MATH_MINUS))
        return state_parentheses(expr, index, tokens, parentheses)

    if expr[index] in " )" and token == '*':
        tokens.append(Token(MATH, MATH_TIMES))
        return state_parentheses(expr, index, tokens, parentheses)

    if expr[index] in " )" and token == '/':
        tokens.append(Token(MATH, MATH_FLOAT_DIV))
        return state_parentheses(expr, index, tokens, parentheses)

    if expr[index] in " )" and token == '%':
        tokens.append(Token(MATH, MATH_MODULLUS))
        return state_parentheses(expr, index, tokens, parentheses)

    if expr[index] in " )" and token == '^':
        tokens.append(Token(MATH, MATH_EXPONENTIAL))
        return state_parentheses(expr, index, tokens, parentheses)

    return False

def state_float_dot(expr, index, tokens, parentheses, token):
    if index == len(expr):
        return False

    if expr[index] in "0123456789":
        token += expr[index]
        return state_float(expr, index + 1, tokens, parentheses, token)
    
    return False

def state_float(expr, index, tokens, parentheses, token):
    if index == len(expr):
        return False

    if expr[index] in "0123456789":
        token += expr[index]
        return state_float(expr, index + 1, tokens, parentheses, token)

    if expr[index] in ' )':
        tokens.append(Token(FLOAT, float(token)))
        return state_parentheses(expr, index, tokens, parentheses)

    return False

def state_int(expr, index, tokens, parentheses, token):
    if index == len(expr):
        return False

    if expr[index] in "0123456789":
        token += expr[index]
        return state_int(expr, index + 1, tokens, parentheses, token)
    
    if expr[index] == '.':
        token += expr[index]
        return state_float_dot(expr, index + 1, tokens, parentheses, token)

    if expr[index] in ' )':
        tokens.append(Token(INT, int(token)))
        return state_parentheses(expr, index, tokens, parentheses)

    return False

def state_word_with_number(expr, index, tokens, parentheses, token):
    if index == len(expr):
        return False

    if expr[index] in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_':
        return state_word_with_number(expr, index + 1, tokens, parentheses, token + expr[index])
    
    if expr[index] in ' )':
        tokens.append(Token(VARIABLE, token))
        return state_parentheses(expr, index, tokens, parentheses)

    return False

def state_word(expr, index, tokens, parentheses, token):
    if index == len(expr):
        return False

    if expr[index] in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_':
        return state_word_with_number(expr, index + 1, tokens, parentheses, token + expr[index])

    if expr[index] in ' )':
        tokens.append(Token(VARIABLE, token))
        return state_parentheses(expr, index, tokens, parentheses)

    return False

def state_keyword_R(expr, index, tokens, parentheses, token):
    if index == len(expr):
        return False

    if expr[index] == 'E':
        return state_keyword_RE(expr, index + 1, tokens, parentheses, token + expr[index])

    if expr[index] in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_':
        return state_word_with_number(expr, index + 1, tokens, parentheses, token + expr[index])

    if expr[index] in ' )':
        tokens.append(Token(VARIABLE, token))
        return state_parentheses(expr, index, tokens, parentheses)

    return False

def state_keyword_RE(expr, index, tokens, parentheses, token):
    if index == len(expr):
        return False

    if expr[index] == 'S':
        return state_keyword_RES(expr, index + 1, tokens, parentheses, token + expr[index])

    if expr[index] in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_':
        return state_word_with_number(expr, index + 1, tokens, parentheses, token + expr[index])

    if expr[index] in ' )':
        tokens.append(Token(VARIABLE, token))
        return state_parentheses(expr, index, tokens, parentheses)

    return False

def state_keyword_RES(expr, index, tokens, parentheses, token):
    if index == len(expr):
        return False

    if expr[index] in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_':
        return state_word_with_number(expr, index + 1, tokens, parentheses, token + expr[index])

    if expr[index] in ' )':
        tokens.append(Token(KEYWORD, KEYWORD_RES))
        return state_parentheses(expr, index, tokens, parentheses)

    return False

def state_dangling_minus(expr, index, tokens, parentheses, token):
    if index == len(expr):
        return False

    if expr[index] in "0123456789":
        return state_int(expr, index + 1, tokens, parentheses, token + expr[index])

    return state_single_operand(expr, index, tokens, parentheses, token)


def state_parentheses(expr, index, tokens, parentheses):
    if index == len(expr):
        return False

    if expr[index] == ' ':
        return state_parentheses(expr, index + 1, tokens, parentheses)

    if expr[index] == '(':
        tokens.append(Token(PARENTHESIS,PARENTHESIS_L))
        return state_parentheses(expr, index + 1, tokens, parentheses + 1)

    if expr[index] in "0123456789":
        return state_int(expr, index + 1, tokens, parentheses, expr[index])

    if expr[index] == "R":
        return state_keyword_R(expr, index + 1, tokens, parentheses, expr[index])

    if expr[index] in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_":
        return state_word(expr, index + 1, tokens, parentheses, expr[index])

    if expr[index] == ".":
        return state_float_dot(expr, index + 1, tokens, parentheses, '0.')

    if expr[index] == "-":
        return state_dangling_minus(expr, index + 1, tokens, parentheses, expr[index])

    if expr[index] in ['+', '-', '*', '/', '%', '^']:
        return state_single_operand(expr, index + 1, tokens, parentheses, expr[index])
    
    if expr[index] == ')' and parentheses > 1:
        tokens.append(Token(PARENTHESIS, PARENTHESIS_R))
        return state_parentheses(expr, index + 1, tokens, parentheses - 1)

    if expr[index] == ')' and parentheses == 1:
        tokens.append(Token(PARENTHESIS, PARENTHESIS_R))
        return state_end(expr, index + 1, tokens)
    
    return False

def parse_expression(expr, index = 0):
    if index == len(expr):
        return False

    if expr[index] == ' ':
        return parse_expression(expr, index + 1)
    
    if expr[index] == '(':
        return state_parentheses(expr, index, [], 0)
        
    return False

def parse_expression_list(expressions):
    return [parse_expression(expression) for expression in expressions]

def display_parsed(parsed):
    espacos = ''
    for token in parsed:
        if token.kind == PARENTHESIS:
            if token.value == PARENTHESIS_L:
                print(f'{espacos}(')
                espacos = espacos + '  '
            else:
                espacos = espacos[:-2]
                print(f'{espacos})')
        elif token.kind == MATH:
            print(f'{espacos}Operador Matemático: ', end='')
            if token.value == MATH_PLUS:
                print('+ (Soma)')
            elif token.value == MATH_MINUS:
                print('- (Subtração)')
            elif token.value == MATH_TIMES:
                print('* (Multiplicação)')
            elif token.value == MATH_FLOAT_DIV:
                print('/ (Divisão)')
            elif token.value == MATH_INT_DIV:
                print('// (Divisão inteira)')
            elif token.value == MATH_MODULLUS:
                print('% (Módulo)')
            elif token.value == MATH_EXPONENTIAL:
                print('^ (Exponenciação)')
        elif token.kind == KEYWORD:
            print(f'{espacos}KEYWORD: ', end='')
            if token.value == KEYWORD_RES:
                print('RES')
        elif token.kind == FLOAT:
            print(f'{espacos}Ponto Flutuante: {token.value}')
        elif token.kind == INT:
            print(f'{espacos}Inteiro: {token.value}')
        elif token.kind == VARIABLE:
            print(f'{espacos}Variável: {token.value}')
        elif token.kind == OPERATION:
            print('OPERAÇÃO')

class Memory:
    def __init__(self):
        self.dict = {}

    def set(self, name, val):
        self.dict[name] = val

    def get(self, name):
        if name not in self.dict:
            return 0.0
        return self.dict[name]

class History:
    def __init__(self):
        self.heap = []
    
    def add(self, value):
        self.heap.append(value)

    def get(self, index):
        if index <= 0 or index > len(self.heap):
            return 0.0
        return self.heap[-index]

def execute_math(v1, v2, op):
    if op == MATH_PLUS:
        data = v1 + v2
    if op == MATH_MINUS:
        data = v1 - v2
    if op == MATH_TIMES:
        data = v1 * v2
    if op == MATH_FLOAT_DIV:
        data = float(v1) / float(v2) if v2 != 0 else float('inf')
    if op == MATH_INT_DIV:
        data = v1 // v2 if v2 != 0 else float('inf')
    if op == MATH_MODULLUS:
        data = v1 % v2 if v2 != 0 else float('inf')
    if op == MATH_EXPONENTIAL:
        data = v1 ** v2
    return data

def execute_expression(expression, memory, history):
    pile = []
    for i in range(len(expression)):
        token = expression[i]
        if token.kind == PARENTHESIS:
            continue
        if token.kind == INT or token.kind == FLOAT:
            pile.append(token.value)
        if token.kind == MATH:
            a = pile.pop()
            b = pile.pop()
            result = execute_math(b, a, token.value)
            pile.append(result)
        if token.kind == VARIABLE:
            if i == len(expression) - 2:
                if len(pile) == 1:
                    value = pile.pop()
                    memory.set(token.value, value)
                    pile.append(value)
                else:
                    pile.append(memory.get(token.value))
                    print(pile[-1])
            else:
                pile.append(memory.get(token.value))

        if token.kind == KEYWORD:
            if(token.value == KEYWORD_RES):
                pile.append(history.get(pile.pop()))

    if len(pile) > 0:
        history.add(pile.pop())

def execute(expressions):
    memory = Memory()
    history = History()

    for expression in expressions:
        execute_expression(expression, memory, history)

    return memory.dict, history.heap

parsed = parse_expression_list([
    "(10 5 +)",
    "(A)",
    "((10 5 +) A)",
    "(A)",
    "((2 3 +) (4 1 -) *)",
    "((2.5 4 *) (3 2 /) +)",
    "(((2 3 +) (4 1 -) *) B)",
    "((B 5 +) C)",
    "(C)",
    "(1 RES)",
    "(3 RES)",
    "((1 RES) (2 RES) +)",
    "((17 5 %) D)",
    "(D)",
    "((2 8 ^) E)",
    "(E)",
    "((7 2 //) F)",
    "(F)",
    "((9 2 /) G)",
    "(G)",
    "(((1 2 +) (3 4 +) +) H)",
    "((H A +) I)",
    "(I)",
    "((2 RES) (5 RES) *)",
    "(((1 RES) (A B +) *) J)",
    "(J)",

    "(0)",
    "(0.0)",
    "(.5)",
    "(0007)",
    "(0007 0003 +)",
    "((1 2 +) (3 4 +) +)",
    "(((1 2 +) (3 4 +) +) X)",
    "(X)",
    "((X 2 ^) Y)",
    "(Y)",
    "((1 RES) (2 RES) +)",
    "((3 RES) (1 RES) *)",
    "((2.5 2 ^) Z)",
    "(Z)",
    "((10 3 %) M)",
    "(M)",
    "((10 3 //) N)",
    "(N)",
    "((10 3 /) O)",
    "(O)",
    "((((1 1 +) (2 2 +) +) ((3 3 +) (4 4 +) +) +) P)",
    "(P)",
    "((P X +) Q)",
    "(Q)",
    "((1 RES) R)",
    "(R)",

    "(U)",
    "((1 U +) V)",
    "(V)",
    "(100 RES)",
    "((1 0 /) A)",
    "((1 0 //) B)",
    "((1 0 %) C)",
    "((0 0 ^) D)",
    "((2 -3 +) E)",
    "((2 3 ^) (4 5 ^) +)",
    "((1 RES) (999 RES) +)",
    "(-20 MENOR)"
])

memory, history = execute(parsed)

print(memory, history)
