from common import *

def state_comment(expr, index, tokens):
    if index == len(expr):
        return tokens
    
    return state_comment(expr, index + 1, tokens)

def state_end(expr, index, tokens):
    if index == len(expr):
        return tokens
    
    if expr[index] == ' ':
        return state_end(expr, index + 1, tokens)
    
    if expr[index] == '#':
        return state_comment(expr, index, tokens)

    raise Exception(f"Caractere não reconhecido '{expr[index]}'")

def state_int_div_operand(expr, index, tokens, parentheses):
    if index == len(expr):
        raise Exception('Expressão inacabada.')

    if expr[index] in " )":
        tokens.append(Token(MATH, MATH_INT_DIV))
        return state_parentheses(expr, index, tokens, parentheses)

    raise Exception(f"Caractere não reconhecido '{expr[index]}'")

def state_single_operand(expr, index, tokens, parentheses, token):
    if index == len(expr):
        raise Exception('Expressão inacabada.')

    if expr[index] == '/':
        return state_int_div_operand(expr, index + 1, tokens, parentheses)

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

    raise Exception(f"Caractere não reconhecido '{expr[index]}'")

def state_float_dot(expr, index, tokens, parentheses, token):
    if index == len(expr):
        raise Exception('Expressão inacabada.')

    if expr[index] in "0123456789":
        token += expr[index]
        return state_float(expr, index + 1, tokens, parentheses, token)
    
    raise Exception(f"Caractere não reconhecido '{expr[index]}'")

def state_float(expr, index, tokens, parentheses, token):
    if index == len(expr):
        raise Exception('Expressão inacabada.')

    if expr[index] in "0123456789":
        token += expr[index]
        return state_float(expr, index + 1, tokens, parentheses, token)

    if expr[index] in ' )':
        tokens.append(Token(FLOAT, float(token)))
        return state_parentheses(expr, index, tokens, parentheses)

    raise Exception(f"Caractere não reconhecido '{expr[index]}'")

def state_int(expr, index, tokens, parentheses, token):
    if index == len(expr):
        raise Exception('Expressão inacabada.')

    if expr[index] in "0123456789":
        token += expr[index]
        return state_int(expr, index + 1, tokens, parentheses, token)
    
    if expr[index] == '.':
        token += expr[index]
        return state_float_dot(expr, index + 1, tokens, parentheses, token)

    if expr[index] in ' )':
        tokens.append(Token(INT, int(token)))
        return state_parentheses(expr, index, tokens, parentheses)

    raise Exception(f"Caractere não reconhecido '{expr[index]}'")

def state_word_with_number(expr, index, tokens, parentheses, token):
    if index == len(expr):
        raise Exception('Expressão inacabada.')

    if expr[index] in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_':
        return state_word_with_number(expr, index + 1, tokens, parentheses, token + expr[index])
    
    if expr[index] in ' )':
        tokens.append(Token(VARIABLE, token))
        return state_parentheses(expr, index, tokens, parentheses)

    raise Exception(f"Caractere não reconhecido '{expr[index]}'")

def state_word(expr, index, tokens, parentheses, token):
    if index == len(expr):
        raise Exception('Expressão inacabada.')

    if expr[index] in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_':
        return state_word_with_number(expr, index + 1, tokens, parentheses, token + expr[index])

    if expr[index] in ' )':
        tokens.append(Token(VARIABLE, token))
        return state_parentheses(expr, index, tokens, parentheses)

    raise Exception(f"Caractere não reconhecido '{expr[index]}'")

def state_keyword_R(expr, index, tokens, parentheses, token):
    if index == len(expr):
        raise Exception('Expressão inacabada.')

    if expr[index] == 'E':
        return state_keyword_RE(expr, index + 1, tokens, parentheses, token + expr[index])

    if expr[index] in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_':
        return state_word_with_number(expr, index + 1, tokens, parentheses, token + expr[index])

    if expr[index] in ' )':
        tokens.append(Token(VARIABLE, token))
        return state_parentheses(expr, index, tokens, parentheses)

    raise Exception(f"Caractere não reconhecido '{expr[index]}'")

def state_keyword_RE(expr, index, tokens, parentheses, token):
    if index == len(expr):
        raise Exception('Expressão inacabada.')

    if expr[index] == 'S':
        return state_keyword_RES(expr, index + 1, tokens, parentheses, token + expr[index])

    if expr[index] in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_':
        return state_word_with_number(expr, index + 1, tokens, parentheses, token + expr[index])

    if expr[index] in ' )':
        tokens.append(Token(VARIABLE, token))
        return state_parentheses(expr, index, tokens, parentheses)

    raise Exception(f"Caractere não reconhecido '{expr[index]}'")

def state_keyword_RES(expr, index, tokens, parentheses, token):
    if index == len(expr):
        raise Exception('Expressão inacabada.')

    if expr[index] in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_':
        return state_word_with_number(expr, index + 1, tokens, parentheses, token + expr[index])

    if expr[index] in ' )':
        tokens.append(Token(KEYWORD, KEYWORD_RES))
        return state_parentheses(expr, index, tokens, parentheses)

    raise Exception(f"Caractere não reconhecido '{expr[index]}'")

def state_dangling_minus(expr, index, tokens, parentheses, token):
    if index == len(expr):
        raise Exception('Expressão inacabada.')

    if expr[index] in "0123456789":
        return state_int(expr, index + 1, tokens, parentheses, token + expr[index])

    return state_single_operand(expr, index, tokens, parentheses, token)


def state_parentheses(expr, index, tokens, parentheses):
    if index == len(expr):
        raise Exception('Expressão inacabada.')

    if expr[index] == ' ':
        return state_parentheses(expr, index + 1, tokens, parentheses)

    if expr[index] == '(':
        tokens.append(Token(PARENTHESES,PARENTHESES_L))
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
        tokens.append(Token(PARENTHESES, PARENTHESES_R))
        return state_parentheses(expr, index + 1, tokens, parentheses - 1)

    if expr[index] == ')' and parentheses == 1:
        tokens.append(Token(PARENTHESES, PARENTHESES_R))
        return state_end(expr, index + 1, tokens)
    
    raise Exception(f"Caractere não reconhecido '{expr[index]}'")

def parse_expression(expr, index = 0):
    if index == len(expr):
        raise Exception('Expressão inacabada.')

    if expr[index] == ' ':
        return parse_expression(expr, index + 1)
    
    if expr[index] == '(':
        return state_parentheses(expr, index, [], 0)
    
    if expr[index] == '#':
        return state_comment(expr, index, [])
        
    raise Exception(f"Caractere não reconhecido '{expr[index]}'")

def parse_expression_list(expressions):
    return [v for v in [parse_expression(expression) for expression in expressions] if len(v) > 0]

def parse_file(file):
    with open(file, "r", encoding="utf-8") as f:
        return parse_expression_list([linha.strip() for linha in f if linha.strip()])
